from wtforms import Form, ValidationError, fields, validators

from .constants import PASSWORD_FIELD_LENGTH, STRING_FIELD_LENGTH, TaskStatus
from .models import User


class UniqueEmailValidator:
    def __init__(self, message=None) -> None:
        self.message = message or "Field must be unique."

    def __call__(self, _form, field) -> None:
        data = User.select(User.email).where(User.email == field.data).limit(1)

        if data:
            raise ValidationError(self.message)


class UserForm(Form):
    email = fields.EmailField(
        label="E-mail",
        validators=[
            UniqueEmailValidator(),
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


class TaskForm(Form):
    title = fields.StringField(
        label="Title",
        validators=[
            validators.Length(**STRING_FIELD_LENGTH),
            validators.DataRequired(),
        ],
    )
    description = fields.TextAreaField(label="Description")
    status = fields.SelectField(
        label="Status",
        choices=[(status, status.name) for status in TaskStatus],
    )
