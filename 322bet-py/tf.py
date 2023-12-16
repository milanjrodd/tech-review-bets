import numpy as np
import tensorflow as tf
import keras
from keras import layers
import pandas as pd
import os
import torch
from pathlib import Path
import process_data

def get_one_hot_heroes_tensor(targets: pd.DataFrame, nb_classes: int):
    one_hot_mask = np.eye(nb_classes)
    one_hot_heroes = one_hot_mask[targets[['radiant_hero_1', 'radiant_hero_2', 'radiant_hero_3', 'radiant_hero_4', 'radiant_hero_5', 'dire_hero_1', 'dire_hero_2', 'dire_hero_3', 'dire_hero_4', 'dire_hero_5']].to_numpy()]
    one_hot_heroes = one_hot_heroes.reshape(len(targets), nb_classes*10)
    one_hot_heroes_tensor = tf.convert_to_tensor(one_hot_heroes, np.float32, name='one_hot_heroes')
    return one_hot_heroes_tensor

def main():
    # Read mathes data
    process_matches_path = os.path.join(os.getcwd(), '322bet-py','data','matches_processed.csv')

    if not Path(process_matches_path).exists():
        matches = process_data.process_matches(process_matches_path)
    else:
        matches = pd.read_csv(process_matches_path)

    matches = matches.head(150000)

    testDataCount = len(matches)//4
    batch_size = len(matches)*5//100

    trainData  = matches.head(-testDataCount)
    tensor_train_input = tf.convert_to_tensor(trainData[['radiant_hero_1_winrate', 'radiant_hero_2_winrate', 'radiant_hero_3_winrate', 'radiant_hero_4_winrate', 'radiant_hero_5_winrate', 'dire_hero_1_winrate', 'dire_hero_2_winrate', 'dire_hero_3_winrate', 'dire_hero_4_winrate', 'dire_hero_5_winrate', 'avg_rank_tier']].to_numpy(), np.float32, name='train_input')
    one_hot_heroes_tensor_train = get_one_hot_heroes_tensor(trainData, 140)
    tensor_train_input = tf.concat([tensor_train_input, one_hot_heroes_tensor_train], 1)
    data_train_output = trainData['radiant_win'].to_numpy()
    tensor_train_output = tf.convert_to_tensor([[i] for i in data_train_output], np.float32, name='train_output')

    testData =  matches.tail(testDataCount)
    tensor_test_input = tf.convert_to_tensor(testData[['radiant_hero_1_winrate', 'radiant_hero_2_winrate', 'radiant_hero_3_winrate', 'radiant_hero_4_winrate', 'radiant_hero_5_winrate', 'dire_hero_1_winrate', 'dire_hero_2_winrate', 'dire_hero_3_winrate', 'dire_hero_4_winrate', 'dire_hero_5_winrate', 'avg_rank_tier']].to_numpy(), np.float32, name='test_input')
    one_hot_heroes_tensor_test = get_one_hot_heroes_tensor(testData, 140)
    tensor_test_input = tf.concat([tensor_test_input, one_hot_heroes_tensor_test], 1)
    data_test_output = np.array([[i] for i in testData['radiant_win'].to_numpy()])

    # Define Sequential model with 2 layers
    model = keras.Sequential(
        [
            layers.Dense(16000, activation="relu", name="input"),
            layers.Dense(8000, activation="relu", name="hidden1"),
            layers.Dense(1, activation="sigmoid" ,name="output"),
        ]
    )

    model.compile(optimizer='adam', loss=keras.losses.BinaryCrossentropy(), metrics=['accuracy'])

    checkpoint_filepath = '/tmp/checkpoint'
    model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=True,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)

    print(f"Train on {len(trainData)} samples, validate on {len(testData)} samples")
    model.fit(one_hot_heroes_tensor_train, tensor_train_output, validation_data=(one_hot_heroes_tensor_test, data_test_output), epochs=300, batch_size=batch_size, callbacks=[model_checkpoint_callback])

    # The model weights (that are considered the best) are loaded into the
    # model.
    model.load_weights(checkpoint_filepath)

    print("Evaluate on test data")
    model.evaluate(tensor_test_input, data_test_output)
    res = model(tensor_test_input)

    print(res)
    print(data_test_output)

    # Save model
    model.save(os.path.join(os.getcwd(), '322bet-py','models','model_lts.keras'))
    print("Saved model to disk")

if __name__ == '__main__':
    main()