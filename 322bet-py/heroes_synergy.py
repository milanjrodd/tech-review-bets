from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
import numpy as np
import tensorflow as tf
from parallel_pandas import ParallelPandas
from enum import Enum

from dotenv import load_dotenv
import os

# initialize parallel-pandas
ParallelPandas.initialize(n_cpu=8, disable_pr_bar=False, split_factor=2)

# Load the .env file
load_dotenv()

# Get the API_KEY
API_KEY = os.getenv("STRATZ_API_KEY")


class RankBracketBasicEnum(Enum):
    HERALD_GUARDIAN = 0
    CRUSADER_ARCHON = 1
    LEGEND_ANCIENT = 2
    DIVINE_IMMORTAL = 3


def map_rank_tier_to_enum(avg_rank_tier):
    if 10 <= avg_rank_tier <= 25:
        return RankBracketBasicEnum.HERALD_GUARDIAN
    elif 30 <= avg_rank_tier <= 45:
        return RankBracketBasicEnum.CRUSADER_ARCHON
    elif 50 <= avg_rank_tier <= 65:
        return RankBracketBasicEnum.LEGEND_ANCIENT
    elif 70 <= avg_rank_tier <= 85:
        return RankBracketBasicEnum.DIVINE_IMMORTAL
    else:
        raise ValueError("Invalid rank tier")


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
batch_size = 30

# Create loop for 138 heroes batched by 30 heroes in one query
heroes_to_fetch = range(0, total_heroes, batch_size)


def ApplySynergyData(matches_data: pd.DataFrame):
    """Apply Synergy Data"""
    # Create a 4D numpy array with dimensions (total_ranks, total_heroes, total_heroes)
    synergyMatrix, counterMatrix = [
        np.zeros((len(RankBracketBasicEnum), total_heroes + 1, total_heroes + 1))
        for _ in range(2)
    ]

    def calculate_synergy(match: pd.Series):
        data = []
        rank = map_rank_tier_to_enum(match["avg_rank_tier"].astype(float) * 100)

        for hero1 in range(1, 6):
            radiantHero1 = match[f"radiant_hero_{hero1}"].astype(int)
            direHero1 = match[f"dire_hero_{hero1}"].astype(int)
            for hero2 in range(1, 6):
                direHero2 = match[f"dire_hero_{hero2}"].astype(int)
                data.append(counterMatrix[rank.value][radiantHero1][direHero2])

                if hero1 == hero2:
                    continue

                radiantHero2 = match[f"radiant_hero_{hero2}"].astype(int)

                data.append(synergyMatrix[rank.value][radiantHero1][radiantHero2])
                data.append(synergyMatrix[rank.value][direHero1][direHero2])

        return data

    for i in heroes_to_fetch:
        print(f"Executing batch {i + 1} to {min(i + batch_size, total_heroes)}")
        hero_ids = range(i + 1, min(i + batch_size + 1, total_heroes + 1))
        query = gql(create_query(hero_ids))
        for rank in RankBracketBasicEnum:
            result = client.execute(query, {"mmr": rank.name})
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
                        synergyMatrix[rank.value][hero_id][hero_id2] = synergiesWith[
                            hero_id2
                        ]

                    for hero_id2 in synergiesVs.keys():
                        counterMatrix[rank.value][hero_id][hero_id2] = synergiesVs[
                            hero_id2
                        ]

    output = matches_data.p_apply(calculate_synergy, axis=1)  # type: ignore
    return output.values.tolist()
