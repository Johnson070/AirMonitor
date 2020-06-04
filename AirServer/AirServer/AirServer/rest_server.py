from AirServer import app
import AirServer.models as db
import jsonpickle, datetime
from flask import Flask, request

access_tokens = [None,None]

model = db.model()

model.atomizer = db.atomizer(False,1000,datetime.datetime.now(),True,100)

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
    model.add_sensor(db.sensor(json['id'], json['type'], json['value'], str(datetime.datetime.now()).replace(' ', 'T')))

    return jsonpickle.encode(model, unpicklable=False)

@app.route('/', methods=['GET','POST'])
def main():
    global model

    if request.method == 'POST':
        print(request.form['id'])
        print(request.form['type'])
        print(request.form['value'])
        print(request.form['time'])

        #model.add_sensor(db.sensor(0, 'temp', 23, datetime.datetime.now()))

        #test = sensor(1, 'temp', 55, datetime.datetime.now())

        #model.add_sensor(test)
        #model.add_nozzle(db.nozzle(0, False, 1000, datetime.datetime.now(),
        #False, 100))
        #model.add_nozzle(db.nozzle(1, False, 1000, datetime.datetime.now(),
        #False, 100))

        model.add_sensor(db.sensor(int(request.form['id']),request.form['type'], int(request.form['value']), request.form['time']))

    html = ''

    with open('index.html', 'r',encoding='utf-8') as f:
        html = f.read()

    index = html.rindex('</p>')

    html = html[:index] + f"<p>{jsonpickle.encode(model, unpicklable=False)}</p>" + html[index:]

    return html