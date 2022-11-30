import json
import pandas as pd
from datetime import datetime

class Team:

    def __init__(self, team_name):

        self.team_name = team_name

    def open_file(self):

        # open team matches JSON file
        with open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\data' + '\\' + self.team_name, 'r', encoding="utf-8") as input_file:

            data = input_file.read()
            team_matches_json = json.loads(data)
            team_matches_processed = Team.process_data(team_matches_json)
        
        return team_matches_df(team_matches_processed)

    def process_data(team_matches_json):

        error_list = []

        for index, item in enumerate(team_matches_json):

            predict_players_mmr_total = 0
            predict_players_mmr_count = 0
            for x, i in enumerate(item['predict_players']):

                try:
                    predict_players_mmr_total += i['player_stats']['mmr_estimate']['estimate']
                    predict_players_mmr_count += 1

                except:
                    
                    error_list.append(index)
                    
            # get the average MMR of the team
            try:
                team_matches_json[index]['predict_players_mmr_average'] = predict_players_mmr_total / predict_players_mmr_count
                
            except:
                team_matches_json[index]['predict_players_mmr_average'] = None
                error_list.append(index)

            opposing_players_mmr_total = 0
            opposing_players_mmr_count = 0
            for y, j in enumerate(item['opposing_players']):

                try:
                    opposing_players_mmr_total += j['player_stats']['mmr_estimate']['estimate']
                    opposing_players_mmr_count += 1

                except:

                    error_list.append(index)
            
            try:
                team_matches_json[index]['opposing_players_mmr_average'] = opposing_players_mmr_total / opposing_players_mmr_count
            
            except:
                team_matches_json[index]['opposing_players_mmr_average'] = None
                error_list.append(index)
            
            
            predict_team_total_matches = item['predict_team_stat'][0]['predict_team_wins_total'] + item['predict_team_stat'][0]['predict_team_losses_total']
            team_matches_json[index]['predict_team_total_matches'] = predict_team_total_matches
            
            predict_team_win_pct = round(item['predict_team_stat'][0]['predict_team_wins_total'] / predict_team_total_matches * 100, 2)
            team_matches_json[index]['predict_team_win_pct'] = predict_team_win_pct
            
            try:
                opposing_team_total_matches = item['opposing_team_stat'][0]['opposing_team_wins_total'] + item['opposing_team_stat'][0]['opposing_team_losses_total']
            
            except:
                error_list.append(index)
                opposing_team_total_matches = 0


            team_matches_json[index]['opposing_team_total_matches'] = opposing_team_total_matches 
            
            try:
                opposing_team_win_pct =  round(item['opposing_team_stat'][0]['opposing_team_wins_total'] / opposing_team_total_matches * 100, 2)
            except:
                error_list.append(index)
                opposing_team_win_pct = 0

            team_matches_json[index]['opposing_team_win_pct'] = opposing_team_win_pct

        return team_matches_json
        

    def match_outcome(radiant_win, radiant):
        if ((radiant_win == False and radiant == False) or (radiant_win == True and radiant == True)):
            return True
        
        elif ((radiant_win == True and radiant == False) or (radiant_win == False and radiant == True)):
            return False
    
    def predict_team_score(item):
        if item['radiant'] == True:
            return item['radiant_score']
        else:
            return item['dire_score']

    def opposing_team_score(item):
        if item['radiant'] == True:
            return item['dire_score']
        else:
            return item['radiant_score']
    
    # Convert the team matches json to a dataframe
def team_matches_df(team_matches_json):

    predict_team_name = team_matches_json[0]['predict_team_stat'][0]['predict_team_name']
    predict_team_id =  team_matches_json[0]['predict_team_stat'][0]['predict_team_id']
    
    all_matches_df = pd.DataFrame(data = [(datetime.fromtimestamp(item['start_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                                       predict_team_name,
                                                       predict_team_id,
                                                       item['predict_team_total_matches'],
                                                       item['predict_team_win_pct'],
                                                       item['predict_team_stat'][0]['predict_team_rating'],
                                                       item['predict_players_mmr_average'],
                                                       item['opposing_team_name'],
                                                       item['opposing_team_id'],
                                                       item['opposing_team_total_matches'],
                                                       item['opposing_team_win_pct'],
                                                       item['opposing_team_stat'][0]['opposing_team_rating'],
                                                       item['opposing_players_mmr_average'],
                                                       item['league_name'],
                                                       item['leagueid'],
                                                       item['cluster'], 
                                                       item['radiant_win'],
                                                       item['radiant'],
                                                       item['duration'], 
                                                       item['match_id'],
                                                       Team.match_outcome(item['radiant_win'], item['radiant']), 
                                                       Team.predict_team_score(item), 
                                                       Team.opposing_team_score(item)) for index, item in enumerate(team_matches_json)], 
                      columns = ['start_date', 
                                 'predict_team_name', 
                                 'predict_team_id', 
                                 'predict_team_total_matches', 
                                 'predict_team_win_pct',
                                 'predict_team_rating',   
                                 'predict_players_mmr_average', 
                                 'opposing_team_name', 
                                 'opposing_team_id', 
                                 'opposing_team_total_matches',
                                 'opposing_team_win_pct', 
                                 'opposing_team_rating',
                                 'opposing_players_mmr_average', 
                                 'league_name', 
                                 'leagueid', 
                                 'cluster', 
                                 'radiant_win', 
                                 'radiant', 
                                 'duration', 
                                 'match_id', 
                                 'match_outcome',
                                 'predict_team_score',
                                 'opposing_team_score'])
    
    return all_matches_df
