from application.models import CarEntry
import datetime as datetime
import pytest
from flask import json

# For Unit Testing, we will be testing 5 types of tests. 
# Unexpected Failure Testing, Expected Failure Testing, Validity Testing, Consistency Testing, Range Testing
# We are able to do range testing due to the variability in values.

# 1. Unexpected Failure Testing ====================================================================================================================
@pytest.mark.parametrize("car_data", [
    # Test cases for varying data combinations
    [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000],
    [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000],
    [2019, 3000, 40, 1, 100, 'diesel', 1.8, 'manual', 25000],
    [None, None, None, None, None, None, None, None, None],
    [2000, 0, 0, 0, 0, 'petrol', 0, 'manual', 0],
    [2023, 300000, 100, 20, 1000, 'electric', 10, 'automatic', 500000],
    [2023, -300000, -100, 20, 1000, 'diesel', 10, 'automatic', 500000],
    [2021, 1000, 55, 0, 0, 'electric', 1.2, 'automatic', 30000],
    [2016, 16000, 34, 4, 170, 'diesel', 2.3, 'semi-automatic', 19000],
    [2010, 40000, 20, 10, 350, 'petrol', 3.2, 'manual', 8000],
    [2013, 14000, 29, 7, 190, 'hybrid', 2.0, 'automatic', 13000],
    [2014, 9000, 37, 5, 160, 'electric', 1.7, 'semi-automatic', 18000],
    [2015, 21000, 26, 6, 210, 'diesel', 2.5, 'manual', 15000],
    [2011, 26000, 23, 9, 290, 'petrol', 3.0, 'automatic', 10000],
    [2019, 3500, 48, 1, 100, 'hybrid', 1.5, 'semi-automatic', 25000],
    [2022, 500, 60.3, 0, 0, 'electric', 1.1, 'other', 32000],
    [2010, 35000, 20, 10, 350, 'petrol', 3.5, 'manual', 7000],
    [2016, 7000, 35, 4, 150, 'diesel', 1.9, 'automatic', 19000],
    [2018, 9500, 39, 2, 110, 'electric', 0, 'semi-automatic', 24000],
    [2020, 3000, 52, 1, 0, 'hybrid', 1.3, 'manual', 28000],
    ['hello', 27000, 24, 9, 290, 'diesel', 3.1, 'automatic', 10500]
])

def test_CarEntryClass(car_data, capsys):
    with capsys.disabled():
        print(car_data)
        now = datetime.datetime.utcnow()
        new_entry = CarEntry(
            year_of_registration=car_data[0],
            mileage=car_data[1],
            mpg=car_data[2],
            age_of_car=car_data[3],
            tax=car_data[4],
            fuel_type=car_data[5],
            engine_size=car_data[6],
            transmission_type=car_data[7],
            prediction=car_data[8],
            predicted_on=now
        )

        assert new_entry.year_of_registration == car_data[0]
        assert new_entry.mileage == car_data[1]
        assert new_entry.mpg == car_data[2]
        assert new_entry.age_of_car == car_data[3]
        assert new_entry.tax == car_data[4]
        assert new_entry.fuel_type == car_data[5]
        assert new_entry.engine_size == car_data[6]
        assert new_entry.transmission_type == car_data[7]
        assert new_entry.prediction == car_data[8]
        assert new_entry.predicted_on == now
        
# Results show that validation was successful in this case, with the correct tests failing and the rest passing.

