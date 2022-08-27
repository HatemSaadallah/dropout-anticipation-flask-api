from flask import Flask, request, render_template, redirect, url_for
import joblib
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = joblib.load(open('model.pkl', 'rb'))


@app.route("/", methods=['POST'])
def predict():
    prediction = []
    errors = []
    if request.method == 'POST':
        try:
            read_ss = int(request.values.get('read_ss'))
            ever_alternative = int(request.values.get('ever_alternative'))
            gpa = float(request.values.get('gpa'))
            african_american = int(request.values.get('african_american')) 

            print(read_ss, ever_alternative, gpa, african_american)
            # create numpy array
            if read_ss < 0 or read_ss > 100:
                errors.append('read_ss must be between 0 and 100')
            if ever_alternative < 0 or ever_alternative > 1:
                errors.append('ever_alternative must be between 0 and 1')
            if gpa < 0 or gpa > 4:
                errors.append('gpa must be between 0 and 4')

            if african_american != 0:
                african_american = 1

            prediction = model.predict([[read_ss, ever_alternative, gpa, african_american]])
        
        except:
            return {'error': 'Invalid input'};
        
    prediction = list(prediction)
    answer = prediction[0]
    if len(errors) > 0:
        # return {'status': 400, 'errors': errors}
        return {'status': 400, 'errors': errors}    
    return {'status': 200, 'answer': str(answer)}


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
