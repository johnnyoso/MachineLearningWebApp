from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\og_log_reg.pkl', 'rb'))

@app.route("/", methods = ['GET', 'POST'])
def home():
    
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
    
    predict_team_id = request.form.get('predict_team_names')
    opposing_team_id = request.form.get('opposing_team_names')

    print('predict_team_id', predict_team_id)
    print('opposing_team_id', opposing_team_id)

    return render_template('index.html', teams = teams)

if __name__ == "__main__":
    app.run()