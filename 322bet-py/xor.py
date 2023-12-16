# -*- coding: utf-8 -*-

##
# Copyright (с) Ildar Bikmamatov 2022
# License: MIT
# Source: https://github.com/bayrell-tutorials/perceptron-xor
# Link:
# https://blog.bayrell.org/ru/iskusstvennyj-intellekt/411-obuchenie-mnogoslojnogo-perseptrona-operaczii-xor.html
##

import matplotlib.pyplot as plt
import torch
import os
import sys
from datetime import datetime as dt
from torch import nn
from torchsummary import summary

# Detect device for tensor
# cpu or cuda
device = "cuda"
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
tensor_device = torch.device(device)


# Step 1. Prepare DataSet
data_train = [
    {"in": [0, 0], "out": [0]},
    {"in": [0, 1], "out": [1]},
    {"in": [1, 0], "out": [1]},
    {"in": [1, 1], "out": [0]},
]


# Convert to question and answer
tensor_train_x = list(map(lambda item: item["in"], data_train))
tensor_train_y = list(map(lambda item: item["out"], data_train))

# Convert to tensor
tensor_train_x = torch.tensor(tensor_train_x).to(torch.float32).to(tensor_device)
tensor_train_y = torch.tensor(tensor_train_y).to(torch.float32).to(tensor_device)

print("Input:\n", tensor_train_x)
print("Shape:\n", tensor_train_x.shape)
print("Answers:\n", tensor_train_y)
print("Shape:\n", tensor_train_y.shape)

# Step 2. Create model

input_shape = 2
output_shape = 1

model = nn.Sequential(
    nn.Linear(input_shape, 16),
    nn.ReLU(),
    nn.Linear(16, output_shape),
    # nn.Softmax()
).to(tensor_device)

summary(model, (input_shape,), device=device)


# Adam optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.99))

# mean squared error
loss = nn.MSELoss()

# Batch size
batch_size = 2

# Epochs
epochs = 100000


# Step 3. Train model
print("Start train")

history = []

model = model.to(tensor_device)

for i in range(epochs):
    # Model result
    model_res = model(tensor_train_x)

    # Loss value
    loss_value = loss(model_res, tensor_train_y)

    # Append to history
    loss_value_item = loss_value.item()
    history.append(loss_value_item)

    # Calc gradient
    optimizer.zero_grad()
    loss_value.backward()

    # Optimize
    optimizer.step()

    # Break if trained
    if loss_value_item < 0.001:
        break

    # Debug output
    if i % 100 == 0:
        print(f"{dt.now().time()} {i+1},\t loss: {loss_value_item:.7f}")

    if device == "cuda":
        torch.cuda.empty_cache()


# Show history


plt.plot(history)
plt.title("Loss")
plt.savefig("xor_torch.png")
plt.show()


# Step 4. Control nn
print("Control")

control_x = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
]

control_x = torch.tensor(control_x).to(torch.float32).to(tensor_device)

print("Shape:", control_x.shape)

answer = model(control_x)

for i in range(len(answer)):
    print(control_x[i].tolist(), "->", answer[i].round().tolist())
