import datetime
import jsonpickle

class atomizer:
    def __init__(self, state_pump: bool, pressure: int, time: datetime, state_fan: bool, rpm_fan: int):
        self.state_pump = state_pump
        self.pressure = pressure
        self.time = time
        self.state_fan = state_fan
        self.rpm_fan = rpm_fan


class nozzle:
    def __init__(self, id: int, state_pump: bool, pressure: int, time: datetime, state_fan: bool, rpm_fan: int):
        self.id = id
        self.state_pump = state_pump
        self.pressure = pressure
        self.time = time
        self.state_fan = state_fan
        self.rpm_fan = rpm_fan


class sensor:
    def __init__(self, id: int, type: str, value: int, time: datetime):
        self.id = id
        self.type = type
        self.value = value
        self.time = time

    def to_json(self):
        return {"id": self.id, "value": self.value, "time": str(self.time).replace(" ", "T")}


class model:
    def __init__(self, sensors: list = [], atomizer_device: atomizer = None, nozzles: list = []):
        self.sensors: list = sensors
        self.atomizer: atomizer = atomizer_device
        self.nozzles: list = nozzles

    def add_sensor(self, sensor):
        if not sensor is str:
            sensor = jsonpickle.decode(jsonpickle.encode(sensor, unpicklable=False))

        math_id = False

        for sensor_for in self.sensors:
            if sensor_for['id'] == sensor['id']:
                math_id = True

        if not math_id:
            self.sensors.append(sensor)
        else:
            new_sensors = [old_sensor for old_sensor in self.sensors if sensor['id'] != old_sensor['id']]
            new_sensors.append(sensor)
            self.sensors = new_sensors

    def delete_sensor(self, id: int):
        for i in range(0, len(self.sensors)):
            if self.sensors[i].id == id:
                del self.sensors[id]

    def add_nozzle(self, nozzle):
        if not nozzle is str:
            nozzle = jsonpickle.decode(jsonpickle.encode(nozzle, unpicklable=False))

        math_id = False

        for nozzle_for in self.nozzles:
            if nozzle_for['id'] == nozzle['id']:
                math_id = True

        if not math_id:
            self.nozzles.append(nozzle)
        else:
            new_nozzles = [old_nozzle for old_nozzle in self.nozzles if nozzle['id'] != old_nozzle['id']]
            new_nozzles.append(nozzle)
            self.nozzles = new_nozzles

    def delete_nozzle(self, id: int):
        for i in range(0, len(self.nozzles)):
            if self.nozzles[i].id == id:
                del self.nozzles[id]


if __name__ == '__main__':
    models = model()

    models.add_sensor(sensor(0,'temp', 100, datetime.datetime.now()))
    models.add_sensor(sensor(1,'temp', 20, datetime.datetime.now()))
    models.add_sensor(sensor(0,'temp', 20, datetime.datetime.now()))

    print(jsonpickle.encode(models, unpicklable=False))


    models.add_nozzle(nozzle(0, False, 1000, datetime.datetime.now(), False, 100))
    models.add_nozzle(nozzle(1, False, 1000, datetime.datetime.now(), False, 100))
    models.add_nozzle(nozzle(0, False, 1000, datetime.datetime.now(), False, 100))

    print(jsonpickle.encode(models, unpicklable=False))
