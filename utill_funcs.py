from pyspark.sql.functions import when, col


def get_winner(df):
    if df['home_score'] > df['away_score']:
        return df['home_team']
    elif df['home_score'] < df['away_score']:
        return df['away_team']
    else:
        return 'draw'
    

def add_home_or_away_winner(df):
    return df.withColumn(
        'home_or_away_winner',
        when(col('winner') == col('home_team'), 'home')
        .when(col('winner') == col('away_team'), 'away')
        .otherwise('draw')
    )