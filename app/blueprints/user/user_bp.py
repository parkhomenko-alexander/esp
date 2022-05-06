from flask import Blueprint, render_template, url_for, request, make_response, redirect
from models import User
from flask_jwt_extended import set_access_cookies, unset_access_cookies, decode_token
from middleware.middleware import check_token



user_bp = Blueprint('user_bp', 
                    __name__,  
                    template_folder='templates/', 
                    static_folder='static/')


@user_bp.route('/', methods=['GET'])
def index():
    return render_template('user/index.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    dict_arguments = {'action': url_for('.login')}
    
    if request.method == 'GET':
        return render_template('user/login.html', dict_arguments=dict_arguments)
    else:
        user_data = request.form.to_dict()
        dict_arguments = User.error_handling_login(dict_arguments=dict_arguments, **user_data)
 
        if 'error' in dict_arguments:
            return render_template('user/login.html', dict_arguments=dict_arguments)
        else:
            user = User(**user_data)
            response = make_response(redirect(url_for('data_manipulator_bp.index')))
            # response = make_response(redirect(url_for('.person_area')))

            token = user.get_access_token()
            print(token)
            set_access_cookies(response, token)

            return response
    

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    dict_arguments = {'action': url_for('.register')}
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

@user_bp.route('/person-area', methods=['GET', 'POST'])
@check_token
def person_area():
    dict_arguments = {'action': url_for('.person_area')}
    token = request.cookies.get('access_token_cookie')
    token = decode_token(token, allow_expired=True)
    dict_arguments['sub'] = token['sub']
    normal_values = User.get_normal_values(dict_arguments['sub'])
    dict_arguments['co'] = normal_values[0]
    dict_arguments['tvoc'] = normal_values[1]
    if request.method == 'GET':
        return render_template('user/person-area.html', dict_arguments=dict_arguments)
    else:
        form_args = request.form.to_dict()
        if not form_args['co_normal'].isdigit() or  not form_args['tvoc_normal'].isdigit() or int(form_args['co_normal']) < 0 or int(form_args['co_normal'])  > 3000 or int(form_args['tvoc_normal']) < 0 or int(form_args['tvoc_normal']) > 3000:
            dict_arguments['error'] = 'Значения не менее 0 и не более 3000. Только цифры'
            print(dict_arguments)
            return render_template('user/person-area.html', dict_arguments=dict_arguments)
        else:
            dict_arguments['co'] = form_args['co_normal']
            dict_arguments['tvoc'] = form_args['tvoc_normal']
            User.change_normal_values(login=dict_arguments['sub'], co=form_args['co_normal'], tvoc=form_args['tvoc_normal'])
            return render_template('user/person-area.html', dict_arguments=dict_arguments)


@user_bp.route('/log-out', methods=['GET'])
@check_token
def log_out():
    response = make_response(redirect(url_for('user_bp.index')))
    unset_access_cookies(response)
    return response

@user_bp.route('/max-value', methods=['GET'])
def max_value():
    print()
    token = request.cookies.get('access_token_cookie')
    token = decode_token(token, allow_expired=True)
    normal_values = User.get_normal_values(token['sub'])
    response = make_response({'co': normal_values[0], 'tvoc': normal_values[1]}, 200)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response