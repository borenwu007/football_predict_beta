import pandas as pd

def create_season_record(filename, cols = ['HomeTeam','AwayTeam','FTHG','FTAG']):
    df = pd.read_csv(filename)
    season_reacord = df[cols]
    return season_reacord

def create_team_dict(season_reacord):
    dict = {}
    index = 1
    for item in enumerate(season_reacord['HomeTeam']):
        team_name = item[1]
        if not (dict.__contains__(team_name)):
            dict[team_name]=index
            index += 1
    return dict

def cal_team_profile(season_reacord, team_name):
    total_matches = season_reacord['HomeTeam'].count()
    total_home_leagure_goals = season_reacord['FTHG'].sum()
    total_away_leagure_goals = season_reacord['FTAG'].sum()
    HGL_mean = total_home_leagure_goals / total_matches
    HLL_mean = total_away_leagure_goals / total_matches
    AGL_mean = total_away_leagure_goals / total_matches
    ALL_mean = total_home_leagure_goals / total_matches


    team_home_record = season_reacord[(season_reacord['HomeTeam'] == team_name)]
    team_away_record = season_reacord[(season_reacord['AwayTeam'] == team_name)]

    HG_mean = team_home_record['FTHG'].sum() / team_home_record['HomeTeam'].count()
    HL_mean = team_home_record['FTAG'].sum() / team_home_record['HomeTeam'].count()
    AG_mean = team_away_record['FTAG'].sum() / team_away_record['AwayTeam'].count()
    AL_mean = team_away_record['FTHG'].sum() / team_away_record['AwayTeam'].count()

    HOP = round(HG_mean / HGL_mean, 3)
    HDP = round(HL_mean / HLL_mean, 3)
    AOP = round(AG_mean / AGL_mean, 3)
    ADP = round(AL_mean / ALL_mean, 3)

    return  HOP,HDP,AOP,ADP

def create_team_profile(season_reacord, team_dict):
    profile_data = []
    for team_name in team_dict.keys():
        dict = {}
        dict['TeamName'] = team_name
        HOP,HDP,AOP,ADP = cal_team_profile(season_reacord, team_name)
        dict['HOP'] = HOP
        dict['HDP'] = HDP
        dict['AOP'] = AOP
        dict['ADP'] = ADP
        profile_data.append(dict)
    
    team_profile = pd.DataFrame(profile_data,index=None)
    return team_profile
        

filename = 'data/E0_2018_2019.csv'
season_record = create_season_record(filename)
team_dict = create_team_dict(season_record)
team_profile = create_team_profile(season_record,team_dict)
team_profile.sort_values(by="HOP",ascending=True).reset_index(drop=True).to_csv('result.csv',index=False)




