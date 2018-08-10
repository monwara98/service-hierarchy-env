from flask import Flask
from service_hierarchy.views.index import bp as index_bp

try:
    app = Flask(__name__)
except Exception as e:
    app = None

if app != None:    
    
    try:
        app.register_blueprint(index_bp)
    except Exception as e:
        print("error registering the app")
        
    try:       
        app.config.from_object(__name__)
    except Exception as e:
        print("error configuring the app")
        
    try:    
        app.config['SECRET_KEY'] = 'secret'
    except Exception as e:
        print("error configuring the secret key")