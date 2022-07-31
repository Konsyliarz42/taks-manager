"""
This file is extended version of validators from wtforms.
Please use this file instead of `wtforms.validators`.
I want to use one import to use validators in code.
"""
from peewee import DoesNotExist
from wtforms import ValidationError
from wtforms.validators import (    # noqa: F401 - imported but unused
    DataRequired,                   # If i set `*` instead of this,
    Email,                          # that mypy does see this in other modules.
    EqualTo,
    Length,
)

from .models import User


class UniqueEmail:
    def __init__(self, message=None) -> None:
        self.message = message or "Field must be unique."

    def __call__(self, _form, field) -> None:
        data = User.select(User.email).where(User.email == field.data).limit(1)

        if data:
            raise ValidationError(self.message)


class UserIsActive:
    def __init__(self, message=None) -> None:
        self.message = message or "User not found."

    def __call__(self, _form, field) -> None:
        if field.data is None:
            return

        try:
            user: User = User.get_by_id(field.data)
        except DoesNotExist as exc:
            raise ValidationError(self.message) from exc

        if not user.is_active:
            raise ValidationError(self.message)


class OldPasswordIsCorrect:
    def __init__(self, message=None) -> None:
        self.message = message or "Password not correct."

    def __call__(self, _form, field) -> None:
        # TODO: After add login mechanism, check password with current user
        pass


class NotEqualTo:
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError as exc:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
        if field.data != other.data:
            return

        other_field_name = {
            "other_label": hasattr(other, "label")
            and other.label.text
            or self.fieldname,
            "other_name": self.fieldname,
        }
        message = self.message
        if message is None:
            message = field.gettext("Field must be not equal to %(other_name)s.")

        raise ValidationError(message % other_field_name)
