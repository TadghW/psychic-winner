#Flask is a microframework for Python that handles web requests according to the WSGI protocol using WSGI library Werkzeug
#SQLAlchemy is an SQL Toolkit and ORM for Python, Flask-SQLAlchemy is a Flask extension that appends SQLAlchemy onto Flask  
#Flask_CORS allows us to set our Cross Origin Resource Sharing HTTP header values so that we can run this demo locally 

from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

#Flask-SQLAlchemy loads configuration keys from Flask, so you set Flask-SQLAlchemy configuraiton keys with Flask's app.config
#Here we tell Flask-SQLAlchemy where to find the database and what engine to use when interacting with it  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solution.db'
db = SQLAlchemy(app)
CORS(app)

#I'm going to normalise the data minimally, organising it into two tables, one for sensors and one for sensor data
class Sensors(db.Model):
    __tablename__ = 'Sensors'
    id = db.Column(db.String(128), primary_key=True)
    location = db.Column(db.String(128))
    region = db.Column(db.String(128))
    country = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

class SensorData(db.Model):
    __tablename__ = 'SensorData'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.String(128), nullable=False)
    #By setting default to datetime.utcnow we can generate a timestamp when a PUT query is recieved
    #This might not be satisfactory if for some applications where lag in the system creates an inaccurate timestamp for when the data was read, but for meteorological purposes this should be fine
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)
    wind_direction = db.Column(db.String(3))
    precipitation_type = db.Column(db.String(24))
    precipitation_rate = db.Column(db.Integer)

#If the database already exists db.create_all() won't do anything extra, this line checks that the database exists and create it if not
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    sensors = Sensors.query.order_by(Sensors.date_created).all()
    sensor_data = SensorData.query.order_by(SensorData.date_time).all()
    return render_template('index.html', sensors=sensors, sensor_data=sensor_data)

#returns webpage with info and an error message
def index(error):
    sensors = Sensors.query.order_by(Sensors.date_created).all()
    sensor_data = SensorData.query.order_by(SensorData.date_time).all()
    error = error
    return render_template('index.html', sensors=sensors, sensor_data=sensor_data, error=error)

@app.route('/sensors', methods=['POST'])
def sensors():    
    #We can't have duplicate primary keys in the Sensors table, let's catch that and display an error in-page
    #if a user tries to use an existing sensor-id
    id = request.form['sensor-id']
    idExists = db.session.query(db.session.query(Sensors).filter_by(id=id).exists()).scalar()
    if idExists == True:
        return index("ERROR: Sensor ID '" + id + "' already in use")
    
    location = request.form['sensor-location']
    region = request.form['sensor-region']
    country = request.form['sensor-country']
    new_sensor = Sensors(id=id, location=location, region=region, country=country)
    try: 
        db.session.add(new_sensor)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return 'Exception returned attempting to add new sensor: ' + str(e)

@app.route('/delete-sensor/<string:id>', methods=['GET'])
def deleteSensor(id):
    sensor = Sensors.query.get_or_404(id)
    try:
        db.session.delete(sensor)
        db.session.commit()
        return redirect('/')
    except Exception as e: 
        return index('Exception returned attempting to delete sensor: ' + str(e))

@app.route('/data', methods=['POST'])
def data():
    #We need to check that a sensor exists under a given ID for the data input to be valid
    #sensor data is assigned an ID and DateTime on construction
    sensor_id = request.form['sensor-id']
    idExists = db.session.query(db.session.query(Sensors).filter_by(id=sensor_id).exists()).scalar()
    if idExists == False:
        return index("ERROR: Sensor '" + sensor_id + "' not found.")
    temperature = request.form['temp']
    humidity = request.form['humidity']
    wind_speed = request.form['wind']
    wind_direction = request.form['wind-dir']
    precipitation_type = request.form['precip']
    precipitation_rate = request.form['precip-q']
    new_data = SensorData(sensor_id=sensor_id, temperature=temperature, humidity=humidity, wind_speed=wind_speed, wind_direction=wind_direction, precipitation_rate=precipitation_rate, precipitation_type=precipitation_type)

    try:
        db.session.add(new_data)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return index('Exception returned attempting to add new sensor data ' + str(e))

@app.route('/delete-data/<string:id>', methods=['GET'])
def deleteData(id):
    sensor_data = SensorData.query.get_or_404(id)
    try:
        db.session.delete(sensor_data)
        db.session.commit()
        return redirect('/')
    except Exception as e: 
        return index('Exception returned attempting to delete data: ' + str(e))

@app.route('/query')
def respondToQuery():
    
    #request.args can read the arguments passed to a url by a HTTP request
    metric1 = request.args.get('metric1')
    metric2 = request.args.get('metric2')
    location = request.args.get('location')
    time_from = request.args.get('from')
    time_to = request.args.get('to')

    print('Request arguments: ' + metric1 + ' ' + metric2 + ' ' + location + ' ' + time_from + ' ' + time_to)
    
    #populate list of all sensors
    sensors = Sensors.query.all()

    #check which ones are located in the region specified by the query
    local_sensors = []
    for sensor in sensors:
        if location in sensor.region.lower() or location in sensor.country.lower():
            local_sensors.append(sensor.id)

    print('Local Sensors: ' + str(local_sensors))

    #Now we can query to see what sensor data entries are within the user set time period
    in_period_entries = SensorData.query.filter(SensorData.date_time.between(time_from, time_to)).all()
    
    print('In Period Entries: ' + str(in_period_entries))
    
    #Now let's see which sensor data entries come from local sensors in the time period set
    valid_entries = []
    for data in in_period_entries:
        if data.sensor_id in local_sensors:
            valid_entries.append(data)
    
    print('Valid Entries: ' + str(valid_entries))

    #Now we can calculate whatever metric the user has requested
    values = []
    for entry in valid_entries:
        if metric2 == 'temp':
            values.append(entry.temperature)
        if metric2 == 'humidity':
            values.append(entry.humidity)
        if metric2 == 'wind-speed':
            values.append(entry.wind_speed)
        if metric2 == 'precipitation':
            values.append(entry.precipitation)
    
    if metric1 == 'max':
        return make_response(jsonify(max(values)))
    if metric1 == 'min':
        return make_response(jsonify(min(values)))
    if metric1 == 'mean':
        return make_response(jsonify(sum(values) / len(values)))

if __name__ == "__main__":
    app.run(debug=True)