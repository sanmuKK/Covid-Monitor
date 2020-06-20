from flask import Flask
from flask_cors import CORS
from ncovapi import ncov
from user import user
from comment import comment


def creat_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:l.1322630122@localhost:3306/first_flask?charset=utf8'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'False'
    app.secret_key='pleasedonthitme'
    app.config['MAIL_SERVER'] = 'smtp.sina.com'
    app.config['MAIL_USERNAME'] = '18965600766ljl@sina.com'
    app.config['MAIL_PASSWORD'] = '7a2edb3ffc16c18f'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    #cors = CORS(app,supports_credentials=True)
    cors = CORS(app, resources={r"/.*": {"origins": "http://localhost:8081"}},supports_credentials=True)
    app.register_blueprint(ncov)
    app.register_blueprint(user)
    app.register_blueprint(comment)
    return app