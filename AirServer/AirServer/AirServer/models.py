import datetime
import jsonpickle

class atomizer:
    def __init__(self, values:list):
        self.values = values

class atomizer_value:
    def __init__(self, state_pump: bool, pressure: int, state_fan: bool, rpm_fan: int, time: datetime):
        self.state_pump = state_pump
        self.pressure = pressure
        self.state_fan = state_fan
        self.rpm_fan = rpm_fan
        self.time = time

class nozzle:
    def __init__(self, id: int, values:list=None):
        self.id = id
        self.values = values

class nozzle_value:
    def __init__(self, state_nozzle: bool, time: datetime, state_fan: bool, rpm_fan: int):
        self.state_nozzle = state_nozzle
        self.time = time
        self.state_fan = state_fan
        self.rpm_fan = rpm_fan


class sensor:
    def __init__(self, id: int, type: str, values: list=None):
        self.id = id
        self.type = type
        self.values = values

class sensor_value:
    def __init__(self, value:int, time:datetime):
        self.value = value
        self.time = time

class model:
    def __init__(self, sensors: list=[], atomizer_device: list=[], nozzles: list=[]):
        self.sensors : list = sensors
        self.atomizer : list = atomizer_device
        self.nozzles : list = nozzles

    def class_to_dict(self, value, list_type:bool=True):
        value_return = None

        if list_type:
            value_return = []
            value_return.append(jsonpickle.decode(jsonpickle.encode(value, unpicklable=False)))
        else:
            value_return = jsonpickle.decode(jsonpickle.encode(value, unpicklable=False))

        return value_return

    def add_atomizer(self, atomizer:atomizer):
        self.atomizer.append(atomizer)

    def add_sensor(self, sensor):
        if not sensor is str:
            sensor :sensor = model.class_to_dict(self,sensor,False)

        math_id = False

        for sensor_for in self.sensors:
            if sensor_for['id'] == sensor['id']:
                math_id = True

        if math_id:
            for i in range(len(self.sensors)):
                if (sensor['id'] == self.sensors[i]['id'] and not sensor['values'] is None):
                    for j in range(len(sensor['values'])):
                        self.sensors[i]['values'].append(
                            model.class_to_dict(
                                self, 
                                sensor_value(
                                    sensor['values'][j]['value'], 
                                    sensor['values'][j]['time']), 
                                False))
        else:
            self.sensors.append(sensor)

    def delete_sensor(self, id: int):
        for i in range(0, len(self.sensors)):
            if self.sensors[i].id == id:
                del self.sensors[id]

    def add_nozzle(self, nozzle):
        if not nozzle is str:
            nozzle:nozzle = model.class_to_dict(self,nozzle, False)

        math_id = False

        for nozzle_for in self.nozzles:
            if nozzle_for['id'] == nozzle['id']:
                math_id = True

        if math_id:
            for i in range(len(self.nozzles)):
                if (nozzle['id'] == self.nozzles[i]['id'] and not nozzle['values'] is None):
                    for j in range(len(nozzle['values'])):
                        self.nozzles[i]['values'].append(
                            model.class_to_dict(self, 
                                                nozzle_value(
                                                    nozzle['values'][j]['state_nozzle'], 
                                                    nozzle['values'][j]['time'], 
                                                    nozzle['values'][j]['state_fan'], 
                                                    nozzle['values'][j]['rpm_fan']),
                                                False))
        else:
            self.nozzles.append(nozzle)

    def delete_nozzle(self, id: int):
        for i in range(0, len(self.nozzles)):
            if self.nozzles[i].id == id:
                del self.nozzles[id]

if __name__ == '__main__':
    models = model()

    models.add_sensor(sensor(0,'temp', [sensor_value(23,datetime.datetime.now())]))
    models.add_sensor(sensor(1,'temp', [sensor_value(1,datetime.datetime.now())]))
    models.add_sensor(sensor(0,'temp', [sensor_value(22,datetime.datetime.now())]))

    print(jsonpickle.encode(models, unpicklable=False))


    models.add_nozzle(nozzle(0, models.class_to_dict(nozzle_value(False, 1000, datetime.datetime.now(), False, 0))))
    models.add_nozzle(nozzle(1))
    models.add_nozzle(nozzle(0, models.class_to_dict(nozzle_value(True, 1500, datetime.datetime.now(), True, 100))))

    print(jsonpickle.encode(models, unpicklable=False))
