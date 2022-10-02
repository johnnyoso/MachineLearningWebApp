from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\og_log_reg.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():

    # Grabs the inputs values and uses them to make prediction
    predict_team_total_matches = float(request.form['predict_team_total_matches']) 
    predict_team_win_pct = float(request.form['predict_team_win_pct'])
    predict_team_rating = float(request.form['predict_team_rating'])
    predict_players_mmr_average = float(request.form['predict_players_mmr_average'])
    opposing_team_total_matches = float(request.form['opposing_team_total_matches'])
    opposing_team_win_pct = float(request.form['opposing_team_win_pct'])
    opposing_team_rating = float(request.form['opposing_team_rating'])
    opposing_players_mmr_average = float(request.form['opposing_players_mmr_average'])
    duration = float(request.form['duration'])

    prediction = model.predict([[predict_team_total_matches, 
       predict_team_win_pct,
       predict_team_rating, 
       predict_players_mmr_average,
       opposing_team_total_matches, 
       opposing_team_win_pct,
       opposing_team_rating, 
       opposing_players_mmr_average, 
       duration]])

    return render_template('index.html', prediction_text = f'Match Outcome is: {prediction}')

if __name__ == "__main__":
    app.run()