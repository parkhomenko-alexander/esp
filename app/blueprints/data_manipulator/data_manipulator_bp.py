from flask import Blueprint, render_template, session, make_response, request, url_for, redirect
from models import Data, User, db
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import jwt_required, decode_token, unset_access_cookies
from functools import wraps


from inspect import signature



data_manipulator_bp = Blueprint('data_manipulator_bp', 
                                __name__,  
                                template_folder='templates',
                                static_folder='static')



def check_token(f):
    @wraps(f)
    def verify_decorator(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')
        token = decode_token(token, allow_expired=True)
        print(token)
        if datetime.now().timestamp() > token['exp']:
            response = make_response(redirect(url_for('user_bp.login')))
            unset_access_cookies(response)
            return response
        else:
            return f(*args, **kwargs)

    return verify_decorator

@data_manipulator_bp.route('/request_data', methods=['GET'])
def request_data():
    co_2 = request.args.get('co_2')
    t_voc =request.args.get('t_voc')
    time = datetime.now()
    hour_add = timedelta(hours=10)
    cur_with_timezone = (time + hour_add).strftime('%Y-%m-%d %H:%M:%S')
    requested_data = Data(co_2=co_2, t_voc=t_voc, time=cur_with_timezone)
    requested_data.save_to_db()
    print(requested_data)
    return('da')


@data_manipulator_bp.route('/', methods=['GET'])
@check_token
def index():
    return render_template('data_manipulator/header.html')


@data_manipulator_bp.route('/show_chart_co', methods=['GET'])
@check_token
def show_chart_co():
    return render_template('data_manipulator/co.html')

@data_manipulator_bp.route('/show_chart_tvoc', methods=['GET'])
@check_token
def show_chart_tvoc():
    return render_template('data_manipulator/tvoc.html')

@data_manipulator_bp.route('/get_data_co/<arr_length>', methods=['GET'])
def get_data_co(arr_length):    
    data = db.session.query(Data).order_by(Data.id.desc()).first()
    response_data = f'[[{int(arr_length) + 1},{data.co_2}]]'
    
    response = make_response(response_data, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@data_manipulator_bp.route('/get_data_tvoc/<arr_length>', methods=['GET'])
def get_data_tvoc(arr_length):    
    data = db.session.query(Data).order_by(Data.id.desc()).first()
    response_data = f'[[{int(arr_length) + 1},{data.t_voc}]]'
    
    response = make_response(response_data, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@data_manipulator_bp.route('/get_data_charts', methods=['GET'])
def get_data_charts():    
    chart_type = request.args.get('chart_type')
    start =request.args.get('time_line_start')
    end = request.args.get('time_line_end')
 
    # 
    # from engine import engine
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # res = session.query(Data).filter(Data.time.between(start,end)).all()
    # 


    if chart_type == 'none':
        response = make_response({},200)
    elif chart_type == 'co':
        res = db.session.query(Data).filter(Data.time.between(start,end)).all()

        max_elem = max(res).co_2
        min_elem = min(res).co_2

        for i in range(len(res)):
            res[i] = {'x': i, 'y': res[i].co_2} 

        response = make_response({'type':'CO 2',
                                'max_val':max_elem,
                                'min_val':min_elem,
                                'data_point': res}, 200, {"Access-Control-Allow-Origin": "*"})
    else:
        res = db.session.query(Data).filter(Data.time.between(start,end)).all()

        for i in range(len(res)):
            res[i] = res[i].t_voc

        max_elem = max(res)
        min_elem = min(res)

        for i in range(len(res)):
            res[i] = {'x': i, 'y': res[i]} 

        response = make_response({'type':'TVOC',
                                'max_val':max_elem,
                                'min_val':min_elem,
                                'data_point': res}, 200 , {"Access-Control-Allow-Origin": "*"})
    
    return response

@data_manipulator_bp.route('/get_data', methods=['GET'])
def get_data():
    start = request.args.get('time_line_start')
    end = request.args.get('time_line_end')
    
    # #!
    # from engine import engine
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # #!   print(res, max_elem, min_elem)

    res = db.session.query(Data).filter(Data.time.between(start, end)).all()
    for i in range(len(res)):
        res[i] = {'id': res[i].id, 
                   'co': res[i].co_2,
                   'tvoc': res[i].t_voc,
                   'time': res[i].time.strftime('%Y-%m-%d %H:%M:%S')} 
    print(res)
    return {'data': res}, 200, {"Access-Control-Allow-Origin": "*"}

@data_manipulator_bp.route('/delete_data', methods=['POST'])
@jwt_required()
@check_token
def delete_data():
    items_to_remove = request.form.get('removeItems').split(',')
    print(items_to_remove)
    response = make_response({}, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(request.cookies)
    # from engine import engine
    # Session = sessionmaker(bind=engine)
    # session = Session()

    for item in items_to_remove:
        res = db.session.query(Data).filter(Data.id == item).first()
        db.session.delete(res)
    
    db.session.commit()

    return response, 200


