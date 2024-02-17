from application import app, ai_model, db
from flask import render_template, request, flash, redirect, url_for, make_response, session, json, jsonify
from application.forms import PredictionForm, LoginForm
from application.models import CarEntry
from datetime import datetime
from application.decorators import login_required
from sqlalchemy import desc

# Configurations for the Web App
# For login page, we will set a default USERNAME and PASSWORD for demonstration purposes
URL = 'http://127.0.0.1:5000'
USERNAME = 'student'
PASSWORD = 'student'

# Adding a new entry
def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error, 'error')
        
# Getting entries from database
def get_entries():
    try:
        entries = CarEntry.query.filter_by().order_by(desc(CarEntry.id)).all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, 'error')
        return 0
    
# Deleting entries from database
def remove_entry(id):
    try:
        entry = CarEntry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, 'error')
        return 0
        
# Index Route
@app.route("/", methods = ['GET'])
@app.route("/index", methods = ['GET'])
@login_required
def index():
    form = PredictionForm()
    return render_template("index.html", form=form, entries=get_entries())

# Login Route
@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()

	# Check if post request
	if request.method == 'POST':
		if form.validate_on_submit():

			username = request.form.get('username')
			password = request.form.get('password')

			if username == USERNAME and password == PASSWORD:
				resp = make_response(redirect(url_for('index')))
				resp.set_cookie('uid', '1') # Get uid and set as cookie
				return resp

			else:
				flash('Incorrect Username or Password.', 'error')

	# Check if already logged in 
	if 'uid' in request.cookies and str(request.cookies['uid']) == '1':
		return redirect(url_for('index'))

	return render_template("login.html", form = form)

# Logout Route
@app.route("/logout", methods=['POST'])
def logout():
	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('uid', '', expires = 0) # Get uid and set as cookie for logout
	return resp
 
# Predict Route
@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    form = PredictionForm()
    prediction_result = None
    if request.method == 'POST':
        if form.validate_on_submit():
            # Extract form data
            year = form.year_of_registration.data
            mileage = form.mileage.data
            mpg = form.mpg.data
            car_age = form.age_of_car.data
            tax = form.tax.data
            fuel_type = form.fuel_type.data
            engine_size = form.engine_size.data
            transmission_type = form.transmission_type.data
            X = [[
                year,
                mileage,
                mpg,
                car_age,
                tax,
                1 if fuel_type == 'petrol' else 0,
                1 if fuel_type == 'hybrid' else 0,
                1 if fuel_type == 'other' else 0,
                1 if fuel_type == 'electric' else 0,
                1 if transmission_type == 'manual' else 0,
                1 if transmission_type == 'semi-automatic' else 0,
                1 if transmission_type == 'other' else 0,
                engine_size
            ]]
            prediction = ai_model.predict(X)
            # Adding a new entry to the database
            new_entry = CarEntry(
                userid = 1,
                year_of_registration=year,
                mileage=mileage,
                mpg=mpg,
                age_of_car=car_age,
                tax=tax,
                fuel_type=fuel_type,
                engine_size=engine_size,
                transmission_type=transmission_type,
                prediction=round(prediction[0], 1),
                predicted_on=datetime.now()
            )
            add_entry(new_entry)
            prediction_result = round(prediction[0], 1)
            session['prediction_result'] = prediction_result
            return redirect(url_for('result'))  # Redirect to the result page
        else:
            flash('Prediction Failed. Ensure all fields are filled.', 'error')
    return render_template("index.html", title="CarValuify | Your One-Stop Car Valuation Platform", form=form, index=True, prediction_result = prediction_result, entries=get_entries())

# Prediction Result Route
@app.route('/result')
@login_required
def result():
    prediction_result = session.get('prediction_result', None)
    return render_template("result.html", prediction_result=prediction_result, no_nav=True, no_footer=True)

# Profile History Route
@app.route("/profile")
@login_required
def profile():
    try:
        form = PredictionForm()
        return render_template("profile.html", title="CarValuify | Your Profile", form=form, entries=get_entries())
    except Exception as e:
        flash('An error occurred while fetching your profile data.', 'error')
        # Log the error
        app.logger.error(f'Error fetching profile data: {e}')
        return redirect(url_for('index'))
        
