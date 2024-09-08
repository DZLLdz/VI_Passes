from flask_restx import fields, Namespace
from flask import Blueprint


main = Blueprint('main', __name__)
api = Namespace('swagger_models', description="Swagger Models")

user_roles_model = api.model('UserRoles', {
    'role': fields.String(description='Роль пользователя', enum=['admin', 'editor', 'tourist'])
})

status_enum_model = api.model('StatusEnum', {
    'status': fields.String(description='Статус заявки', enum=[
        'New', 'pending', 'accepted', 'rejected'
    ])
})

activities_types_model = api.model('ActivityTypes', {
    'atype': fields.String(description='Тип активности', enum=[
        'пешком', 'лыжи', 'катамаран', 'байдарка', 'плот', 'сплав',
        'велосипед', 'автомобиль', 'мотоцикл', 'парус', 'верхом'
    ])
})

level_enum_model = api.model('LevelEnum', {
    'level': fields.String(description='Уровень сложности', enum=[
        'Определяется', '1A', '1B', '2A', '2B', '3A', '3B'
    ])
})

user_model = api.model('Users', {
    'id': fields.Integer(description='ID пользователя'),
    'username': fields.String(description='Имя пользователя', required=True),
    'email': fields.String(description='Email пользователя', required=True),
    'role': fields.Nested(user_roles_model, description='Роль пользователя'),
    'atype': fields.Nested(activities_types_model, description='Тип активности пользователя'),
    'passes': fields.List(fields.Integer, description='ID маршрутов, связанных с пользователем')
})


level_model = api.model('Level', {
    'winter': fields.Nested(level_enum_model, description='Уровень зимой'),
    'spring': fields.Nested(level_enum_model, description='Уровень весной'),
    'summer': fields.Nested(level_enum_model, description='Уровень летом'),
    'autumn': fields.Nested(level_enum_model, description='Уровень осенью')
})

passes_model_old = api.model('PassesOld', {
    'id': fields.Integer(description='ID прохода'),
    'title': fields.String(description='Название перевала'),
    'beautyTitle': fields.String(description='Красивое название'),
    'level': fields.Nested(level_model, description='Уровни сложности'),
})

passes_model = api.model('PassesNew', {
    'id': fields.Integer(description='ID перевала'),
    'beautyTitle': fields.String(description='Красивое название'),
    'title': fields.String(description='Название перевала'),
    'other_titles': fields.String(description='Другие названия'),
    'connect': fields.List(fields.Integer, description='Связанные объекты'),
    'add_time': fields.DateTime(description='Дата добавления'),
    'level_winter': fields.Nested(level_enum_model, description='Уровень сложности зимой'),
    'level_spring': fields.Nested(level_enum_model, description='Уровень сложности весной'),
    'level_summer': fields.Nested(level_enum_model, description='Уровень сложности летом'),
    'level_autumn': fields.Nested(level_enum_model, description='Уровень сложности осенью'),
    'status': fields.Nested(status_enum_model, description='Статус заявки'),
    'users_id': fields.Integer(description='ID пользователя'),
    'coords_id': fields.Integer(description='ID координат'),
    'images': fields.List(fields.Integer, description='Связанные изображения')
})

new_pass_response_model = api.model('NewPassResponse', {
    'message': fields.String(description='Сообщение о результате'),
    'data_id': fields.Integer(description='ID нового перевала')
})

coords_model = api.model('Coords', {
    'id': fields.Integer(description='ID координат'),
    'latitude': fields.Float(description='Широта', required=True),
    'longitude': fields.Float(description='Долгота', required=True),
    'height': fields.Integer(description='Высота')
})

images_model = api.model('Images', {
    'id': fields.Integer(description='ID изображения'),
    'pass_id': fields.Integer(description='ID перевала')
})

