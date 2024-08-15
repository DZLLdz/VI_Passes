from flask import Blueprint, render_template, jsonify, request
from models import db, User, Passes, Images, Coords, LevelEnum, PassesSchema
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
    users = User.query.all()
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


@main.route('/submitData/<int:id>', methods=['GET'])
def get_passes_data(id):
    try:
        passes = Passes.query.get(id)
        if passes is not None:
            return jsonify(pass_schema.dump(passes))
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