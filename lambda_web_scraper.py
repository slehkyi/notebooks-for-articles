import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create urls for all SEASONS of all LEAGUES
BASE_URL = 'https://understat.com/league'
LEAGUES = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1']
SEASONS = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
# SEASONS = ['2021']


def get_teams_data(data):
    # Get teams and their relevant ids and put them into separate dictionary
    teams = {}
    for id in data.keys():
        teams[id] = data[id]['title']
    
    # EDA to get a feeling of how the JSON is structured
    # Column names are all the same, so we just use first element
    columns = []
    # Check the sample of values per each column
    values = []
    for id in data.keys():
        columns = list(data[id]['history'][0].keys())
        values = list(data[id]['history'][0].values())
        break
    
    # Getting data for all teams
    dataframes = {}
    for id, team in teams.items():
        teams_data = []
        for row in data[id]['history']:
            teams_data.append(list(row.values()))

        df = pd.DataFrame(teams_data, columns=columns)
        dataframes[team] = df
        # print('Added data for {}.'.format(team))

    return dataframes


def get_data_from_web(league, season):
    url = BASE_URL+'/'+league+'/'+season
    logger.info("Scraping " + url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")

    # Based on the structure of the webpage, I found that data is in the JSON variable, under <script> tags
    scripts = soup.find_all('script')
    
    string_with_json_obj = ''

    # Find data for teams
    for el in scripts:
        if 'teamsData' in str(el):
            string_with_json_obj = str(el).strip()

    # print(string_with_json_obj)

    # strip unnecessary symbols and get only JSON data
    ind_start = string_with_json_obj.index("('")+2
    ind_end = string_with_json_obj.index("')")
    json_data = string_with_json_obj[ind_start:ind_end]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    
    # convert JSON data into Python dictionary
    data = json.loads(json_data)

    return data

def calculate_custom_parameters(dataframes):
    for team, df in dataframes.items():
        dataframes[team]['ppda_coef'] = dataframes[team]['ppda'].apply(lambda x: x['att']/x['def'] if x['def'] != 0 else 0)
        dataframes[team]['oppda_coef'] = dataframes[team]['ppda_allowed'].apply(lambda x: x['att']/x['def'] if x['def'] != 0 else 0)
        dataframes[team]['xG_h'] = dataframes[team].apply(lambda x: x['xG'] if x['h_a'] == 'h' else 0.0, axis=1)
        dataframes[team]['xG_a'] = dataframes[team].apply(lambda x: x['xG'] if x['h_a'] == 'a' else 0.0, axis=1)
        dataframes[team]['xGA_h'] = dataframes[team].apply(lambda x: x['xGA'] if x['h_a'] == 'h' else 0.0, axis=1)
        dataframes[team]['xGA_a'] = dataframes[team].apply(lambda x: x['xGA'] if x['h_a'] == 'a' else 0.0, axis=1)
        dataframes[team]['matches_h'] = dataframes[team].apply(lambda x: 1 if x['h_a'] == 'h' else 0.0, axis=1)
        dataframes[team]['matches_a'] = dataframes[team].apply(lambda x: 1 if x['h_a'] == 'a' else 0.0, axis=1)

    return dataframes


def regroup_data(dataframes):
    cols_to_sum = ['xG', 'xG_h', 'xG_a', 'xGA', 'xGA_h', 'xGA_a', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins', 'draws', 'loses', 'pts', 'npxGD', 'matches_h', 'matches_a']
    cols_to_mean = ['ppda_coef', 'oppda_coef']
    
    frames = []
    for team, df in dataframes.items():
        sum_data = pd.DataFrame(df[cols_to_sum].sum()).transpose()
        mean_data = pd.DataFrame(df[cols_to_mean].mean()).transpose()
        final_df = sum_data.join(mean_data)
        final_df['team'] = team
        final_df['matches'] = len(df)
        frames.append(final_df)

    full_stat = pd.concat(frames)

    return full_stat


def adjustments_for_final_table_look(full_stat):
    full_stat = full_stat[['team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'xG_h', 'xG_a', 'xGA', 'xGA_h', 'xGA_a', 'npxG', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts', 'matches_h', 'matches_a']]
    full_stat.sort_values('pts', ascending=False, inplace=True)
    full_stat.reset_index(inplace=True, drop=True)
    full_stat['position'] = range(1,len(full_stat)+1)
    
    full_stat['xG_diff'] = full_stat['xG'] - full_stat['scored']
    full_stat['xGA_diff'] = full_stat['xGA'] - full_stat['missed']
    full_stat['xpts_diff'] = full_stat['xpts'] - full_stat['pts']
    
    cols_to_int = ['wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'deep', 'deep_allowed']
    full_stat[cols_to_int] = full_stat[cols_to_int].astype(int)
    
    col_order = ['position', 'team', 'matches', 'wins', 'draws', 'loses', 'scored', 'missed', 'pts', 'xG', 'xG_diff', 'npxG', 'xGA', 'xGA_diff', 'npxGA', 'npxGD', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed', 'xpts', 'xpts_diff', 'xG_h', 'xG_a', 'xGA_h', 'xGA_a', 'matches_h', 'matches_a']
    full_stat = full_stat[col_order]
    full_stat = full_stat.set_index('position')
    # print(full_stat.head(20))

    return full_stat


def lambda_handler(event, context):
    logger.info('Getting teams data...')

    full_data = dict()
    for league in LEAGUES:
    
        season_data = dict()
        for season in SEASONS:
            data = get_data_from_web(league, season)

            dataframes = get_teams_data(data)

            dataframes = calculate_custom_parameters(dataframes)

            full_stat = regroup_data(dataframes)
            
            season_data[season] = adjustments_for_final_table_look(full_stat)
    
        df_season = pd.concat(season_data)
        full_data[league] = df_season
        
    data = pd.concat(full_data)
    cols_norm = data.select_dtypes(include=[object]).columns
    data[cols_norm] = data[cols_norm].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    # data.to_csv('understat_teams.csv')

    # s3_client = boto3.client('s3')
    # response = s3_client.upload_file('understat_teams.csv', 'xg-live-data', 'data/understat_teams_from_local.csv')

    data.to_csv('s3://xg-live-data/data/understat_teams.csv')
    
    return "Got the latest data"
