import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from .views import API_VIEWS

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["DATABASE_URL"] = os.environ["DATABASE_URL"]
app.config["ENV"] = os.environ["ENV"]


api = Api(app, "/api")

for endpoint, resource in API_VIEWS.items():
    api.add_resource(resource, endpoint)
