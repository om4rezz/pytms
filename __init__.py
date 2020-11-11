from flask import Flask
from .views import api
from .extensions import db


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pent3ster@192.168.1.3/pytms'

    db.init_app(app)

    app.register_blueprint(api)

    return app
