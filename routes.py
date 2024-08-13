from flask import Blueprint, render_template, jsonify, request
from models import User

main = Blueprint('main', __name__)

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
