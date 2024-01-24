import keras
from fastapi import FastAPI
from typing import Optional
from pathlib import Path
from os import path
import numpy as np
import pandas as pd
import tensorflow as tf
from heroes_synergy import CreateSynergyData


path_to_model = Path(__file__).parent / "./models/model_5886.keras"

model: Optional[keras.Model] = keras.models.load_model(path_to_model)

if model is None or not isinstance(model, keras.Model):
    raise RuntimeError("Failed to load the model")


app = FastAPI(title="322bet", description="Dota 2 match prediction API")


from fastapi import Query


@app.get("/predict")
def predict(
    ids: list[int] = Query(
        ...,
        min_length=10,
        max_length=10,
        example=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ),
    avg_rank_tier: int = Query(..., ge=10, le=85, example=10),
):
    # Check if the model is loaded
    if model is None:
        raise RuntimeError("Failed to load the model")

    # Create dataframe from the ids
    df = pd.DataFrame(
        data=[ids],
        columns=[
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
        ],
    )

    data_parser_dir = Path(__file__).parent.parent / "dataParser"

    heroes_path = path.join(data_parser_dir, "heroes.json")

    heroes = pd.read_json(heroes_path).set_index("id")

    # Add avg_rank_tier to the dataframe
    df["avg_rank_tier"] = avg_rank_tier

    for i in range(1, 6):
        df[f"radiant_hero_{i}_winrate"] = df[f"radiant_hero_{i}"].apply(
            lambda x: heroes.loc[int(x)][f'{df["avg_rank_tier"].iloc[0]//10}_win']
            / heroes.loc[int(x)][f'{df["avg_rank_tier"].iloc[0]//10}_pick']
        )
        df[f"dire_hero_{i}_winrate"] = df[f"dire_hero_{i}"].apply(
            lambda x: heroes.loc[int(x)][f'{df["avg_rank_tier"].iloc[0]//10}_win']
            / heroes.loc[int(x)][f'{df["avg_rank_tier"].iloc[0]//10}_pick']
        )

    # Get heroes synergy data
    synergy_df = CreateSynergyData(df, strict=True).values.tolist()

    df["avg_rank_tier"] = avg_rank_tier / 100

    tensor_data = tf.convert_to_tensor(
        df[
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
        name="input",
    )

    tensor_synergies = tf.convert_to_tensor(synergy_df, np.float32, name="synergies")

    tensor_data = tf.concat([tensor_data, tensor_synergies], 1)

    # Perform prediction using the loaded model
    prediction = model.predict(tensor_data)

    return {"radiant_win_prediction": prediction[0].item()}


if __name__ == "__main__":  #
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
