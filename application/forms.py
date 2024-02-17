from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, NumberRange, DataRequired
from datetime import datetime

# Car Prediction Form
class PredictionForm(FlaskForm):
    year_of_registration = IntegerField("Enter Car Registration Year:", validators=[DataRequired(), NumberRange(min=1900, max=datetime.now().year)])
    mileage = IntegerField("Enter Mileage:", validators=[DataRequired(), NumberRange(min=0)]) 
    mpg = FloatField("Enter MPG:", validators=[DataRequired(), NumberRange(min=0)])
    age_of_car = IntegerField("Enter Age of Car:", validators=[DataRequired(), NumberRange(min=0, max=100)])  # Assuming a car won't be older than 100 years
    tax = FloatField("Enter Tax:", validators=[DataRequired(), NumberRange(min=0)])
    fuel_type = SelectField("Enter Fuel Type:", choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('hybrid', 'Hybrid'), ('other', 'Other'), ('electric', 'Electric')], validators=[DataRequired()])
    engine_size = FloatField("Enter Engine Size:", validators=[DataRequired(), NumberRange(min=0)])
    transmission_type = SelectField("Enter Transmission Type:", choices=[('manual', 'Manual'), ('automatic', 'Automatic'), ('semi-automatic', 'Semi-Automatic'), ('other', 'Other')], validators=[DataRequired()])
    submit = SubmitField("PREDICT CAR VALUATION")

class LoginForm(FlaskForm):
	username = StringField("Username", validators = [InputRequired()])
	password = PasswordField("Password", validators = [InputRequired()])
	submit = SubmitField("LOGIN")
    