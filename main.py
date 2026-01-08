import os

import kagglehub
import pandas as pd

from visuals import build_barplot, build_plot

def main():
    # path = kagglehub.dataset_download("martj42/international-football-results-from-1872-to-2017")
    path = 'C:/Users/Admin/.cache/kagglehub/datasets/martj42/international-football-results-from-1872-to-2017/versions/102'

    df = pd.read_csv(os.path.join(path, 'results.csv'))

    def get_winner(row):
        if row['home_score'] > row['away_score']:
            return row['home_team']
        elif row['away_score'] > row['home_score']:
            return row['away_team']
        else:
            return None
        
    def get_loser(row):
        if row['home_score'] > row['away_score']:
            return row['away_team']
        elif row['away_score'] > row['home_score']:
            return row['home_team']
        else:
            return None
        
    def analys_math_wins(df, additional_title='', min_games=100):
        df['winner'] = df.apply(get_winner, axis=1)
        df['looser'] = df.apply(get_loser, axis=1)
        game_counts = pd.concat([df['winner'], df['looser']]).value_counts()

        eligible_countries = game_counts[game_counts >= min_games].index
        df = df[(df['home_team'].isin(eligible_countries)) & (df['away_team'].isin(eligible_countries))]
        win_counts = df['winner'].value_counts()
        win_percent = (win_counts / game_counts * 100).dropna().sort_values(ascending=False)

        top_ten_win_counts = win_counts.head(10)
        build_barplot(
            top_ten_win_counts.index, 
            top_ten_win_counts.values,
            'Country',
            'Number of wins',
            f'Top 10 country for number of wins{additional_title}'
        )

        top_ten_win_percents = win_percent.head(10)
        build_barplot(
            top_ten_win_percents.index, 
            top_ten_win_percents.values,
            'Country',
            'Percent of wins',
            f'Top 10 country for percent of wins{additional_title}'
        )

    def analys_home_advantage(df):
        df = df[~df['neutral']]
        df['winner'] = df.apply(get_winner, axis=1)
        df['is_home_win'] = df['winner'] == df['country']

        df = df[df['year'] >= 1980]
        df_grouped = df.groupby('year')['is_home_win'].mean() * 100

        build_plot(
            df_grouped.index, 
            df_grouped.values, 
            'Years', 
            'Percent of wins at home', 
            'Home advantage during the years'
        )

    def analys_total_goales_scored(df):
        df['total_goals'] = df['home_score'] + df['away_score']
        df = df[df['year'] >= 1900]
        df_grouped = df.groupby('year')['total_goals'].mean()

        build_plot(
            df_grouped.index, 
            df_grouped.values, 
            'Years', 
            'Total goals scored', 
            'Total goals scored during the years'
        )

    def get_unique_teams_count(df):
        return pd.concat([df['home_team'], df['away_team']]).nunique()
    
    def get_teams_str(row):
        if row['home_team'] > row['away_team']:
            return row['home_team'] + ' vs ' + row['away_team']
        else:
            return row['away_team'] + ' vs ' + row['home_team']

    def analys_geopolitic(df):
        df = pd.DataFrame(df)

        unique_teams_by_years = df.groupby('year').apply(get_unique_teams_count)

        build_plot(
            unique_teams_by_years.index, 
            unique_teams_by_years.values, 
            'Years', 
            'Total unique teams',
            'Total unique teams during the years'
        )

        df['home_and_away_team'] = df.apply(get_teams_str, axis=1)

        top_frequent_pairings = df['home_and_away_team'].value_counts().head(10)

        build_barplot(
            top_frequent_pairings.index, 
            top_frequent_pairings.values,
            'Country',
            'Total fixtures',
            f'Top 10 teams like to play each other'
        )
    
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year

    # analys_math_wins(df)
    # MAIN_TOURNEMENTS = [
    #     'FIFA World Cup', 'FIFA World Cup qualification',
    #     'UEFA Euro', 'UEFA Euro qualification',
    #     'Copa América', 'UEFA Nations League',
    #     'African Cup of Nations', 'AFC Asian Cup', 'Gold Cup'
    # ]
    # df = df[df['tournament'].isin(MAIN_TOURNEMENTS)]
    # analys_math_wins(df, ' include only main tournaments')
    # FOOTBALL_ERAS = [1950, 1960, 1975, 1990, 2005, 2015, 2025]
    # for start, end in zip(FOOTBALL_ERAS, FOOTBALL_ERAS[1:]): 
    #     analys_math_wins(
    #         df[(df['date'].dt.year > start) & (df['date'].dt.year <= end)],
    #         f' from {start} to {end}',
    #         10 if start <= 1975 else 15
    #     )
    # analys_home_advantage(df)
    # analys_total_goales_scored(df)
    analys_geopolitic(df)

if __name__ == '__main__':
    main()