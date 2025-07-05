from flask import Flask
from flask_login import LoginManager
from app.extensions import init_extensions, mongo
from bson import ObjectId
from app.webhook.auth import User  # ⚠️ make sure this doesn't cause a circular import
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500"])
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/database'
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    # app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS
    app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS

    init_extensions(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None

    # Blueprints
    from app.webhook.routes import webhook
    from app.webhook.auth import auth
    app.register_blueprint(webhook)
    app.register_blueprint(auth)

    return app
