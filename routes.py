import requests
import logging
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request
from flask_restx import Namespace, Resource
from models import db, Users, Passes, Images, Coords, LevelEnum
from schems import PassesSchema, UserSchema
from swagger_models import user_model, passes_model_old, passes_model, new_pass_response_model, coords_model, images_model

api = Namespace('Routes', description="Возможные маршруты")


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return jsonify({"message": "Hello, World!"})


@api.route('/users/<int:id>')
class UserResource(Resource):
    @api.doc(description="Get jSON User on ID")
    @api.response(200, 'Success', user_model)
    @api.response(404, 'User not found', user_model)
    @api.response(500, 'Server Error')
    def get(self, id):
        try:
            if id == 0:
                users = Users.query.all()
                if users:
                    users_schema = UserSchema(many=True)
                    result = users_schema.dump(users)
                    return result, 200
            elif id > 0:
                user = Users.query.get(id)
                if user:
                    user_schema = UserSchema()
                    result = user_schema.dump(user)
                    return result, 200
            else:
                return {'erorr': 'User not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/sendData')
class SendData(Resource):
    @api.doc(description="Отправляет в старой форме на сервере", )
    @api.response(200, 'Success', passes_model_old)
    @api.response(400, 'Bad Request')
    def get(self):
        url = 'http://127.0.0.1:5000/api/sendData'
        data = {
            "data": {
                "users_id": "1",
                "coords_id": "1",
                "images": [],
                "beautyTitle": "пер.",
                "title": "Title1",
                "other_titles": "Title2",
                "connect": [],
                "level": {
                    "winter": "threeA",
                    "spring": "oneB",
                    "summer": "twoA",
                    "autumn": "z1"
                }
            }
        }
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return {"error": "Invalid JSON received"}, 500
        else:
            return {"error": f"Request failed with status code {response.status_code}"}, 400

    @api.doc(description="Принимает данные в старой форме, преобразует в новую и сохраняет", )
    @api.response(200, 'Success', new_pass_response_model)
    @api.response(400, 'Bad Request')
    @api.response(500, 'Server Error')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            else:
                print(f'получена:{data}')
            data_value = data.get('data')
            user_id = data_value.get('users_id')
            coord_id = data_value.get('coords_id')
            # images = data_value.get('images')
            beauty_title = data_value.get('beautyTitle')
            title = data_value.get('title')
            other_titles = data_value.get('other_titles')
            connect = data_value.get('connect')
            level_values = data_value.get('level')
            level_winter = level_values.get('winter', LevelEnum.z1)
            level_spring = level_values.get('spring', LevelEnum.z1)
            level_summer = level_values.get('summer', LevelEnum.z1)
            level_autumn = level_values.get('autumn', LevelEnum.z1)

            new_passes = Passes(users_id=user_id,
                                coords_id=coord_id,
                                beautyTitle=beauty_title,
                                title=title,
                                other_titles=other_titles,
                                connect=connect,
                                level_winter=level_winter,
                                level_spring=level_spring,
                                level_summer=level_summer,
                                level_autumn=level_autumn)
            print(new_passes)
            # Добавление в сессию и сохранение в базе данных
            db.session.add(new_passes)
            print("--1--")
            # db.session.flush()
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                logging.error(f"Error committing transaction: {e}")
            print("--2--")
            response_data = {
                'message': 'Data submitted successfully',
                'data_id': new_passes.id
            }
            print("---3---")
            print(new_passes)
            return jsonify(response_data), 200

        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/submitData/<int:id>')
class PassResource(Resource):
    @api.doc(description="Получение данных перевале по ID")
    @api.response(200, 'Success', passes_model)
    @api.response(404, 'Pass not found', passes_model)
    @api.response(500, 'Server Error')
    def get(self, id):
        try:
            if id == 0:
                passes = Passes.query.all()
                if passes is not None:
                    passes_schema = PassesSchema(many=True)
                    result = passes_schema.dump(passes)
                    return result
                else:
                    return {'message': f"Data is clear!"}
            elif id > 0:
                passes = db.session.get(Passes, id)
                if passes is not None:
                    pass_schema = PassesSchema()
                    result = pass_schema.dump(passes)
                    return {'message': 'Data submitted successfully',
                            'data': result}
                else:
                    return {'message': f"Object with ID:{id} not founded!"}

        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc(description="Изменение данных об одном перевале по ID c учетом изменений формы записи")
    @api.response(200, 'Success', passes_model)
    @api.response(404, 'Entry Data not found', passes_model_old)
    @api.response(547, 'Status not NEW', passes_model)
    @api.response(500, 'Server Error')
    def patch(self, id):
        session = db.session
        data_get = session.get(Passes, id)
        pass_schema = PassesSchema()
        data_entry = pass_schema.dump(data_get)
        status = data_entry.get('status')

        if not data_entry:
            return {'state': 0, 'error': 'Entry not found'}, 404

        if status != 'NEW':
            return {'state': 0, 'error': 'Only entries with status "NEW" can be edited'}, 547

        new_data = request.json

        if not new_data:
            return {'state': 0, 'erorr': 'No data provided'}, 404

        try:
            data_to_update = new_data.get('data')
            level_to_update = data_to_update.get('level')
            fields_in_new = ["beautyTitle", "connect", "other_titles", "title", 'level']
            level_in_update = ["autumn", "spring", "summer", "winter"]
            # fields_to_update = ["beautyTitle", "connect", "other_titles", "title",
            #                     "level_autumn", "level_spring", "level_summer", "level_winter",]
            valid_levels = {'z1', 'oneA', 'oneB', 'twoA', 'twoB', 'threeA', 'threeB'}
            for field in fields_in_new:
                if field != 'level':
                    setattr(data_get, field, data_to_update[field])
                else:
                    for level in level_in_update:
                        change_attribute = f'level_{level}'
                        if new_data['data']['level'][f'{level}'] in valid_levels:
                            setattr(data_get, change_attribute, level_to_update[level])
                        else:
                            setattr(data_get, change_attribute, 'z1')

        except Exception as e:
            return {'state': 0, 'message': str(e)}, 500

        try:
            db.session.commit()
            return {'state': 1, 'message': 'Data updated successfully', 'id': id}, 200
        except Exception as e:
            db.session.rollback()
            return {'state': 0, 'message': str(e)}, 500


@api.route('/passes/<string:email>')
class PassesForMail(Resource):
    @api.doc(description="Получение списка перевалов по USEREMAIL")
    @api.response(200, 'Success', passes_model)
    @api.response(400, 'Email not get')
    @api.response(404, 'User not Found', user_model)
    def get(self, email):
        print(f'New get_user_data_by_email {email}')
        if not email:
            return jsonify({'state': 0, 'message': 'Email parameter is missing'}), 400

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'state': 0, 'message': 'User not found'}, 404

        passes_entries = Passes.query.filter_by(users_id=user.id).all()
        passes_schema = PassesSchema(many=True)
        passes_json = passes_schema.dump(passes_entries)

        return {'state': 1, 'data': passes_json}, 200
