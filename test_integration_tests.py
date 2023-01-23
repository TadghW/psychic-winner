import pytest
import requests
import json
from app import app


def test_server_responds():
    response = requests.get('http://127.0.0.1:5000/')
    assert response.status_code == 200

def test_api_root_responds():
    response = requests.get('http://127.0.0.1:5000/api')
    assert response.status_code == 200

def test_api_sensors_responds():
    response = requests.get('http://127.0.0.1:5000/api/sensors')
    assert response.status_code == 200

def test_data_responds():
    response = requests.get('http://127.0.0.1:5000/api/data')
    assert response.status_code == 200

def test_sensor_create():
    test_sensor = {
        "id": "integration_test_sensor",
        "location": "my_house",
        "region": "galway",
        "country": "ireland",
    }
    response = requests.post("http://127.0.0.1:5000/api/sensors", data=test_sensor)
    assert response.status_code == 201

def test_sensor_created():
    response = requests.get('http://127.0.0.1:5000/api/sensors').content.decode()
    list = eval(response)
    assert any(sensor['id'] == 'integration_test_sensor' for sensor in list)

def test_sensor_correct():
    response = requests.get('http://127.0.0.1:5000/api/sensors').content.decode()
    list = eval(response)
    test_sensor = next(sensor for sensor in list if sensor['id'] == 'integration_test_sensor')
    if test_sensor['location'] != 'my_house': return False
    if test_sensor['region'] != 'galway': return False
    if test_sensor['country'] != 'ireland': return False
    assert True

def test_data_create():
    test_sensor_data = {
        "sensor_id": "integration_test_sensor",
        "temperature": "9999999",
        "humidity": "600",
        "wind-speed": "1000",
        "wind-direction": "SSS",
        "precipitation-type": "fire",
        "precipitation-rate": "10000"
    }
    response = requests.post("http://127.0.0.1:5000/api/data", data=test_sensor_data)
    assert response.status_code == 201

def test_data_created():
    response = requests.get('http://127.0.0.1:5000/api/data').content.decode()
    list = eval(response)
    assert any(sensor_data['sensor_id'] == 'integration_test_sensor' for sensor_data in list)

def test_data_correct():
    response = requests.get('http://127.0.0.1:5000/api/data').content.decode()
    list = eval(response)
    test_data = next(sensor_data for sensor_data in list if sensor_data['sensor_id'] == 'integration_test_sensor')
    if test_data['temperature'] != 9999999: assert False
    if test_data['humidity'] != 600: assert False
    if test_data['wind_speed'] != 1000: assert False
    if test_data['wind_direction'] != 'SSS': assert False
    if test_data['precipitation_type'] != 'fire': assert False
    if test_data['precipitation_rate'] != 10000: assert False
    assert True

def test_query_responds():
    response = requests.get('http://127.0.0.1:5000/api/query?metric1=max&metric2=temp&location=galway&from=2023-01-22&to=2023-01-25')
    assert response.status_code == 201

def test_query_response_adjusted():
    response = requests.get('http://127.0.0.1:5000/api/query?metric1=max&metric2=temp&location=galway&from=2023-01-22&to=2023-01-25').content.decode()
    assert response == '9999999'

def test_data_delete():
    response = requests.get('http://127.0.0.1:5000/api/data').content.decode()
    list = eval(response)
    test_data = next(sensor_data for sensor_data in list if sensor_data['sensor_id'] == 'integration_test_sensor')
    sensor_id_to_drop = {"id": test_data['id']}
    response = requests.delete("http://127.0.0.1:5000/api/data", data=sensor_id_to_drop)
    assert response.status_code == 200

def test_data_deleted():
    response = requests.get('http://127.0.0.1:5000/api/data').content.decode()
    list = eval(response)
    assert not any(data['temperature'] == '9999999' for data in list)

def test_sensor_delete():
    sensor_id_to_drop = {"id": "integration_test_sensor"}
    response = requests.delete("http://127.0.0.1:5000/api/sensors", data=sensor_id_to_drop)
    assert response.status_code == 200

def test_sensor_deleted():
    response = requests.get('http://127.0.0.1:5000/api/sensors').content.decode()
    list = eval(response)
    assert not any(sensor['id'] == 'integration_test_sensor' for sensor in list)
