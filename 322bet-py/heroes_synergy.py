from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
import numpy as np
import tensorflow as tf

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API_KEY
API_KEY = os.getenv("STRATZ_API_KEY")

# Define the RankBracketBasicEnum
RankBracketBasicEnum = {
    "HERALD_GUARDIAN": "HERALD_GUARDIAN",
    "CRUSADER_ARCHON": "CRUSADER_ARCHON",
    "LEGEND_ANCIENT": "LEGEND_ANCIENT",
    "DIVINE_IMMORTAL": "DIVINE_IMMORTAL",
}


def create_query(hero_ids):
    base_query = f"""
    query getMatchSynergy(
      $mmr: [RankBracketBasicEnum]
    ) {{
      heroStats {{
    """

    for i, hero_id in enumerate(hero_ids, start=1):
        base_query += f"""
        h{i}: heroVsHeroMatchup(heroId: {hero_id}, bracketBasicIds: $mmr) {{
          advantage {{
            heroId
            with {{
              heroId2
              synergy
            }}
            vs {{
              heroId2
              synergy
            }}
          }}
        }}
        """

    base_query += "}}"
    return base_query


# Create a transport with a defined url
transport = RequestsHTTPTransport(
    url="https://api.stratz.com/graphql",
    headers={"Content-type": "application/json", "Authorization": f"Bearer {API_KEY}"},
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

total_heroes = 138

# Create a 3D dictionary with 138*138*4 elements
synergyMatrix, counterMatrix = [
    {
        i: {
            j: {k: 0.0 for k in range(1, total_heroes + 1)}
            for j in range(1, total_heroes + 1)
        }
        for i in RankBracketBasicEnum
    }
    for _ in range(2)
]


# Create loop for 138 heroes batched by 30 heroes in one query
batch_size = 30
heroes_to_fetch = range(0, total_heroes, batch_size)

for i in heroes_to_fetch:
    print(f"Executing batch {i + 1} to {min(i + batch_size, total_heroes)}")
    hero_ids = range(i + 1, min(i + batch_size + 1, total_heroes + 1))
    query = gql(create_query(hero_ids))
    for rank in RankBracketBasicEnum:
        result = client.execute(query, {"mmr": rank})
        print(f"{rank} executed for heroes {hero_ids}")

        for k, hero_id in enumerate(hero_ids, start=1):
            advantages = result["heroStats"][f"h{k}"]["advantage"]

            for l, advantage in enumerate(advantages):
                synergiesWith = {
                    advantage_with["heroId2"]: advantage_with["synergy"] / 100
                    for advantage_with in advantage["with"]
                }
                synergiesVs = {
                    advantage_vs["heroId2"]: advantage_vs["synergy"] / 100
                    for advantage_vs in advantage["vs"]
                }

                for hero_id2 in synergiesWith.keys():
                    synergyMatrix[rank][hero_id][hero_id2] = synergiesWith[hero_id2]

                for hero_id2 in synergiesVs.keys():
                    counterMatrix[rank][hero_id][hero_id2] = synergiesVs[hero_id2]

# create dataframe from dictionary synergyMatrix["HERALD_GUARDIAN"]


# call the function (matches_data)
def CreateSynergyData(matches_data: pd.DataFrame):
    output = []

    for _, match in matches_data.iterrows():
        data = []

        rankTier = match["avg_rank_tier"].astype(float) * 100

        if rankTier >= 10 and rankTier <= 25:
            rankTier = "HERALD_GUARDIAN"
        elif rankTier >= 30 and rankTier <= 45:
            rankTier = "CRUSADER_ARCHON"
        elif rankTier >= 50 and rankTier <= 65:
            rankTier = "LEGEND_ANCIENT"
        elif rankTier >= 70 and rankTier <= 85:
            rankTier = "DIVINE_IMMORTAL"
        else:
            raise Exception("Invalid rank tier")

        for hero1 in range(1, 6):
            radiantHero1 = match[f"radiant_hero_{hero1}"]
            direHero1 = match[f"dire_hero_{hero1}"]
            for hero2 in range(1, 6):
                if hero1 == hero2:
                    continue

                radiantHero2 = match[f"radiant_hero_{hero2}"]
                direHero2 = match[f"dire_hero_{hero2}"]

                data.append(synergyMatrix[rankTier][radiantHero1][radiantHero2])
                data.append(synergyMatrix[rankTier][direHero1][direHero2])

            for hero2 in range(1, 6):
                direHero2 = match[f"dire_hero_{hero2}"]
                data.append(counterMatrix[rankTier][radiantHero1][direHero2])

        output.append(data)

    return output


# for rank in RankBracketBasicEnum:
#     df = pd.DataFrame.from_dict(synergyMatrix[rank], orient="index")
#     print(f"{rank} MATRIX\n", df)
