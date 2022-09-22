from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open(r'C:\Users\johnp\deploy-mlmodel\deploy-mlmodel-project\og_log_reg.pkl', 'rb'))

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()