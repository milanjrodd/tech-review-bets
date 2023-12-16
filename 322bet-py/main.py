import os
import pandas as pd
import torch
import torch.nn as nn
import numpy
import matplotlib.pyplot as plt
from torchsummary import summary
from datetime import datetime
from pathlib import Path
import process_data


def main():
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = "cpu"
    tensor_device = torch.device(device)
    torch.set_default_device(device=device)

    # Read mathes data
    process_matches_path = os.path.join(
        os.getcwd(), "322bet-py", "data", "matches_processed.csv"
    )

    if not Path(process_matches_path).exists():
        matches = process_data.process_matches(process_matches_path)
    else:
        matches = pd.read_csv(process_matches_path)

    matches = matches.head(1000)

    testDataCount = len(matches) // 4

    trainData = matches.head(-testDataCount)
    tensor_train_input = torch.from_numpy(
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
            ]
        ].to_numpy()
    ).to(torch.float32)
    data_train_output = trainData["radiant_win"].to_numpy()
    tensor_train_output = torch.tensor([[i] for i in data_train_output]).to(
        torch.float32
    )

    testData = matches.tail(testDataCount)
    tensor_test_input = torch.from_numpy(
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
            ]
        ].to_numpy()
    ).to(torch.float32)
    data_test_output = testData["radiant_win"].to_numpy()

    print("Input:\n", tensor_train_input)
    print("Shape:\n", tensor_train_input.shape)
    print("Answers:\n", tensor_train_output)
    print("Shape:\n", tensor_train_output.shape)

    # Step 2. Create model
    input_shape = 10
    output_shape = 1
    batch_size = 15000

    model = torch.nn.Sequential(
        torch.nn.Linear(input_shape, 2),
        torch.nn.ReLU(),
        torch.nn.Linear(2, output_shape),
        torch.nn.Sigmoid(),
    ).to(tensor_device)

    summary(model, (input_shape,), batch_size=batch_size, device=device)

    # Adam optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-3, betas=(0.9, 0.99))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, "min")

    loss = torch.nn.BCELoss()

    # Epochs
    epochs = 1000

    # Step 3. Train model
    print("Start train")

    history = []

    model = model.to(tensor_device)

    trained = False

    for epoch in range(epochs):
        if trained:
            break

        permutation = torch.randperm(tensor_train_input.size()[0])
        loss_value_item = 0

        for i in range(0, tensor_train_input.size()[0], batch_size):
            optimizer.zero_grad()

            indices = permutation[i : i + batch_size]
            batch_x, batch_y = tensor_train_input[indices], tensor_train_output[indices]

            # in case you wanted a semi-full example
            outputs = model(batch_x)
            loss_value = loss(outputs, batch_y)

            # Append to history
            loss_value_item = loss_value.item()
            history.append(loss_value_item)

            loss_value.backward()
            optimizer.step()
            scheduler.step(loss_value)

            # # Break if trained
            # if loss_value_item < 0.1:
            #     trained = True
            #     break

        # Debug output
        if epoch % 100 == 0:
            print(f"{datetime.now().time()} {epoch+1},\t loss: {loss_value_item:.7f}")
            if device == "cuda":
                torch.cuda.empty_cache()

    # Step 4. Control nn
    print("Control")

    print("Shape:", tensor_test_input.shape)

    answer = model(tensor_test_input)

    errors = 0

    for i in range(len(answer)):
        predicted = int(answer[i].round().item())
        real = data_test_output.item(i)
        if predicted != real:
            errors += 1

    # print rate of radiants win in test data
    print(
        "Test radiants winrate: ",
        (sum(data_test_output) / len(data_test_output)) * 100,
        "%",
    )
    print("Success rate: ", (1 - (errors / testDataCount)) * 100, "%")
    plt.plot(history)
    plt.title("Loss")
    graphPath = os.path.join(
        os.getcwd(),
        f'322bet-py/graphs/history-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.png',
    )
    plt.savefig(graphPath)
    plt.show()


if __name__ == "__main__":
    main()
