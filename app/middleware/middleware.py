from flask import make_response, request, url_for, redirect
from datetime import datetime, timedelta
from flask_jwt_extended import decode_token, unset_access_cookies
from functools import wraps



def check_token(f):
    @wraps(f)
    def verify_decorator(*args, **kwargs):
        token = request.cookies.get('access_token_cookie')
        print(request.cookies)
        if token == None:
            response = make_response(redirect(url_for('user_bp.login')))
            return response
        token = decode_token(token, allow_expired=True)
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), token['exp'])
        if datetime.now().timestamp() > token['exp']:

            response = make_response(redirect(url_for('user_bp.login')))
            unset_access_cookies(response)
            return response
        else:
            return f(*args, **kwargs)

    return verify_decorator