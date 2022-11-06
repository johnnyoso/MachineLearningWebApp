from flask import Flask, request, render_template
import pickle, json
import pandas as pd

error_list = []

app = Flask(__name__)

teams = {'1838315' : 'Team Secret', 
             '2586976' : 'OG', 
             '2163'    : 'Team Liquid', 
             '7732977' : 'Boom Esports', 
             '15'      : 'PSG.LGD', 
             '7119388' : 'Team Spirit', 
             '8254400' : 'Beastcoast', 
             '6209166' : 'Team Aster', 
             '7391077' : 'Thunder Awaken', 
             '8260983' : 'TSM', 
             '8291895' : 'Tundra Esports', 
             '7390454' : 'Soniqs', 
             '8599101' : 'Gaimin Gladiators', 
             '39'      : 'Evil Geniuses', 
             '350190'  : 'Fnatic', 
             '8131728' : 'Hokori', 
             '8605863' : 'Entity', 
             '8721219' : 'BetBoom Team', 
             '6209804' : 'Royal Never Give Up', 
             '8597976' : 'Talon Esports'} 

log_reg_precision_recall = {'350190'  : (0.6310679611650486, 0.8057851239669421), 
                            '8254400' : (0.5882352941176471, 0.7407407407407407), 
                            '7732977' : (0.6990291262135923, 0.8571428571428571), 
                            '39'      : (0.6473988439306358, 0.8648648648648649),
                            '8599101' : (0.5, 0.6),
                            '8131728' : (0.7301587301587301, 0.7666666666666667),  
                            '15'      : (0.6467889908256881, 0.8730650154798761), 
                            '7390454' : (0.6710526315789473, 0.9272727272727272),  
                            '8597976' : (0.7, 0.7777777777777778),  
                            '2163'    : (0.5548387096774193, 0.8113207547169812),
                            '6209166' : (0.6379310344827587, 0.6851851851851852),
                            '1838315' : (0.7070707070707071, 0.967741935483871), 
                            '8291895' : (0.68, 0.9444444444444444),
                            '8721219' : (0.6666666666666666, 0.5555555555555556),
                            '8605863' : (0.7241379310344828, 0.7241379310344828),
                            '2586976' : (0.7247191011235955, 0.7371428571428571),
                            '7119388' : (0.6056338028169014, 0.8431372549019608),
                            '7391077' : (0.7567567567567568, 0.7567567567567568),
                            '8260983' : (0.7567567567567568, 0.7567567567567568),
                            '6209804' : (0.5897435897435898, 0.7419354838709677)}

pickle_team = {'2586976' : ('og_log_reg.pkl', 'og_data.json'),
                '1838315' : ('team_secret_log_reg.pkl', 'team_secret_data.json')}

@app.route("/", methods = ['GET', 'POST'])
def home():

    return render_template('index.html', teams = teams)


@app.route("/predict", methods = ['GET', 'POST'])
def predict():

    predict_team_id = request.form.get('predict_team_names')
    opposing_team_id = request.form.get('opposing_team_names')

    print('predict_team_id', predict_team_id)
    print('opposing_team_id', opposing_team_id)

    model = pickle.load(open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\pickles' + '\\' +  pickle_team[predict_team_id][0], 'rb'))
    
    with open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\data' + '\\' + pickle_team[predict_team_id][1], 'r', encoding="utf-8") as input_file:

        data = input_file.read()
        predict_team_matches = json.loads(data)
    
    with open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\data' + '\\' + pickle_team[opposing_team_id][1], 'r', encoding="utf-8") as input_file:

        data = input_file.read()
        opposing_team_matches = json.loads(data)
    
    predict_data = get_predict_data(predict_team_matches[0], opposing_team_matches[0])

    prediction = model.predict(predict_data)

    return render_template('index.html', prediction_text = prediction[0], teams = teams)


def get_predict_data(predict_team_dict, opposing_team_dict):

    predict_players_mmr_total = 0
    predict_players_mmr_count = 0
    opposing_players_mmr_total = 0
    opposing_players_mmr_count = 0

    for x, i in enumerate(predict_team_dict['predict_players']):

        try:
            predict_players_mmr_total += i['player_stats']['mmr_estimate']['estimate']
            predict_players_mmr_count += 1

        except:

            error_list.append()
            
    # get the average MMR of the predict team
    predict_players_mmr_average = predict_players_mmr_total / predict_players_mmr_count

    predict_team_total_matches = predict_team_dict['predict_team_stat'][0]['predict_team_wins_total'] + predict_team_dict['predict_team_stat'][0]['predict_team_losses_total']
    
    predict_team_win_pct = round(predict_team_dict['predict_team_stat'][0]['predict_team_wins_total'] / predict_team_total_matches * 100, 2)
    
    for y, j in enumerate(opposing_team_dict['predict_players']):

        try:
            opposing_players_mmr_total += i['player_stats']['mmr_estimate']['estimate']
            opposing_players_mmr_count += 1

        except:

            error_list.append()
    
    # get the average MMR of the opposing team
    opposing_players_mmr_average = opposing_players_mmr_total / opposing_players_mmr_count

    opposing_team_total_matches = opposing_team_dict['predict_team_stat'][0]['predict_team_wins_total'] + opposing_team_dict['predict_team_stat'][0]['predict_team_losses_total']

    opposing_team_win_pct = round(opposing_team_dict['predict_team_stat'][0]['predict_team_wins_total'] / opposing_team_total_matches * 100, 2)

    predict_data_df =  pd.DataFrame(data = {'predict_team_total_matches' : predict_team_total_matches, 
                                            'predict_team_win_pct' : predict_team_win_pct, 
                                            'predict_team_rating' : predict_team_dict['predict_team_stat'][0]['predict_team_rating'], 
                                            'predict_players_mmr_average' : predict_players_mmr_average, 
                                            'opposing_team_total_matches' : opposing_team_total_matches, 
                                            'opposing_team_win_pct' : opposing_team_win_pct, 
                                            'opposing_team_rating' : opposing_team_dict['predict_team_stat'][0]['predict_team_rating'], 
                                            'opposing_players_mmr_average' : opposing_players_mmr_average}, 
                                            index = [0])     

    return predict_data_df           

if __name__ == "__main__":
    app.run()