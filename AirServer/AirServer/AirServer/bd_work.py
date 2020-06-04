import sqlite3
import datetime
from pymongo import cursor

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

	def add_nozzle(self, id:int, state_pump:bool, pressure:int, state_fan:bool, rpm_fan:int, time:datetime):
		if self.connect_to_db:
			data = (id, state_pump, pressure, state_fan, rpm_fan, time)

			try:
				cursor.execute('INSERT INTO nozzles VALUES(?, ?, ?, ?, ?, ?)', data)
				connect.commit()
			except:
				print('Error insert values in db')
		else:
			print('Need connect to the db')

	def add_sensor(self, id:int, type:str, value:int, time:datetime=datetime.datetime.now()):
		if self.connect_to_db:
			data = (id, value, type, time)

			try:
				cursor.execute('INSERT INTO sensors VALUES(?, ?, ?, ?)', data)
				connect.commit()
			except:
				print('Error insert values in db')
		else:
			print('Need connect to the db')

	def remove_sensor(self, by_id:int=None, by_type:int=None, by_value:int=None, by_time:datetime=None):
		if self.connect_to_db:
			if not by_id is None or not by_value is None or not by_type is None or not by_time is None:
				data = (by_id, by_value, by_type, by_time)

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
					print(query)
					cursor.execute(query)
					connect.commit()
				except:
					print('Error delete values in db')
			else:
				print('Need at least one argument')
		else:
			print('Need connect to the db')

if __name__ == '__main__':
	db = db_work()

	db.connect()
	db.add_sensor(0,'hum',55, datetime.datetime.now())
	db.add_sensor(1,'hum',52)
	db.remove_sensor(by_value = 52)
	db.add_nozzle(0, False, 1000, False, 100, datetime.datetime.now())
	db.disconnect()

	#db.remove_sensor(0,'hum',55)



