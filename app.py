import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

from config import inicializa_swagger
from db import db_session, init_db

from routes import inicializa_rotas

app = Flask(__name__)
api = Api(app)

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

mail = Mail(app)

swagger = inicializa_swagger(app=app)


if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

inicializa_rotas(api=api)


@app.teardown_request
def checkin_db(exc):
    try:
        db_session.remove()
    except:
        pass


@app.before_first_request
def first_request():
    init_db(bcrypt=bcrypt)


if __name__ == "__main__":
    app.run()
