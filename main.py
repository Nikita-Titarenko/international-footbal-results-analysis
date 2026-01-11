import os

import kagglehub
import pandas as pd

import analysis as an
from model import predict_winner

def main():
    # path = kagglehub.dataset_download("martj42/international-football-results-from-1872-to-2017")
    path = 'C:/Users/Admin/.cache/kagglehub/datasets/martj42/international-football-results-from-1872-to-2017/versions/102'

    df = pd.read_csv(os.path.join(path, 'results.csv'))
    print(df.head(10))
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    an.analys_math_wins(df)
    MAIN_TOURNEMENTS = [
        'FIFA World Cup', 'FIFA World Cup qualification',
        'UEFA Euro', 'UEFA Euro qualification',
        'Copa América', 'UEFA Nations League',
        'African Cup of Nations', 'AFC Asian Cup', 'Gold Cup'
    ]
    df_main = df[df['tournament'].isin(MAIN_TOURNEMENTS)]
    an.analys_math_wins(df_main, ' include only main tournaments')
    FOOTBALL_ERAS = [1950, 1960, 1975, 1990, 2005, 2015, 2025]
    for start, end in zip(FOOTBALL_ERAS, FOOTBALL_ERAS[1:]): 
        an.analys_math_wins(
            df_main[(df_main['date'].dt.year > start) & (df_main['date'].dt.year <= end)],
            f' from {start} to {end}',
            10 if start <= 1975 else 15
        )
    an.analys_home_advantage(df)
    an.analys_total_goales_scored(df)
    an.analys_geopolitic(df)
    an.analys_hosted_countries(df)
    predict_winner(df)

if __name__ == '__main__':
    main()