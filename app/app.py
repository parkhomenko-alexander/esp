from flask import Flask
from config import Configuration
from db import db 
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from blueprints.data_manipulator.data_manipulator_bp import data_manipulator_bp
from blueprints.micro_scheme.micro_scheme_bp import micro_scheme_bp
from blueprints.user.user_bp import user_bp
from blueprints.redirect.redirect_bp import redirect_bp


app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(redirect_bp)
app.register_blueprint(data_manipulator_bp, url_prefix='/data_manipulator')
app.register_blueprint(micro_scheme_bp, url_prefix='/micro_scheme')
app.register_blueprint(user_bp, url_prefix='/user')




