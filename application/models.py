from application import db
from datetime import datetime
from sqlalchemy.orm import validates

# For login
class User(db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(100), unique = True, nullable = False)
	password = db.Column(db.String(100), nullable = False)
	entries = db.relationship('CarEntry', backref='user', lazy=True)
 
# For storing prediction entries
class CarEntry(db.Model):
    __tablename__ = 'CarEntry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    year_of_registration = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    mpg = db.Column(db.Float, nullable=False)
    age_of_car = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    fuel_type = db.Column(db.String(50), nullable=False)
    engine_size = db.Column(db.Float, nullable=False)
    transmission_type = db.Column(db.String(50), nullable=False)
    prediction = db.Column(db.Float, nullable=False)
    predicted_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Validate the year value
    @validates('year_of_registration')
    def validate_year_of_registration(self, key, year):
        if year is None or not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        current_year = datetime.now().year
        if not (1900 <= year <= current_year):
            raise ValueError("Year must be between 1900 and the current year.")
        return year
    
    # Validate the mileage, age of the car, tax, and engine size
    @validates('mileage', 'age_of_car', 'tax', 'engine_size')
    def validate_positive_number(self, key, value):
        if value is None or not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be a number.")
        if value < 0:
            raise ValueError(f"{key} must be a positive number.")
        return value

    # Validate the mpg
    @validates('mpg')
    def validate_mpg(self, key, value):
        if value is None or not isinstance(value, (int, float)):
            try:
                value = float(value)
            except ValueError:
                raise ValueError(f"{key} must be a numeric value")
        if value <= 0:
            raise ValueError(f"{key} must be greater than 0")
        return value