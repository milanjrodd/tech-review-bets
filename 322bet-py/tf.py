import numpy as np
import tensorflow as tf
import keras
from keras import layers
import pandas as pd
import os
import torch
from pathlib import Path
import process_data

# Read mathes data
process_matches_path = os.path.join(os.getcwd(), '322bet-py','data','matches_processed.csv')

if not Path(process_matches_path).exists():
    matches = process_data.process_matches(process_matches_path)
else:
    matches = pd.read_csv(process_matches_path)

testDataCount = len(matches)//4
batch_size = len(matches)*5//100

trainData  = matches.head(-testDataCount)
tensor_train_input = tf.convert_to_tensor(trainData[['radiant_hero_1_winrate', 'radiant_hero_2_winrate', 'radiant_hero_3_winrate', 'radiant_hero_4_winrate', 'radiant_hero_5_winrate', 'dire_hero_1_winrate', 'dire_hero_2_winrate', 'dire_hero_3_winrate', 'dire_hero_4_winrate', 'dire_hero_5_winrate']].to_numpy(), np.float32, name='train_input')
data_train_output = trainData['radiant_win'].to_numpy()
tensor_train_output = tf.convert_to_tensor([[i, 1-i] for i in data_train_output], np.float32, name='train_output')

testData =  matches.tail(testDataCount)
tensor_test_input = tf.convert_to_tensor(testData[['radiant_hero_1_winrate', 'radiant_hero_2_winrate', 'radiant_hero_3_winrate', 'radiant_hero_4_winrate', 'radiant_hero_5_winrate', 'dire_hero_1_winrate', 'dire_hero_2_winrate', 'dire_hero_3_winrate', 'dire_hero_4_winrate', 'dire_hero_5_winrate']].to_numpy(), np.float32, name='test_input')
data_test_output = np.array([[i, 1-i] for i in testData['radiant_win'].to_numpy()])

# Define Sequential model with 2 layers
model = keras.Sequential(
    [
        layers.Dense(256, activation="relu", name="input"),
        layers.Dense(128, activation="relu", name="hidden1"),
        layers.Dense(2, activation="softmax", name="output"),
    ]
)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

checkpoint_filepath = '/tmp/checkpoint'
model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

print("Train on {} samples, validate on {} samples".format(len(tensor_train_input), len(tensor_test_input)))
model.fit(tensor_train_input, tensor_train_output, validation_data=(tensor_test_input, data_test_output), epochs=300, batch_size=batch_size, callbacks=[model_checkpoint_callback])

# The model weights (that are considered the best) are loaded into the
# model.
model.load_weights(checkpoint_filepath)

print("Evaluate on test data")
model.evaluate(tensor_test_input, data_test_output)

# Save model
model.save(os.path.join(os.getcwd(), '322bet-py','models','model.keras'))
print("Saved model to disk")