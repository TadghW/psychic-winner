#Flask is a microframework for Python that handles web requests according to the WSGI protocol using WSGI library Werkzeug
#SQLAlchemy is an SQL Toolkit and ORM for Python, Flask-SQLAlchemy is a Flask extension that appends SQLAlchemy onto Flask  
#Flask_CORS allows us to set our Cross Origin Resource Sharing HTTP header values so that we can run this demo locally 
#Marshmallow is a convenient way to deserialize data (like SQLAlchemy objects) 

from flask import Flask, render_template, request, redirect, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
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
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    wind_speed = db.Column(db.Integer)
    wind_direction = db.Column(db.String(3))
    precipitation_type = db.Column(db.String(24))
    precipitation_rate = db.Column(db.Integer)

#If the database already exists db.create_all() won't do anything, but otherwise it will create the database referenced at SQLALCHEMY_DATABASE_URI
with app.app_context():
    db.create_all()

#To deserialize SQLALchemy query results concisely I'm going to use marshmallow_sqlalchemy's SQLAlchemyAutoSchema
class SensorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sensors
        load_instance = True
    
class SensorDataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SensorData
        load_instance = True


#API ROOT-----------------------------------------------------------
@app.route('/api', methods=['GET'])
def api_root():
    
    #Load in our marshmallow schema
    sensor_schema = SensorSchema()
    sensor_data_schema = SensorDataSchema()
    #Query our database
    sensors = Sensors.query.order_by(Sensors.date_created).all()
    sensor_data = SensorData.query.order_by(SensorData.date_time).all()
    
    #Deserialise query results and store them in a list 
    sensors_list = []
    for sensor in sensors:
        sensor_dump = sensor_schema.dump(sensor)
        sensors_list.append(sensor_dump)
    
    sensor_data_list = []
    for data in sensor_data:
        sensor_data_dump = sensor_data_schema.dump(data)
        sensor_data_list.append(sensor_data_dump)

    #Compile lists to dict
    response = {"Sensors": sensors_list, "Sensor Data": sensor_data_list}
    #Make response
    return make_response(str(response), 200)

#SENSORS API---------------------------------------------------------
@app.route('/api/sensors', methods=['GET', 'POST', 'DELETE'])
def sensors():

    if request.method == 'GET':

        #Load in our marshmallow schema
        sensor_schema = SensorSchema()
        #Query our database
        sensors = Sensors.query.order_by(Sensors.date_created).all()
        #Deserialise query results and store them in a list
        sensors_list = []
        for sensor in sensors:
            sensor_dump = sensor_schema.dump(sensor)
            sensors_list.append(sensor_dump)
        #Make response
        return make_response(str(sensors_list), 200)
    
    
    if request.method == 'POST':
        
        #Load the request body as a dict
        data = request.values
        id = data['id']
        location = data['location']
        region = data['region']
        country = data['country']
        
        #Check that the id doesn't already exist in the table
        #If it does, return a 403 (Forbidden)
        id_exists = db.session.query(db.session.query(Sensors).filter_by(id=id).exists()).scalar()
        if id_exists == True:
            abort(403)
        
        #Otherwise, as all other fields are nullable other data is valid
        new_sensor = Sensors(id=id, location=location, region=region, country=country)

        #Commit to db and return success code
        try:
            db.session.add(new_sensor)
            db.session.commit()
            return make_response('Success', 201)
        except Exception as e:
            #Or return failure
            return make_response('Exception returned attempting to add new sensor: ' + str(e), 500)


    if request.method == 'DELETE':
    
        #Load the request data to find the id
        data = request.values
        id_to_drop = data['id']

        #Find the object with corresponding id in the table
        sensor = Sensors.query.get_or_404(id_to_drop)

        #Delete it and return success
        try:
            db.session.delete(sensor)
            db.session.commit()
            return make_response(jsonify('Success'), 200)
        except Exception as e: 
            #Or return failure
            return make_response(jsonify('Failed to delete sensor via API: ' + str(e)), 500)

