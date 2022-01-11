from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression
import pickle


app = Flask(__name__)

# collab에서 만들어서 pickle로 내보낸 모델 불러오기 
model = pickle.load(open('flask_app/movie.pkl', 'rb'))

# api url route별 화면 지정 
@app.route('/')
def index() : 
    return render_template('home.html'), 200 

@app.route('/predict', methods=['GET', 'POST'])
def home() : 
    data1 = request.form['a'] 
    data2 = request.form['b'] 

    # model에 넣고 예측할 때에 [[]]형태
    # predict 결과의 첫번째가 결과값이므로 첫번째만 가져옴
    pred = model.predict([[data1, data2]])[0] 

    # 순위예측이라 소수점 밑에 반올림 후 int로 변경 
    int_pred = int(pred.round(0)) 
    return render_template('after.html', data=int_pred)

