import sqlite3
import datetime

class db_work:
	def __init__(self):
		pass

	def add_value_sensor(self):
		connect = sqlite3.connect('.\AirServerDB.db')

		cursor = connect.cursor()

		data = \
		[
			(1, 23, 'temp', str(datetime.datetime.now())),
			(2, 55, 'hum', str(datetime.datetime.now()))
		]

		#try:
		cursor.executemany('INSERT INTO sensors VALUES(?, ?, ?, ?)', data)
		#except:
		#	cursor.execute('UPDATE INTO sensors VALUES(?, ?, ?, ?)', data)

		for row in cursor.execute("SELECT rowid, * FROM sensors"):
			print(row)

		#cursor.execute('DELETE FROM sensors WHERE value = 55')
		#cursor.execute('DELETE FROM sensors WHERE value = 23')
		#cursor.execute('UPDATE sensors SET id = 2 WHERE id = 1')

		connect.commit()

		cursor.close()
		connect.close()

if __name__ == '__main__':
	db = db_work()

	db.add_value_sensor()



