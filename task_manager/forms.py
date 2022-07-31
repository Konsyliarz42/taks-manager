from wtforms import Form, fields

from . import form_validators as validators
from .constants import PASSWORD_FIELD_LENGTH, STRING_FIELD_LENGTH, TaskStatus


class AddUserForm(Form):
    email = fields.EmailField(
        label="E-mail",
        validators=[
            validators.UniqueEmail(),
            validators.Email(),
            validators.Length(**STRING_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )
    password = fields.PasswordField(
        label="Password",
        validators=[
            validators.Length(**PASSWORD_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )
    confirm_password = fields.PasswordField(
        label="Confirm Password",
        validators=[
            validators.EqualTo("password"),
            validators.DataRequired(),
        ],
    )
    first_name = fields.StringField(
        label="First Name",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )
    last_name = fields.StringField(
        label="Last Name",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )


class UpdateUserForm(Form):
    email = fields.EmailField(
        label="E-mail",
        validators=[
            validators.UniqueEmail(),
            validators.Email(),
            validators.Length(**STRING_FIELD_LENGTH),
        ],
    )
    old_password = fields.PasswordField(
        label="Old Password",
        validators=[
            validators.OldPasswordIsCorrect(),
            validators.Length(**PASSWORD_FIELD_LENGTH),
        ],
    )
    password = fields.PasswordField(
        label="Password",
        validators=[
            validators.Length(**PASSWORD_FIELD_LENGTH),
        ],
    )
    confirm_password = fields.PasswordField(
        label="Confirm Password",
        validators=[
            validators.EqualTo("password"),
        ],
    )
    first_name = fields.StringField(
        label="First Name",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
        ],
    )
    last_name = fields.StringField(
        label="Last Name",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
        ],
    )


# ================================================================


class AddTaskForm(Form):
    title = fields.StringField(
        label="Title",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )
    description = fields.TextAreaField(label="Description")
    assigned = fields.IntegerField(
        label="Assigned", validators=[validators.UserIsActive()]
    )


class UpdateTaskForm(Form):
    title = fields.StringField(
        label="Title",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
        ],
    )
    description = fields.TextAreaField(label="Description")
    status = fields.SelectField(
        label="Status",
        choices=[(status, status.name) for status in TaskStatus],
    )
    assigned = fields.IntegerField(
        label="Assigned", validators=[validators.UserIsActive()]
    )
