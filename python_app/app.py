from flask import Flask
from views.index import bp as index_bp

app = Flask(__name__)
app.register_blueprint(index_bp)

if __name__ == '__main__':
    try:
        app.run(port=9999, debug=True) # changed port as 5000 was not working
    except OSError as o:
        print("there is an OSError - consider changing ports.")
    except Exception as e:
        print("there is an exception.")

# don't need this if using a view
# @app.route('/') 

# def home():
#     return "Hi there!"