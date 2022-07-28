import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from peewee_migrate import Router

from .models import BaseModel, db
from task_manager.migrator import SqlMigrator

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["DATABASE_URL"] = os.environ["DATABASE_URL"]
app.config["ENV"] = os.environ["ENV"]

# db.connect()
# db.create_tables(BaseModel.__subclasses__())
migrator = SqlMigrator(db)

api = Api(app, "/api")
router = Router(db)
