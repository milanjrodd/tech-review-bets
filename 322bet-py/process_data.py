import os
import pandas as pd
from parallel_pandas import ParallelPandas

# initialize parallel-pandas
ParallelPandas.initialize(n_cpu=8, split_factor=4, disable_pr_bar=False)

def process_matches(path: str):
  # Get the current working directory
  data_parser_dir = os.path.join(os.getcwd(), 'dataParser')

  # Construct the file paths
  matches_path = os.path.join(data_parser_dir, 'matches.csv')
  heroes_path = os.path.join(data_parser_dir, 'heroes.json')
  
  # Read the CSV file
  matches = pd.read_csv(matches_path).head(160000)
  heroes = pd.read_json(heroes_path).set_index('id')

  df = pd.DataFrame(columns=['match_id', 'radiant_win', 'radiant_hero_1', 'radiant_hero_2', 'radiant_hero_3', 'radiant_hero_4', 'radiant_hero_5', 'dire_hero_1', 'dire_hero_2', 'dire_hero_3', 'dire_hero_4', 'dire_hero_5', 'avg_rank_tier', 'radiant_hero_1_winrate', 'radiant_hero_2_winrate', 'radiant_hero_3_winrate', 'radiant_hero_4_winrate', 'radiant_hero_5_winrate', 'dire_hero_1_winrate', 'dire_hero_2_winrate', 'dire_hero_3_winrate', 'dire_hero_4_winrate', 'dire_hero_5_winrate'])

  # Add data to the dataframe using pandas library

  df['match_id'] = matches['match_id']
  df['avg_rank_tier'] = matches['avg_rank_tier']/100
  df['radiant_win'] = matches['radiant_win'] + 0

  for i in range(1, 6):
      df[f'radiant_hero_{i}'] = matches['radiant_team'].str.split(',').str[i-1]
      df[f'dire_hero_{i}'] = matches['dire_team'].str.split(',').str[i-1]

  # Picks and wins are stored in heroes.json file in colums 1_pick - 8_pick and 1_win - 8_win accordinally. Need to divide wins by picks to get winrate, and then add it to the dataframe

  for i in range(1, 6):
      df[f'radiant_hero_{i}_winrate'] = df[f'radiant_hero_{i}'].p_apply(lambda x: heroes.loc[int(x)][f'{matches["avg_rank_tier"].iloc[0]//10}_win'] / heroes.loc[int(x)][f'{matches["avg_rank_tier"].iloc[0]//10}_pick'])
      df[f'dire_hero_{i}_winrate'] = df[f'dire_hero_{i}'].p_apply(lambda x: heroes.loc[int(x)][f'{matches["avg_rank_tier"].iloc[0]//10}_win'] / heroes.loc[int(x)][f'{matches["avg_rank_tier"].iloc[0]//10}_pick'])

  print(df.head())
  # Save the dataframe to a CSV file
  df.to_csv(path, index=False)
  return df