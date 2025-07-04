from flask import Flask
from app.extensions import init_extensions
from app.webhook.routes import webhook


# Creating our flask app
def create_app():

    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/database' 
    
    # linking database
    init_extensions(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
