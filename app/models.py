from db import db
from datetime import timedelta
from flask_login import UserMixin
import sys
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class Data(db.Model):

    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    co_2 = db.Column(db.Integer)
    t_voc = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<data id: {self.id}, co_2: {self.co_2}, t_voc: {self.t_voc}, time: {self.time}>'

    def __lt__(self, other):
        return self.co_2 < other.co_2

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return 0

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    pas = db.Column(db.String(256), nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.pas = generate_password_hash(kwargs['pas'])

    def __repr__(self):
        return '<User id: {}, login: {}, pas: {}>'.format(self.id, self.login, self.pas)

    @staticmethod
    def is_equal_passwords(pas1: str, pas2: str):
        return pas1 == pas2 and pas1 != ''

    @staticmethod
    def is_exist_user(login: str):
        return len(db.session.query(User).filter(User.login==login).all()) == 1

    @staticmethod
    def is_matching_pattern(login: str):
        res = re.match(r'\w{5,20}', login)
        return res != None and len(login) <= 20 and len(login) >= 5

    @staticmethod
    def error_handling_register(dict_arguments, *args, **kwargs):
        
        if not User.is_matching_pattern(kwargs['login']):
            dict_arguments['error'] = 'Логин должен содержать символы a-zA-Z0-9, иметь длину от 5 до 20 символов'
            return dict_arguments

        if User.is_exist_user(kwargs['login']):
            dict_arguments['error'] = 'Логин занят'
            return dict_arguments

        if not User.is_equal_passwords(kwargs['pas'], kwargs['pas2']):
            dict_arguments['error'] = 'Пароли не совпадают или не заполнены'
            return dict_arguments
        
        return dict_arguments


    @staticmethod
    def error_handling_login(dict_arguments, *args, **kwargs):
        
        if not User.is_exist_user(kwargs['login']):
            dict_arguments['error'] = 'Пользователь не зарегестрирован'
            return dict_arguments 
    
        if 'pas' == '' or not User.authenticate(kwargs['login'], kwargs['pas']):
            dict_arguments['error'] = 'Неправильный пароль'
            return dict_arguments
        
        return dict_arguments


    @staticmethod
    def authenticate(login, pas):
        user = User.query.filter(User.login == login).first()
        if check_password_hash(user.pas, pas):
            return user
        else:
            return None

    def get_access_token(self):
        token = create_access_token(identity=self.login)
        return token


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return 'User successfully added ' + self.login
