import pandas as pd

URL = 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv'
data = pd.read_csv(URL)

championship = data[data['league'] == 'English League Championship']
championship = championship[['season', 'date', 'team1', 'team2', 'xg1', 'xg2']]
championship['xga1'] = championship['xg2']
championship['xga2'] = championship['xg1']

home_data = championship[['season', 'team1', 'xg1', 'xga1']]
away_data = championship[['season', 'team2', 'xg2', 'xga2']]

home_groupped = home_data.groupby(['season', 'team1']).mean().reset_index()
away_groupped = away_data.groupby(['season', 'team2']).mean().reset_index()

final_data = pd.merge(home_groupped, away_groupped, left_on=['team1','season'], right_on=['team2','season'])
final_data.drop(['team2'], axis='columns', inplace=True)
final_data.rename({'team1': 'team', 'xg1': 'xG_h', 'xga1': 'xGA_h', 'xg2': 'xG_a', 'xga2': 'xGA_a'}, axis='columns', inplace=True)

final_data.to_csv('data/xGA_championship.csv', index=False)
print("Done!")