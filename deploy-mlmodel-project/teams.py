import json

class Team:

    def __init__(self, team_name):

        self.team_name = team_name

    def open_file(self):

        # open team matches JSON file
        with open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\data' + '\\' + self.team_name, 'r', encoding="utf-8") as input_file:

            data = input_file.read()
            team_matches_json = json.loads(data)
        
        return team_matches_json


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