# Remove Database Record
@app.route('/remove', methods=['POST'])
def remove():
    req = request.form
    id = req["id"]
    remove_entry(id)
    return redirect(url_for('profile'))

# API : Add Entry
@app.route("/api/add", methods=['POST'])
def api_add():
    # Retrieve the json file posted from client
    data = request.get_json()
    # Retrieve each field from the data
    year_of_registration = data['year_of_registration']
    mileage = data['mileage']
    mpg = data['mpg']
    age_of_car = data['age_of_car']
    tax = data['tax']
    fuel_type = data['fuel_type']
    engine_size = data['engine_size']
    transmission_type = data['transmission_type']
    prediction = data['prediction']

    # Create a CarEntry object store all data for DB action
    new_entry =  CarEntry (
        userid=1,
        year_of_registration = year_of_registration,
        mileage = mileage,
        mpg = mpg,
        age_of_car = age_of_car, 
        tax = tax,
        fuel_type = fuel_type,
        engine_size = engine_size,
        transmission_type = transmission_type,
        prediction=prediction,
        predicted_on=datetime.now())
    # Invoke the add entry function to add entry
    result = add_entry(new_entry)
    # Return the result of the db action
    return jsonify({'id':result})

# API : Get Entry
# Get Entry Function
def get_entry(id):
    try:
        result = CarEntry.query.get(id)
        return result
    except Exception as error:
        db.session.rollback()
        flash(error,"error")
        return 0 
    
# Get Entry 
@app.route("/api/get/<id>", methods=['GET'])
def api_get(id):
    # Retrieve the entry using ID from the client
    entry = get_entry(int(id))
    data = {
        "id" : entry.id,
        "userid": 1,
        # Retrieve each field from the data
        "year_of_registration": entry.year_of_registration,
        "mileage": entry.mileage,
        "mpg": entry.mpg,
        "age_of_car": entry.age_of_car,
        "tax": entry.tax,
        "fuel_type": entry.fuel_type,
        "engine_size": entry.engine_size,
        "transmission_type": entry.transmission_type,
        "prediction": entry.prediction,
    }
    # Convert the data from JSON
    result = jsonify(data)
    return result # Return response back

# API : Delete Entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id):
    entry = remove_entry(int(id))
    return jsonify({'result': 'ok'})

# API : Predict Entry
@app.route("/api/predict", methods=['POST'])
def api_predict():
    data = request.get_json()

    # Extracting data from the request
    year_of_registration = data['year_of_registration']
    mileage = data['mileage']
    mpg = data['mpg']
    age_of_car = data['age_of_car']
    tax = data['tax']
    fuel_type = data['fuel_type']
    engine_size = data['engine_size']
    transmission_type = data['transmission_type']

    # Prepare data for prediction
    X = [[ 
        year_of_registration,
        mileage,
        mpg,
        age_of_car,
        tax,
        1 if fuel_type == 'petrol' else 0,
        1 if fuel_type == 'hybrid' else 0,
        1 if fuel_type == 'other' else 0,
        1 if fuel_type == 'electric' else 0,
        1 if transmission_type == 'manual' else 0,
        1 if transmission_type == 'semi-automatic' else 0,
        1 if transmission_type == 'other' else 0,
        engine_size
    ]]

    # Predicting using the AI model
    prediction = ai_model.predict(X)

    # Creating a new entry in the database
    new_entry = CarEntry(
        userid=1,
        year_of_registration=year_of_registration,
        mileage=mileage,
        mpg=mpg,
        age_of_car=age_of_car,
        tax=tax,
        fuel_type=fuel_type,
        engine_size=engine_size,
        transmission_type=transmission_type,
        prediction=round(prediction[0], 1),
        predicted_on=datetime.utcnow()
    )

    # Add entry to the database and return the result
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'id': new_entry.id, 'prediction': round(prediction[0], 1)})