# 2. Expected Failure Testing ====================================================================================================================
# For expected failure testing, we will intentionally test with invalid inputs for selected values to ensure our validation check is thorough.
# What if year / mileage / mpg was negative? What if age was negative? What if tax was negative?
# Transmission & Engine is assumed to be correct as the user can only interact with dropdown values
@pytest.mark.xfail(reason="Invalid input arguments (<= 0 or invalid types)")
@pytest.mark.parametrize("car_data", [
    # Test case with invalid year_of_registration (<= 0)
    [-1, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with invalid mileage (<= 0)
    [2015, -10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with invalid mpg (<= 0)
    [2015, 10000, -30, 5, 200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with invalid age_of_car (<= 0)
    [2015, 10000, 30, -5, 200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with invalid tax (<= 0)
    [2015, 10000, 30, 5, -200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with valid entry
    [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000, datetime.datetime.utcnow()],
    # Test case with valid entry
    [2017, 20000, 35, 4, 150, 'diesel', 2.0, 'automatic', 20000, datetime.datetime.utcnow()]
])
def test_CarEntryValidation(car_data, capsys):
    test_CarEntryClass(car_data, capsys)
    
# 3. Validity Testing ====================================================================================================================
    
# API Testing
# Testing Add API
@pytest.mark.parametrize("car_data", [
    # Test cases for varying data combinations
    [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000],
    [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000],
    [2019, 3000, 40, 1, 100, 'diesel', 1.8, 'manual', 25000],
])
def test_addAPI(client, car_data, capsys):
    with capsys.disabled():
        # Prepare the data into a dictionary
        predictData = {
            'year_of_registration': car_data[0],
            'mileage': car_data[1],
            'mpg': car_data[2],
            'age_of_car': car_data[3], 
            'tax': car_data[4],
            'fuel_type' : car_data[5],
            'engine_size' : car_data[6],
            'transmission_type' : car_data[7],
            'prediction':car_data[8],
        }
    # Use client object to post
    # Data is converted to JSON
    # Posting content is specified
    response = client.post('/api/add',
                           data=json.dumps(predictData),
                           content_type="application/json",)
    # Check the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["id"]
    
# Testing Get API
@pytest.mark.parametrize("predictionList", [
    # Test cases for varying data combinations
    [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000, 2], 
    [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000, 3],
    [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000, 4],
    [2019, 3000, 40, 1, 100, 'diesel', 1.8, 'manual', 25000, 5],
])
def test_getAPI(client, predictionList, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get/{predictionList[-1]}')
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == predictionList[-1]
        assert response_body["year_of_registration"] == predictionList[0]
        assert response_body["mileage"] == predictionList[1]
        assert response_body["mpg"] == predictionList[2]
        assert response_body["age_of_car"] == predictionList[3]
        assert response_body["tax"] == predictionList[4]
        assert response_body["fuel_type"] == predictionList[5]
        assert response_body["engine_size"] == predictionList[6]
        assert response_body["transmission_type"] == predictionList[7]
        assert response_body["prediction"] == predictionList[8]
        
# Testing Delete API
@pytest.mark.parametrize("car_data", [
    [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000],
])
def test_deleteAPI(client, car_data, capsys):
    with capsys.disabled():
        predictData = {
            'year_of_registration': car_data[0],
            'mileage': car_data[1],
            'mpg': car_data[2],
            'age_of_car': car_data[3], 
            'tax': car_data[4],
            'fuel_type' : car_data[5],
            'engine_size' : car_data[6],
            'transmission_type' : car_data[7],
            'prediction':car_data[8],
        }
        # Use client object to post data & convert to JSON
        response = client.post('/api/add', data=json.dumps(predictData), content_type="application/json",)
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]
        id = response_body["id"]
        response2 = client.get(f'/api/delete/{id}')
        ret = json.loads(response2.get_data(as_text=True))

        # Check the outcome of the action
        assert response2.status_code == 200
        assert response2.headers["Content-Type"] == "application/json"
        response2_body = json.loads(response2.get_data(as_text=True))
        assert response2_body["result"] == "ok"

# 4. Consistency Testing ====================================================================================================================
@pytest.mark.parametrize("bigPredictionList", [
    [
        [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
        [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000],
        [2015, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000]
    ],
    [
        [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000],
        [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000],
        [2017, 5000, 35, 3, 150, 'electric', 2.0, 'automatic', 20000]
    ],
    [
        [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000],
        [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000],
        [2012, 20000, 25, 8, 250, 'hybrid', 3.0, 'semi-automatic', 10000]
    ]
])
def test_predictAPI(client, bigPredictionList, capsys):
    predictOutput = []
    for predictionList in bigPredictionList:
        with capsys.disabled():
            # Prepare the data into a dictionary
            predictData = {
                'year_of_registration': predictionList[0],
                'mileage': predictionList[1],
                'mpg': predictionList[2],
                'age_of_car': predictionList[3], 
                'tax': predictionList[4],
                'fuel_type' : predictionList[5],
                'engine_size' : predictionList[6],
                'transmission_type' : predictionList[7],
                'prediction': predictionList[8],
            }
        response = client.post('/api/predict',
                               data=json.dumps(predictData),
                               content_type="application/json",)
        # Check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        predictOutput.append(response_body["prediction"])

    assert len(set(predictOutput)) == 1

# 5. Range Testing ====================================================================================================================
@pytest.mark.parametrize("car_data", [
    # Test lower and upper bounds of year_of_registration
    [1990, 10000, 30, 5, 200, 'petrol', 2.5, 'manual', 15000],
    [2023, 10000, 30, 5, 200, 'petrol', 2.5, 'automatic', 15000],
    # Test lower and upper bounds of mileage
    [2015, 1, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    [2015, 300001, 30, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    # Test lower and upper bounds of mpg (Miles Per Gallon)
    [2015, 10000, 10, 5, 200, 'petrol', 2.5, 'manual', 15000], 
    [2015, 10000, 101, 5, 200, 'petrol', 2.5, 'semi-automatic', 15000], 
    # Test lower and upper bounds of age_of_car
    [2015, 10000, 30, 1, 200, 'petrol', 2.5, 'manual', 15000], 
    [2015, 10000, 30, 21, 200, 'petrol', 2.5, 'manual', 15000], 
    # Test lower and upper bounds of tax
    [2015, 10000, 30, 5, 0, 'petrol', 2.5, 'manual', 15000],
    [2015, 10000, 30, 5, 1001, 'petrol', 2.5, 'other', 15000], 
    # Test lower and upper bounds of engine_size
    [2015, 10000, 30, 5, 200, 'petrol', 0.5, 'manual', 15000], 
    [2015, 10000, 30, 5, 200, 'petrol', 5.1, 'manual', 15000],
])
def test_CarEntryRange(client, car_data, capsys):
    with capsys.disabled():
        columns = ['year_of_registration', 'mileage', 'mpg', 'age_of_car', 'tax', 'fuel_type', 'engine_size', 'transmission_type']
        data = {col: v for col, v in zip(columns, car_data)}

        response = client.post("/api/predict", data=json.dumps(data), content_type='application/json')
        
        # Validate response
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert "error" not in response_body.keys()
        assert "id" in response_body and "prediction" in response_body