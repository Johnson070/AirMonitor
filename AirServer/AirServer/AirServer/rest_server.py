from AirServer import app
import AirServer.models as data
import AirServer.bd_work as database
import jsonpickle, datetime
from flask import Flask, request

access_tokens = [None,None]

model = data.model()
db = database.db_work()

model.atomizer = data.atomizer(False,1000,datetime.datetime.now(),True,100)

@app.route('/sensors', methods=['GET'])
def get_list():
    json = request.json

    return jsonpickle.encode(model, unpicklable=False)


@app.route('/sensors', methods=['POST'],)
def update_list():
    global model
    json = request.json

    print(json)
    print(json['time'])
    model.add_sensor(data.sensor(json['id'], json['type'], json['value'], str(datetime.datetime.now()).replace(' ', 'T')))

    db.connect()
    db.add_sensor(json['id'], json['value'], json['type'])
    db.disconnect()

    return jsonpickle.encode(model, unpicklable=False)

@app.route('/', methods=['GET','POST'])
def main():
    global model

    if request.method == 'POST':
        #print(request.form['id'])
        #print(request.form['type'])
        #print(request.form['value'])
        #print(request.form['time'])

        model.add_sensor(data.sensor(int(request.form['id']),request.form['type'], int(request.form['value']), request.form['time']))

        try:
            db.connect()
            db.add_sensor(int(request.form['id']), int(request.form['value']), request.form['type'], request.form['time'])
            db.disconnect()
        except:
            pass

    html = ''

    with open('index.html', 'r',encoding='utf-8') as f:
        html = f.read()

    index = html.rindex('</p>')

    html = html[:index] + f"<p>{jsonpickle.encode(model, unpicklable=False)}</p>" + html[index:]

    return html