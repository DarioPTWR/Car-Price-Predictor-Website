from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import joblib


# Instantiate SQLAlchemy to handle db process
db = SQLAlchemy()

# Create the Flask app
app = Flask(__name__)

# Load configuration from config.cfg
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# AI Model File
joblib_file = "./application/static/joblib_Model.pkl"

app.debug = False

# Load AI Model
with open(joblib_file, 'rb') as f:
	ai_model = joblib.load(f)
 
with app.app_context():
	db.init_app(app)
	from .models import User, CarEntry
	db.create_all()
	db.session.commit()
	print('Created database!')

#run the file routes.py
from application import routes