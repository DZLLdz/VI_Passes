from flask import Blueprint, render_template, jsonify, request
from models import db, Users, Passes, Images, Coords, LevelEnum, PassesSchema, UserSchema
import requests

main = Blueprint('main', __name__)

passes_schema = PassesSchema(many=True)
pass_schema = PassesSchema()


@main.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})


@main.route('/')
def index():
    return "Hello, World!"


@main.route('/users')
def list_users():
    users = Users.query.all()
    return render_template('users.html', users=users)


@main.route('/sendData')
def send_data():
    url = 'http://127.0.0.1:5000/submitData'
    # image1 = Images.create_img()
    # image2 = Images.create_img()

    data = {
        "data": {
            "users_id": "2",
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
    response = requests.post(url, json=data)
    return response.json(), response.status_code


@main.route('/submitData', methods=['POST'])
def submit_data():
    try:
        # Получение данных из запроса
        data_value = request.json.get('data')
        # Проверка на наличие данных
        if not data_value:
            return jsonify({'error': 'No data provided'}), 400
        else:
            print(f"Data Recived")
        # Преобразование данных
        user_id = data_value.get('users_id')

        coord_id = data_value.get('coords_id')

        # images = data_value.get('images')

        beauty_title = data_value.get('beautyTitle')
        title = data_value.get('title')
        other_titles = data_value.get('other_titles')
        connect = data_value.get('connect')
        level_values = data_value.get('level')
        level_winter = level_values.get('winter')
        if level_winter == "" or level_winter is None:
            level_winter = LevelEnum.z1
        level_spring = level_values.get('spring')
        if level_spring == "" or level_spring is None:
            level_spring = LevelEnum.z1
        level_summer = level_values.get('summer')
        if level_summer == "" or level_summer is None:
            level_summer = LevelEnum.z1
        level_autumn = level_values.get('autumn')
        if level_autumn == "" or level_autumn is None:
            level_autumn = LevelEnum.z1
        # Создание нового объекта Passes
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
        # Добавление в сессию и сохранение в базе данных
        db.session.add(new_passes)
        # db.session.flush()

        db.session.commit()

        return jsonify({'message': 'Data submitted successfully', 'data_id': new_passes.id}), 201

    except Exception as e:
        # Обработка ошибок
        return jsonify({'error': str(e)}), 500


@main.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id)
    if user:
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify({'erorr': 'User not found'}), 404


@main.route('/user/all', methods=['GET'])
def get_all_user():
    users = Users.query.all()
    if users:
        users_schema = UserSchema(many=True)
        return jsonify(users_schema.dump(users)), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@main.route('/submitData/<int:id>', methods=['GET'])
def get_passes_data(id):
    try:
        passes = db.session.get(Passes, id)
        if passes is not None:
            return jsonify({'message': 'Data submitted successfully',
                            'data': pass_schema.dump(passes)})
        else:
            return jsonify({'message': f"Object with ID:{id} not founded!"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/submitData/all', methods=['GET'])
def get_all_passes_data():
    try:
        passes = Passes.query.all()
        if passes is not None:
            return jsonify(passes_schema.dump(passes))
        else:
            return jsonify({'message': f"Data is clear!"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/submitData/<int:id>', methods=['PATCH'])
def update_data(id):
    session = db.session
    data_get = session.get(Passes, id)
    pass_schema = PassesSchema()
    data_entry = pass_schema.dump(data_get)
    status = data_entry.get('status')

    if not data_entry:
        return jsonify({'state': 0, 'error': 'Entry not found'}), 404

    if status != 'NEW':
        return jsonify({'state': 0, 'error': 'Only entries with status "NEW" can be edited'}), 400

    new_data = request.json

    if not new_data:
        return jsonify({'state': 0, 'erorr': 'No data provided'}), 400

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
        return jsonify({'state': 0, 'message': e }), 500

    try:
        db.session.commit()
        return jsonify({'state': 1, 'message': 'Data updated successfully', 'id': id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'state': 0, 'message': e }), 500


@main.route('/submitData/', methods=['GET'])
def get_user_data_by_email():
    email = request.args.get('user__email')
    print(f'New get_user_data_by_email {email}')
    if not email:
        return jsonify({'state': 0, 'message': 'Email parameter is missing'}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({'state': 0, 'message': 'User not found'}), 404

    passes_entries = Passes.query.filter_by(users_id=user.id).all()
    # passes_schema = PassesSchema(many=True)
    passes_json = passes_schema.dump(passes_entries)

    return jsonify({'state': 1, 'data': passes_json})
