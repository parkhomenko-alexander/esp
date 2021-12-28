from app import app 
from models import Data
from datetime import datetime
import render_template

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

@app.route('/show_chart', methods=['GET'])
def show_chart():
    render_template('index.html')
    return('q')