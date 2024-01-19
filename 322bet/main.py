import numpy as np
import keras
from keras import layers
import pandas as pd
from pathlib import Path
import process_data
import os
from heroes_synergy import CreateSynergyData

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


def get_one_hot_heroes_tensor(targets: pd.DataFrame, nb_classes: int):
    import tensorflow as tf

    one_hot_mask = np.eye(nb_classes)
    one_hot_heroes = one_hot_mask[
        targets[
            [
                "radiant_hero_1",
                "radiant_hero_2",
                "radiant_hero_3",
                "radiant_hero_4",
                "radiant_hero_5",
                "dire_hero_1",
                "dire_hero_2",
                "dire_hero_3",
                "dire_hero_4",
                "dire_hero_5",
            ]
        ].to_numpy()
    ]
    one_hot_heroes = one_hot_heroes.reshape(len(targets), nb_classes * 10)
    one_hot_heroes_tensor = tf.convert_to_tensor(
        one_hot_heroes, np.float32, name="one_hot_heroes"
    )
    return one_hot_heroes_tensor


def main():
    import tensorflow as tf

    physical_devices = tf.config.list_physical_devices("GPU")
    if len(physical_devices) > 0:
        print("GPU Available", physical_devices)
        tf.config.set_logical_device_configuration(
            physical_devices[0],
            [tf.config.LogicalDeviceConfiguration(memory_limit=10000)],
        )

    # Read mathes data
    process_matches_path = Path(__file__).parent / "./data/matches_processed.csv"

    if not Path(process_matches_path).exists():
        matches = process_data.process_matches(process_matches_path)
    else:
        matches = pd.read_csv(process_matches_path)

    matches_data = matches
    mathes_synergy_data = CreateSynergyData(matches_data)

    testDataCount = len(matches_data) // 4

    trainData = matches_data.head(-testDataCount)
    trainSynergies = mathes_synergy_data.head(-testDataCount).values.tolist()

    tensor_train_input = tf.convert_to_tensor(
        trainData[
            [
                "radiant_hero_1_winrate",
                "radiant_hero_2_winrate",
                "radiant_hero_3_winrate",
                "radiant_hero_4_winrate",
                "radiant_hero_5_winrate",
                "dire_hero_1_winrate",
                "dire_hero_2_winrate",
                "dire_hero_3_winrate",
                "dire_hero_4_winrate",
                "dire_hero_5_winrate",
                "avg_rank_tier",
            ]
        ].to_numpy(),
        np.float32,
        name="train_input",
    )
    tensor_train_synergies = tf.convert_to_tensor(
        trainSynergies, np.float32, name="synergies"
    )
    tensor_train_input = tf.concat([tensor_train_input, tensor_train_synergies], 1)

    data_train_output = trainData["radiant_win"].to_numpy()
    tensor_train_output = tf.convert_to_tensor(
        [[i] for i in data_train_output], np.float32, name="train_output"
    )

    testData = matches_data.tail(testDataCount)
    testSynergies = mathes_synergy_data.tail(testDataCount).values.tolist()

    tensor_test_input = tf.convert_to_tensor(
        testData[
            [
                "radiant_hero_1_winrate",
                "radiant_hero_2_winrate",
                "radiant_hero_3_winrate",
                "radiant_hero_4_winrate",
                "radiant_hero_5_winrate",
                "dire_hero_1_winrate",
                "dire_hero_2_winrate",
                "dire_hero_3_winrate",
                "dire_hero_4_winrate",
                "dire_hero_5_winrate",
                "avg_rank_tier",
            ]
        ].to_numpy(),
        np.float32,
        name="test_input",
    )
    tensor_test_synergies = tf.convert_to_tensor(
        testSynergies, np.float32, name="synergies"
    )

    tensor_test_input = tf.concat([tensor_test_input, tensor_test_synergies], 1)
    data_test_output = np.array([[i] for i in testData["radiant_win"].to_numpy()])

    # Define Sequential model with 2 layers
    model = keras.Sequential(
        [
            layers.Dense(64, activation="relu", name="input"),
            layers.Dense(32, activation="sigmoid", name="hidden1"),
            layers.Dense(1, activation="sigmoid", name="output"),
        ]
    )

    model.compile(
        optimizer="adam", loss=keras.losses.BinaryCrossentropy(), metrics=["accuracy"]
    )

    checkpoint_filepath = "/tmp/checkpoint"
    model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
    )

    print(f"Train on {len(trainData)} samples, validate on {len(testData)} samples")
    model.fit(
        tensor_train_input,
        tensor_train_output,
        validation_data=(tensor_test_input, data_test_output),
        epochs=100,
        batch_size=16000,
        callbacks=[model_checkpoint_callback],
    )

    # The model weights (that are considered the best) are loaded into the
    # model.
    model.load_weights(checkpoint_filepath)

    print("Evaluate on test data")
    model.evaluate(tensor_test_input, data_test_output)
    res = model(tensor_test_input)

    print(res)
    print(data_test_output)

    # Save model
    path_to_save = Path("models/model_lts.keras")
    model.save(path_to_save)
    print("Saved model to disk")


if __name__ == "__main__":
    main()
