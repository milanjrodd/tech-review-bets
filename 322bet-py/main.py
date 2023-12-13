import pandas as pd
import torch
import numpy
import matplotlib.pyplot as plt
from torchsummary import summary
from datetime import datetime
from parallel_pandas import ParallelPandas
from pathlib import Path

# initialize parallel-pandas
ParallelPandas.initialize(n_cpu=12, split_factor=4, disable_pr_bar=False)


def main():
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'
    tensor_device = torch.device(device)
    # Read mathes data

    heroes = pd.read_json("../dataParser/heroes.json").set_index("id")

    def getHeroWinrate(heroId: int, rank: int) -> float:
        heroPicks, heroWins = heroes.loc[heroId][[
            f'{rank}_pick', f'{rank}_win']]
        heroWinRate = heroWins / heroPicks
        return round(heroWinRate, 5)

    def mapHeroIdsToWinrates(ids: str, rank: int) -> list[float]:
        return list([getHeroWinrate(heroId=int(id), rank=rank) for id in ids.split(',')])

    matches = pd.read_csv("../dataParser/matches.csv")

    # Normalize and merge data
    matches['radiant_win'] += 0
    matches['radiant_heroes_winrates'] = matches.p_apply(lambda x: mapHeroIdsToWinrates(
        x['radiant_team'], x['avg_rank_tier']//10), axis=1)
    matches['dire_heroes_winrates'] = matches.p_apply(lambda x: mapHeroIdsToWinrates(
        x['dire_team'], x['avg_rank_tier']//10), axis=1)

    testDataCount = len(matches)//4
    trainData = matches.head(-testDataCount)
    testData = matches.tail(testDataCount)

    data_train_input = (trainData['radiant_heroes_winrates'] +
                        trainData['dire_heroes_winrates']).to_numpy()
    data_train_output = [[i] for i in trainData['radiant_win'].to_numpy()]

    # Convert to tensor
    tensor_train_input = torch.tensor(list(data_train_input)).to(
        torch.float32).to(tensor_device)
    tensor_train_output = torch.tensor(list(data_train_output)).to(
        torch.float32).to(tensor_device)

    print("Input:\n", tensor_train_input)
    print("Shape:\n", tensor_train_input.shape)
    print("Answers:\n", tensor_train_output)
    print("Shape:\n", tensor_train_output.shape)

    # Step 2. Create model

    input_shape = 10
    output_shape = 1
    batch_size = 15000

    model = torch.nn.Sequential(
        torch.nn.Linear(input_shape, 10),
        torch.nn.ReLU(),
        torch.nn.Linear(10, 2),
        torch.nn.ReLU(),
        torch.nn.Linear(2, output_shape),
        torch.nn.Sigmoid()
    ).to(tensor_device)

    summary(model, (input_shape,), batch_size=batch_size, device=device)

    # Adam optimizer
    optimizer = torch.optim.Adam(
        model.parameters(), lr=1e-3, betas=(0.9, 0.99))

    # mean squared error
    loss = torch.nn.BCELoss()

    # Epochs
    epochs = 1000

    # Step 3. Train model
    print("Start train")

    history = []

    model = model.to(tensor_device)

    trained = False

    for epoch in range(epochs):
        if (trained):
            break

        permutation = torch.randperm(tensor_train_input.size()[0])

        for i in range(0, tensor_train_input.size()[0], batch_size):
            optimizer.zero_grad()

            indices = permutation[i:i+batch_size]
            batch_x, batch_y = tensor_train_input[indices], tensor_train_output[indices]

            # in case you wanted a semi-full example
            outputs = model(batch_x)
            loss_value = loss(outputs, batch_y)

            # Append to history
            loss_value_item = loss_value.item()
            history.append(loss_value_item)

            loss_value.backward()
            optimizer.step()

            # Break if trained
            if loss_value_item < 0.001:
                trained = True
                break

            # Debug output
            if epoch % 100 == 0:
                print(
                    f"{datetime.now().time()} {epoch+1},\t loss: {loss_value_item:.7f}")
            if device == 'cuda':
                torch.cuda.empty_cache()

    # Step 4. Control nn
    print("Control")

    data_test_input = (testData['radiant_heroes_winrates'] +
                       testData['dire_heroes_winrates']).to_numpy()
    data_test_output = testData['radiant_win'].to_numpy()

    tensor_train_input = torch.tensor(list(data_test_input)).to(
        torch.float32).to(tensor_device)

    print("Shape:", tensor_train_input.shape)

    answer = model(tensor_train_input)

    errors = 0

    for i in range(len(answer)):
        predicted = int(answer[i].round().item())
        real = data_test_output.item(i)
        if predicted != real:
            errors += 1

    print('Success rate: ', (1-(errors/testDataCount))*100, '%')
    plt.plot(history)
    plt.title('Loss')
    plt.savefig(
        f'graphs/history-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.png')
    plt.show()


if __name__ == "__main__":
    main()
