import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

from analysis import get_teams_str

def get_result(row):
    if row['home_score'] > row['away_score']:
        return 1
    elif row['away_score'] > row['home_score']:
        return -1
    else:
        return 0
        
def get_order_result(row):
    if row['home_score'] == row['away_score']:
        return 0
    is_home_win = row['home_score'] > row['away_score']
    is_home_first = row['home_team'] > row['away_team']
    return 1 if is_home_win == is_home_first else -1
        
def get_last_wins(df, match_result, last_n):
    return (
        df
        .groupby('team')['result_team']
        .transform(
            lambda x: (
                (x==match_result)
                .rolling(last_n, min_periods=1)
                .sum()
                .shift(1)
                .fillna(0)
            )
        )
    )
        
def get_h2h_last_wins(df, match_result, last_n):
    return (
        df
        .groupby('home_and_away_team')['order_result']
        .transform(
            lambda x: (
                (x==match_result)
                .rolling(last_n, min_periods=1)
                .sum()
                .shift(1)
                .fillna(0)
            )
        )
    )

def predict_winner(df):
    df = df.copy()
    df['result'] = df.apply(get_result, axis=1)
    df['order_result'] = df.apply(get_order_result, axis=1)

    le_team = LabelEncoder()
    all_teams = pd.concat([df['home_team'], df['away_team']])
    le_team.fit(all_teams)
    df['home_team_enc'] = le_team.transform(df['home_team'])
    df['away_team_enc'] = le_team.transform(df['away_team'])
    df['home_and_away_team'] = df.apply(get_teams_str, axis=1)
    LAST_N_H2H = 10
    df['h2h_last_wins'] = get_h2h_last_wins(df, 1, LAST_N_H2H)
    df['h2h_last_draws'] = get_h2h_last_wins(df, 0, LAST_N_H2H)
    df['h2h_last_losses'] = get_h2h_last_wins(df, -1, LAST_N_H2H)
    home_df = (
        df[['home_team', 'result', 'date']]
        .rename(columns={'home_team':'team', 'result':'result_team'})
    )
    home_df['side'] = 'home'
    away_df = (
        df[['away_team', 'result', 'date']]
        .rename(columns={'away_team':'team'})
    )
    away_df['result_team'] = -away_df['result']
    away_df['side'] = 'away'
    all_results = pd.concat([home_df, away_df], ignore_index=True).sort_values('date')

    LAST_N_MATCHES = 20

    all_results['wins_last'] = get_last_wins(
        all_results, 
        1, 
        LAST_N_MATCHES
    )
    all_results['draws_last'] = get_last_wins(
        all_results, 
        0, 
        LAST_N_MATCHES
    )
    all_results['losses_last'] = get_last_wins(
        all_results, 
        -1, 
        LAST_N_MATCHES
    )

    home_stats = all_results[all_results['side'] == 'home'].reset_index(drop=True)
    away_stats = all_results[all_results['side'] == 'away'].reset_index(drop=True)
    df['home_wins_last'] = home_stats['wins_last']
    df['home_draws_last'] = home_stats['draws_last']
    df['home_losses_last'] = home_stats['losses_last']
    df['away_wins_last'] = away_stats['wins_last']
    df['away_draws_last'] = away_stats['draws_last']
    df['away_losses_last'] = away_stats['losses_last']
    x = df[['home_team_enc', 'away_team_enc', 'year',
            'home_wins_last', 'home_draws_last', 'home_losses_last',
            'away_wins_last', 'away_draws_last', 'away_losses_last',
            'h2h_last_wins', 'h2h_last_draws',
            'h2h_last_losses']]

    y = df['order_result']
    TRAIN_PERCENT = 0.8
    train_index = int(len(x) * TRAIN_PERCENT)
    x_train = x.iloc[:train_index]
    x_test = x.iloc[train_index:]
    y_train = y.iloc[:train_index]
    y_test = y.iloc[train_index:]
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))