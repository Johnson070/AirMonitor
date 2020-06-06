from AirServer import app
import AirServer.models as data
import AirServer.bd_work as database
import jsonpickle, datetime,os
from flask import request,render_template

access_tokens = [None,None]

model = data.model()
db = database.db_work()

@app.route('/getvalue')
def getValue():
    return jsonpickle.encode(model, unpicklable=False, indent=4)

@app.route('/favicon.ico')
def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'),
    #                           'icon.ico', mimetype='image/vnd.microsoft.icon')
    return app.send_static_file('favicon.ico')

@app.route('/sensor', methods=['GET'])
def get_sensors():
    return jsonpickle.encode(model, unpicklable=False)


@app.route('/sensor', methods=['POST'],)
def add_sensor():
    global model
    json = None

    json = request.json

    model.add_sensor(
            data.sensor(
                int(json['id']), 
                json['type'], 
                [
                    data.sensor_value(
                        int(json['value']), 
                        json['time'].replace('T',' '))
                    ]
                ))

    db.connect()
    db.add_sensor(json['id'], json['type'], json['value'],json['time'].replace('T',' '))
    db.disconnect()

    return jsonpickle.encode(model, unpicklable=False)

@app.route('/nozzle', methods=['POST'],)
def add_nozzle():
    global model
    json = None

    json = request.json

    model.add_nozzle(
        data.nozzle(
            int(json['id']),
            [
            data.nozzle_value( 
                json['state_nozzle'], 
                json['time'], 
                json['state_fan'], 
                int(json['rpm_fan']
                    )
                )
            ]
            ))

    db.connect()
    db.add_nozzle(int(json['id']),json['state_nozzle'],json['state_fan'],int(json['rpm_fan']),json['time'])
    db.disconnect()

    return jsonpickle.encode(model, unpicklable=False)

@app.route('/nozzle', methods=['GET'])
def get_nozzles():
    return jsonpickle.encode(model, unpicklable=False)

@app.route('/atomizer', methods=['GET'])
def get_atomizers():
    return jsonpickle.encode(model, unpicklable=False)

@app.route('/atomizer', methods=['POST'],)
def add_atomizer():
    global model
    json = None

    json = request.json

    model.add_atomizer(
        data.atomizer(
            [
            data.atomizer_value( 
                json['state_pump'], 
                int(json['pressure']),
                json['state_fan'], 
                int(json['rpm_fan']),
                json['time']
                )
            ]
            ))

    db.connect()
    db.add_nozzle(json['state_pump'],int(json['pressure']),json['state_fan'],int(json['rpm_fan']),json['time'])
    db.disconnect()

    return jsonpickle.encode(model, unpicklable=False)

@app.route('/')
def main():
    global model

    if request.method == 'POST':
        #print(request.form['id'])
        #print(request.form['type'])
        #print(request.form['value'])
        #print(request.form['time'])

        model.add_sensor(
            data.sensor(
                int(request.form['id']), 
                request.form['type'], 
                [
                    data.sensor_value(
                        int(request.form['value']), 
                        request.form['time'])
                    ]
                ))

        try:
            db.connect()
            db.add_sensor(int(request.form['id']), int(request.form['value']), request.form['type'], request.form['time'])
            db.disconnect()
        except:
            pass

    return render_template('index_new.html', title = 'AirServer', data = jsonpickle.encode(model, unpicklable=False, indent=4))