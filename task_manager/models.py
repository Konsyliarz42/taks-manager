import json
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from peewee import BooleanField
from peewee import CharField as _CharField
from peewee import (
    DateTimeField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
    TextField,
)
from playhouse.shortcuts import model_to_dict

from .constants import PASSWORD_FIELD_LENGTH, STRING_FIELD_LENGTH, TaskStatus

load_dotenv()

if os.environ["ENV"] == "production":
    db = PostgresqlDatabase(os.environ["DATABASE_URL"])
else:
    db = SqliteDatabase(os.environ["DATABASE_URL"])

# ================================================================


def model_to_json(model: Model) -> dict:
    _model = json.dumps(model_to_dict(model), sort_keys=True, default=str)
    return json.loads(_model)


class BaseModel(Model):
    class Meta:
        database = db


class CharField(_CharField):
    def __init__(self, *args, max_length: Optional[int] = None, **kwargs):
        max_length = max_length or STRING_FIELD_LENGTH["max"]
        super().__init__(max_length, *args, **kwargs)


# ================================================================


class User(BaseModel):
    email = CharField(unique=True)
    password = CharField(max_length=PASSWORD_FIELD_LENGTH["max"])
    first_name = CharField()
    last_name = CharField()

    is_admin = BooleanField(default=False)
    registered_at = DateTimeField(default=datetime.utcnow())


class Task(BaseModel):
    title = CharField()
    description = TextField(null=True)
    status = CharField(default=TaskStatus.TO_DO.value)

    created_at = DateTimeField(default=datetime.utcnow())
    owner = ForeignKeyField(User, backref="tasks")
