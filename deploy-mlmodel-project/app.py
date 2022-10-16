from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open(r'C:\Users\johnp\deploy-mlmodel\MachineLearningWebApp\deploy-mlmodel-project\og_log_reg.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():

    predict_team = request.form.get('predict-team-names')
    opposing_team = request.form.get('opposing-team-names')

    print(predict_team)
    print(opposing_team)

    return render_template('index.html')


if __name__ == "__main__":
    app.run()