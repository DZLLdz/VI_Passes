from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields as ma_fields
from models import Users, Passes


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True


class PassesSchema(SQLAlchemyAutoSchema):
    user = ma_fields.List(ma_fields.Nested(UserSchema, many=True))

    class Meta:
        model = Passes
        include_relationships = True
        load_instance = True
