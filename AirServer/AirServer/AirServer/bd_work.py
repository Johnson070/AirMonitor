import sqlite3
import datetime

class db_work:
	connect = None
	cursor = None
	connect_to_db = False

	def __init__(self, path_to_db:str='.\AirServer\AirServerDB.db'):
		self.db_name = path_to_db

	def connect(self):
		global connect
		global cursor
		global connect_to_db

		try:
			connect = sqlite3.connect(self.db_name)
			cursor = connect.cursor()
			self.connect_to_db = True
		except:
			print('Failed to connect to db')
			self.connect_to_db = False
			raise Exception('Failed to connect to db')

	def disconnect(self):
		global connect
		global cursor
		global connect_to_db

		try:
			cursor.close()
			connect.close()
			self.connect_to_db = False
		except:
			print('Failed to disconnect from db')
			raise Exception('Failed to disconnect from db')
	
	def remove_nozzle(self, 
				   id:int = None, 
				   state_pump:bool = None, 
				   pressure:int = None, 
				   state_fan:bool = None, 
				   rpm_fan:int = None, 
				   time:datetime = None):
		if self.connect_to_db:
			if not id is None or not state_pump is None or not pressure is None or not state_fan is None or not rpm_fan is None or not time is None:
				dot = False

				queries = ['DELETE FROM nozzles WHERE ']

				if not id is None:
					queries.append('id = {}'.format(id))
					dot = True
				if not state_pump is None:
					if dot:
						queries.append(' AND state_pump = {}'.format(state_pump))
					else:
						queries.append('state_pump = {}'.format(state_pump))
					dot = True
				if not pressure is None:
					if dot:
						queries.append(' AND pressure = {}'.format(pressure))
					else:
						queries.append('pressure = {}'.format(pressure))
					dot = True
				if not state_fan is None:
					if dot:
						queries.append(' AND state_fan = {}'.format(state_fan))
					else:
						queries.append('state_fan = {}'.format(state_fan))
					dot = True
				if not rpm_fan is None:
					if dot:
						queries.append(' AND rpm_fan = {}'.format(rpm_fan))
					else:
						queries.append('rpm_fan = {}'.format(rpm_fan))
					dot = True
				if not time is None:
					if dot:
						queries.append(' AND time = {}'.format(time))
					else:
						queries.append('time = {}'.format(time))
					dot = True

				query = ''

				for part in queries:
					query += part

				try:
					cursor.execute(query)
					connect.commit()
				except:
					print('Error delete values in db')
					raise Exception('Error delete values in db')
			else:
				print('Need at least one argument')
				raise Exception('Need at least one argument')
		else:
			print('Need connect to the db')
			raise Exception('Need connect to the db')

	def add_nozzle(self, 
				id:int, 
				state_pump:bool, 
				pressure:int, 
				state_fan:bool, 
				rpm_fan:int, 
				time:datetime):
		if self.connect_to_db:
			data = (id, state_pump, pressure, state_fan, rpm_fan, time)

			try:
				cursor.execute('INSERT INTO nozzles VALUES(?, ?, ?, ?, ?, ?)', data)
				connect.commit()
			except Exception as ex:
				print(ex)
				raise Exception(ex)
		else:
			print('Need connect to the db')
			raise Exception('Need connect to the db')

	def add_sensor(self, 
				id:int, 
				type:str, 
				value:int, 
				time:datetime=datetime.datetime.now()):
		if self.connect_to_db:
			data = (id, value, type, time)

			try:
				cursor.execute('INSERT INTO sensors VALUES(?, ?, ?, ?)', data)
				connect.commit()
			except Exception as ex:
				print(ex)
				raise Exception(ex)
		else:
			print('Need connect to the db')
			raise Exception('Need connect to the db')

	def remove_sensor(self, by_id:int=None, by_type:int=None, by_value:int=None, by_time:datetime=None):
		if self.connect_to_db:
			if not by_id is None or not by_value is None or not by_type is None or not by_time is None:
				dot = False

				queries = ['DELETE FROM sensors WHERE ']

				if not by_id is None:
					queries.append('id = {}'.format(by_id))
					dot = True
				if not by_value is None:
					if dot:
						queries.append(' AND value = {}'.format(by_value))
					else:
						queries.append('value = {}'.format(by_value))
					dot = True
				if not by_type is None:
					if dot:
						queries.append(' AND type = "{}"'.format(by_type))
					else:
						queries.append('type = "{}"'.format(by_type))
					dot = True
				if not by_time is None:
					if dot:
						queries.append(' AND time = "{}"'.format(by_time))
					else:
						queries.append('time = "{}"'.format(by_time))
					dot = True

				query = ''

				for part in queries:
					query += part

				try:
					cursor.execute(query)
					connect.commit()
				except:
					print('Error delete values in db')
					raise Exception('Error delete values in db')
			else:
				print('Need at least one argument')
				raise Exception('Need at least one argument')
		else:
			print('Need connect to the db')
			raise Exception('Need connect to the db')

if __name__ == '__main__':
	db = db_work()

	db.connect()
	db.add_sensor(0,'hum',55, datetime.datetime.now())
	db.add_sensor(1,'hum',52)
	db.remove_sensor(by_value = 52)
	db.add_nozzle(0, False, 1001, False, 100, datetime.datetime.now())
	db.add_nozzle(1, False, 1001, False, 100, datetime.datetime.now())
	db.add_nozzle(3, False, 1001, False, 100, datetime.datetime.now())
	db.remove_nozzle(0)
	db.disconnect()

	#db.remove_sensor(0,'hum',55)



