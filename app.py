from flask import Flask, request, render_template, redirect, url_for

import joblib

app = Flask(__name__)
model = joblib.load(open('model.pkl', 'rb'))


@app.route("/", methods=['POST'])
def predict():
    prediction = []
    if request.method == 'POST':
        read_ss = int(request.values.get('read_ss'))
        ever_alternative = int(request.values.get('ever_alternative'))
        gpa = float(request.values.get('gpa'))
        african_american = int(request.values.get('african_american')) 

        print(read_ss, ever_alternative, gpa, african_american)
        # create numpy array

        prediction = model.predict([[read_ss, ever_alternative, gpa, african_american]])
    
    prediction = list(prediction)
    answer = prediction[0]
    return str(answer)


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
