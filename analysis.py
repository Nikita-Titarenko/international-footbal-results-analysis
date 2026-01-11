import pandas as pd

from visuals import build_barplot, build_plot

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
    df = df.copy()
    df['winner'] = df.apply(get_winner, axis=1)
    df['looser'] = df.apply(get_loser, axis=1)
    game_counts = pd.concat([df['winner'], df['looser']]).value_counts()
    eligible_countries = game_counts[game_counts >= min_games].index
    eligible_home_team = df['home_team'].isin(eligible_countries)
    eligible_away_team = df['away_team'].isin(eligible_countries)
    df = df[eligible_home_team & eligible_away_team]
    win_counts = df['winner'].value_counts()
    win_percent = (
        (win_counts / game_counts * 100)
        .dropna()
        .sort_values(ascending=False)
    )
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
    df = df.copy()
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
    df = df.copy()
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

def get_teams_str(row):
    if row['home_team'] > row['away_team']:
        return row['home_team'] + ' vs ' + row['away_team']
    else:
        return row['away_team'] + ' vs ' + row['home_team']
    
def analys_geopolitic(df):
    df = df.copy()
    home_team = df[['home_team', 'year']].rename(columns={'home_team': 'team'})
    away_team = df[['away_team', 'year']].rename(columns={'away_team': 'team'})
    unique_teams_by_years = (
        pd.concat([home_team, away_team])
        .groupby('year')['team']
        .nunique()
    )
    build_plot(
        unique_teams_by_years.index, 
        unique_teams_by_years.values, 
        'Years', 
        'Total unique teams',
        'Total unique teams during the years'
    )
    df['home_and_away_team'] = df.apply(get_teams_str, axis=1)
    top_frequent_pairs = df['home_and_away_team'].value_counts().head(10)
    build_barplot(
        top_frequent_pairs.index, 
        top_frequent_pairs.values,
        'Country',
        'Total fixtures',
        f'Top 10 teams like to play each other'
    )

def is_hosted_but_not_participated(row):
    return (
        row['home_team'] != row['country'] 
        and row['away_team'] != row['country']
    )

def analys_hosted_countries(df):
    df = df.copy()
    df['hosted_but_not_participated'] = (
        df.apply(is_hosted_but_not_participated, axis=1)
    )
    hosted_countries = (
        df
        .groupby('country')['hosted_but_not_participated']
        .count()
        .sort_values(ascending=False)
        .head(10)
    )
    build_barplot(
        hosted_countries.values,
        hosted_countries.index, 
        'Total host matches where they themselves are not participating in',
        'Country',
        ('Top 10 teams that host matches '
        'where they themselves are not participating in'),
        'h'
    )