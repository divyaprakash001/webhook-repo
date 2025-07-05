from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()

def init_extensions(app):
    
  CORS(app,
     supports_credentials=True,
     resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

  mongo.init_app(app)
