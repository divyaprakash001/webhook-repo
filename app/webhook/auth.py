from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import mongo
from bson import ObjectId

auth = Blueprint('auth', __name__, url_prefix='/auth')

# user class for flask-login
class User(UserMixin):
    def __init__(self, user_data):
      self.id = str(user_data['_id'])
      self.username = user_data['username']

    def get_id(self):
      return self.id


# register endpoint
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if mongo.db.users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password
    })

    return jsonify({'message': 'Registration successful'}), 201



# login endpoint
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # user if user already exists
    user_data = mongo.db.users.find_one({'username': username})

    # checking the password and if not giving invalid response
    if not user_data or not check_password_hash(user_data['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # user for flask-login
    user = User(user_data)

    # log the user in and create session
    login_user(user)
    
    return jsonify({'message': 'Login successful','user':current_user.username}), 200




# logout endpoint
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200




@auth.route('/me')
def me():
    if current_user.is_authenticated:
        return jsonify({'username': current_user.username}), 200
    return jsonify({'error': 'Unauthorized'}), 401