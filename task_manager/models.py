import json
import os
from datetime import datetime

from dotenv import load_dotenv
from peewee import BooleanField, CharField, DateTimeField, Model, SqliteDatabase
from playhouse.shortcuts import model_to_dict

load_dotenv()
db = SqliteDatabase(os.environ["DATABASE_URL"])


def model_to_json(model: Model) -> dict:
    _model = json.dumps(model_to_dict(model), sort_keys=True, default=str)
    return json.loads(_model)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=512)
    is_admin = BooleanField(default=False)
    register_datetime = DateTimeField(default=datetime.utcnow())
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
