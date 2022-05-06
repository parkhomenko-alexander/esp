from datetime import timedelta

class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'wadqwqwrqvwteltw[wr[qq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db:3306/esp_data'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/esp_data'
    STATIC_FOLDER = 'static'
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_CSRF_PROTECT = False
    #/ JWT_ACCESS_COOKIE_PATH = ['/data_manipulator/', '/user/']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1000)