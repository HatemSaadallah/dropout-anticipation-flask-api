from flask import Flask, request, render_template, redirect, url_for, make_response
import joblib
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = joblib.load(open('model.pkl', 'rb'))


@app.route("/", methods=['POST'])
def predict():
    prediction = []
    errors = []
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    data = request.get_data()
    data = json.loads(data)
    print(data)
    if request.method == 'POST':
        try:
            read_ss = int(data['read_ss'])
        except ValueError:
            response.status_code = 400
            response.data = json.dumps({"error": "read_ss is not a number"})
            return response
        try:
            ever_alternative = int(data['ever_alternative'])
        except ValueError:
            response.status_code = 400
            response.data = json.dumps({"error": "ever_alternative is not a number"})
            return response
        try:
            gpa = float(data['gpa'])
        except ValueError:
            response.status_code = 400
            response.data = json.dumps({"error": "gpa is not a number"})
            return response
        try:
            african_american = int(data['african_american'])
        except ValueError:
            response.status_code = 400
            response.data = json.dumps({"error": "african_american is not a number"})
            return response

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
        
    prediction = list(prediction)
    answer = prediction[0]
    if len(errors) > 0:
        # return {'status': 400, 'errors': errors}
        return {'status': 400, 'errors': errors}    
    return {'status': 200, 'answer': str(answer)}


# Running the app
if __name__ == '__main__':
    app.run(debug=True)