#SENSOR DATA API--------------------------------------------------------
@app.route('/api/data', methods=['GET', 'POST', 'DELETE'])
def sensor_data():

    if request.method == 'GET':
        #Load Marshmallow schema
        sensor_data_schema=SensorDataSchema()
        #Query Database
        sensor_data = SensorData.query.order_by(SensorData.date_time).all()
        #Deserialise query results and store in list
        sensor_data_list = []
        for data in sensor_data:
            sensor_data_dump = sensor_data_schema.dump(data)
            sensor_data_list.append(sensor_data_dump)
        return make_response(str(sensor_data_list), 200)
    
    if request.method == 'POST':
    
        #Load the request body as a dict
        data = request.values

        #All sensor data POST requests MUST have a sensor_id that corresponds to an existing sensor
        #So we're going to check that here
        sensor_id = data['sensor_id']

        sensor_id_exists = db.session.query(db.session.query(Sensors).filter_by(id=sensor_id).exists()).scalar()
        if sensor_id_exists == False:
            abort(403)

        temperature = data['temperature']
        humidity = data['humidity']
        wind_speed = data['wind-speed']
        wind_direction = data['wind-direction']
        precipitation_type = data['precipitation-type']
        precipitation_rate = data['precipitation-rate']
        new_sensor_data = SensorData(sensor_id=sensor_id, temperature=temperature, humidity=humidity, wind_speed=wind_speed, wind_direction=wind_direction, precipitation_type=precipitation_type, precipitation_rate=precipitation_rate)
        
        #Commit to db and return success code
        try: 
            db.session.add(new_sensor_data)
            db.session.commit()
            return make_response(jsonify('Success'),201)
        except Exception as e:
            #Or return failure
            return make_response(jsonify('Exception returned attempting to add new sensor data: ' + str(e)), 500)

    if request.method == 'DELETE':
    
        #Load the request data to find the id
        data = request.values
        id_to_drop = data['id']

        #Find the object with the corresponding id in the table
        sensor_data = SensorData.query.get_or_404(id_to_drop)

        #Delete it and return success
        try:
            db.session.delete(sensor_data)
            db.session.commit()
            return make_response(jsonify('Success'), 200)
        except Exception as e: 
            return make_response(jsonify('Exception returned attempting to delete sensor data entry: ' + str(e)), 500)

#QUERY API---------------------------------------------------------------
#api/query request must inlcude 5 parameters: metric1 (calculation), metric2 (metric), location, time_from, and time_to
@app.route('/api/query', methods=['GET'])
def respondToQuery():
    
    #request.args can read the arguments passed to a url by a HTTP request
    metric1 = request.args.get('metric1')
    metric2 = request.args.get('metric2')
    location = request.args.get('location')
    time_from = request.args.get('from')
    time_to = request.args.get('to')
    
    #populate list of all sensors
    sensors = Sensors.query.all()

    #check which ones are located in the region specified by the query
    local_sensors = []
    for sensor in sensors:
        if location in sensor.region.lower() or location in sensor.country.lower():
            local_sensors.append(sensor.id)

    #Now we can query to see what sensor data entries are within the user set time period
    in_period_entries = SensorData.query.filter(SensorData.date_time.between(time_from, time_to)).all()
    
    #Now let's see which sensor data entries come from local sensors in the time period set
    valid_entries = []
    for data in in_period_entries:
        if data.sensor_id in local_sensors:
            valid_entries.append(data)

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
        return make_response(str(max(values)), 201)
    if metric1 == 'min':
        return make_response(str(min(values)), 201)
    if metric1 == 'mean':
        return make_response(str(sum(values) / len(values)), 201)


#DASHBOARD STUFF ---------------------------------------------------------------------------------------------------------------------
#Accessing root will return a dashboard showing the information in the server at any given time
@app.route('/')
def index():
    sensors = Sensors.query.order_by(Sensors.date_created).all()
    sensor_data = SensorData.query.order_by(SensorData.date_time).all()
    return render_template('index.html', sensors=sensors, sensor_data=sensor_data)

#Passing index() an error will create an error box at the top of the page
def index(error):
    sensors = Sensors.query.order_by(Sensors.date_created).all()
    sensor_data = SensorData.query.order_by(SensorData.date_time).all()
    error = error
    return render_template('index.html', sensors=sensors, sensor_data=sensor_data, error=error)

#You can add additional sensors from the dashboard with a HTML form
@app.route('/sensors', methods=['POST'])
def dash_sensors():    
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

#You can remove sensors from the dashboard too, although it's implemented with a GET and not a drop
@app.route('/delete-sensor/<string:id>', methods=['GET'])
def dash_deleteSensor(id):
    #I've implemented the delete links hastily by 
    sensor = Sensors.query.get_or_404(id)
    try:
        db.session.delete(sensor)
        db.session.commit()
        return redirect('/')
    except Exception as e: 
        return index('Exception returned attempting to delete sensor: ' + str(e))

#You can add additional sensor data from the dashboard with a HTML form
@app.route('/data', methods=['POST'])
def dash_data():
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

#You can remove sensor data from the dashboard too, although it's implemented with a GET and not a drop
@app.route('/delete-data/<string:id>', methods=['GET'])
def dash_delete_data(id):
    sensor_data = SensorData.query.get_or_404(id)
    try:
        db.session.delete(sensor_data)
        db.session.commit()
        return redirect('/')
    except Exception as e: 
        return index('Exception returned attempting to delete data: ' + str(e))


if __name__ == "__main__":
    app.run(debug=True)