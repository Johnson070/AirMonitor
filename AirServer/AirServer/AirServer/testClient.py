from operator import methodcaller
import requests, datetime
import jsonpickle
import AirServer.models as db

responge = requests.post('http://192.168.1.54:5000/sensors', json=
{
    'id': 0,
    'type': 'temp',
    'value': '23',
    'time': str(datetime.datetime.now()).replace(' ', 'T')
})

#responge = requests.get('http://192.168.1.54:5000/sensors')

#rint(responge.text)

# print(requests.get())
#
# model = db.models(atomizer_device=db.atomizer(False,1000,datetime.datetime.now(),True,100))
# model.add_sensor(db.sensor(0,100,datetime.datetime.now()))
#
# print(jsonpickle.encode(model, unpicklable=False))
