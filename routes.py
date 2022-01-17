from app import app, db
from models import Data
from datetime import datetime,timedelta
from flask import render_template, session, make_response, request
from sqlalchemy.orm import sessionmaker

@app.route('/request/<int:co_2>/<int:t_voc>', methods=['GET'])
def request_data(co_2, t_voc):
    time = datetime.now()
    hour_add = timedelta(hours=10)
    cur_with_timezone = (time + hour_add).strftime("%Y-%m-%d %H:%M:%S")
    requested_data = Data(co_2=co_2, t_voc=t_voc, time=cur_with_timezone)
    requested_data.save_to_db()
    print(requested_data)
    return('da')

@app.route('/', methods=['GET'])
def index():
     return render_template('header.html')

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
    response_data = f'[[{int(arr_length) + 1},{data.t_voc}]]'
    
    response = make_response(response_data, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/get_data_charts', methods=['GET'])
def get_data_charts():    
    chart_type = request.args.get('chart_type')
    start = request.args.get('time_line_start')
    end = request.args.get('time_line_end')
    print(start)

    print(start)

    #!
    from engine import engine
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Data).filter(Data.time.between(start,end)).all()
    print(res)

    #!

    if chart_type == 'none':
        response = make_response({},200)
    elif chart_type == 'co':

        response = make_response({'co':'true'}, 200)
    else:
        response = make_response({'tvoc':'true'}, 200)
    
    return response
