from app import app, db
from models import Data
from datetime import datetime
from flask import render_template, session, make_response
from sqlalchemy.orm import sessionmaker

@app.route('/request/<int:co_2>/<int:t_voc>', methods=['GET'])
def request_data(co_2, t_voc):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_data = Data(co_2=co_2, t_voc=t_voc, time=time)
    requested_data.save_to_db()
    print(requested_data)
    return('da')

@app.route('/', methods=['GET'])
def index():
    return('q')

@app.route('/show_chart_co', methods=['GET'])
def show_chart_co():
    return render_template('co.html')

@app.route('/show_chart_tvoc', methods=['GET'])
def show_chart_tvoc():
    return render_template('tvoc.html')

@app.route('/get_data_co/<arr_length>', methods=['GET'])
def get_data_co(arr_length):    
    data = db.session.query(Data).order_by(Data.id.desc()).first()
    response_data = f'[[{int(arr_length) + 1},{data.co_2}]]'
    
    response = make_response(response_data, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/get_data_tvoc/<arr_length>', methods=['GET'])
def get_data_tvoc(arr_length):    
    data = db.session.query(Data).order_by(Data.id.desc()).first()
    response_data = f'[[{int(arr_length) + 1},{data.tvoc}]]'
    
    response = make_response(response_data, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    