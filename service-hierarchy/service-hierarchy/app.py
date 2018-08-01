from flask import Flask
from service_hierarchy.views.index import bp as index_bp

app = Flask(__name__)
app.register_blueprint(index_bp)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'