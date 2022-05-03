from flask import Blueprint, render_template, url_for, request, make_response, redirect
from models import User
from flask_jwt_extended import set_access_cookies

user_bp = Blueprint('user_bp', 
                    __name__,  
                    template_folder='templates/', 
                    static_folder='static/')


@user_bp.route('/', methods=['GET'])
def index():
    return render_template('user/index.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    dict_arguments = {'title': 'Вход', 'button_title': 'Войти', 'action': url_for('.login')}
    
    if request.method == 'GET':
        return render_template('user/login.html', dict_arguments=dict_arguments)
    else:
        user_data = request.form.to_dict()
        print(dict_arguments)

        dict_arguments = User.error_handling_login(dict_arguments=dict_arguments, **user_data)
        print(dict_arguments)
        if 'error' in dict_arguments:
            return render_template('user/login.html', dict_arguments=dict_arguments)
        else:
            user = User(**user_data)
            response = make_response(redirect(url_for('data_manipulator_bp.index')))
            set_access_cookies(response, user.get_access_token())
            print(response)
            return response
    

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    dict_arguments = {'title': 'Регистрация', 'button_title': 'Зарегестрироваться', 'action': url_for('.register')}
    if request.method == 'GET':
        return render_template('user/register.html', dict_arguments=dict_arguments)
    else:
        form_args = request.form.to_dict()
        dict_arguments = User.error_handling_register(dict_arguments=dict_arguments, **form_args)

        if 'error' in dict_arguments:
            return render_template('user/register.html', dict_arguments=dict_arguments)
        else:
            user_data = request.form.to_dict()
            user_data.pop('pas2', None)
            user = User(**user_data)
            user.save_to_db()
            return redirect(url_for('.login'))
