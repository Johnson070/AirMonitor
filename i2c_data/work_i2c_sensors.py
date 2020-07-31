import time,smbus,argparse,subprocess,ast

bus = smbus.SMBus(1)


try:
	if __name__ == '__main__':
		parser = argparse.ArgumentParser(usage = "work_i2c_sensors.py [options]")
		parser.add_argument('-n', help='Setting addresses I2C sensors', action='store_true', dest='search', default=False)
		
		sensor_group = parser.add_argument_group('Sensor get data')
		sensor_group.add_argument('-s',metavar='3', default=False, action='store',dest='addr', help='I2C address sensor')
		sensor_group.add_argument('-uid', action='store_true', default=False, dest='uid', help='Get UID sensor')
		sensor_group.add_argument('-sen', action='store_true', default=False, dest='count', help='Get count sensors in module')
		sensor_group.add_argument('-cli', metavar='0',action='store', default=False, dest='climate', help='Get temperature and humidity')

		sensors_group = parser.add_argument_group('Get sensors data')
		sensors_group.add_argument('--sensors', action='store_true', default=False, dest='sensors', help="Get sensors UID's")



		options = parser.parse_args()

		if options.search:
			set_sensors = subprocess.Popen(['python3','set_i2c_addr.py'], stdout=subprocess.PIPE)
			data = ast.literal_eval(set_sensors.communicate()[0].decode("utf-8"))
			print(data)
		elif options.sensors:
			uids = []

			for i in range(0x03,0x78):
				try:
					uid_len = bus.read_byte_data(i,0x02)
					uid = bus.read_i2c_block_data(i,0x02,uid_len+1)

					text = ''
					for j in range(1,uid_len+1):
						text += chr(uid[j])
					uids.append(text)
				except:
					pass
			print(uids)

		elif options.addr:
			cmd_list = ['python3', 'i2c_read.py', '-n', str(options.addr)]

			if options.uid:
				cmd_list.append('-uid')
			if options.climate:
				cmd_list.append('-cli')
				cmd_list.append(str(options.climate))
			if options.count:
				cmd_list.append('-sen')

			get_sensor = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
			data = ast.literal_eval(get_sensor.communicate()[0].decode("utf-8"))
			print(data)
finally:
	bus.close()
