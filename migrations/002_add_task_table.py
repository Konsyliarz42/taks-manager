"""Peewee migrations -- 002_add_task_table.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw

from task_manager.constants import TaskStatus


SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class Task(pw.Model):
        id = pw.AutoField()
        title = pw.CharField()
        description = pw.TextField()
        status = pw.CharField(constraints=[SQL("DEFAULT 'To Do'")], default=TaskStatus.TO_DO.value)
        created_at = pw.DateTimeField(constraints=[SQL("DEFAULT (datetime('now','utc'))")], default=dt.datetime.utcnow())
        owner = pw.ForeignKeyField(backref='tasks', column_name='owner', field='id', model=migrator.orm['user'])

        class Meta:
            table_name = "task"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('task')

    migrator.remove_model('basemodel')
