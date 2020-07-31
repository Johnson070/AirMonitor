import smbus
import time
import os

bus = smbus.SMBus(1)
count = 0 #int(input('Введите кол-во датчиков: '))
count_limit = 50
count_while = 0
max_sensors = 0
map_i2c = {}
map_i2c_old = {}

def get_sensors_map():
	global bus
	global map_i2c
	global map_i2c_old

	map_i2c_old = map_i2c.copy()
	map_i2c = {}

	for i in range(0x03, 0x78):
		try:
			bus.read_byte(i)
			map_i2c[i] = True
		except:
			map_i2c[i] = False

def set_sensor_random_addr(addr, startAddr):
	global bus

	try:
		bus.write_i2c_block_data(addr, 0xfc, [startAddr])
	except:
		pass

def set_sensors_default_addr():
	global bus

	for i in range(0x03, 0x78):
		try:
			bus.write_i2c_block_data(i, 0xfe, [])
		except:
			pass

def set_sensors_new_addr(startAddr = 0x03):
	global bus

	for i in range(0x03,0x78):
		try:
			bus.write_i2c_block_data(i,0xfc,[startAddr])
		except:
			pass

def get_sensors_count(set_new_addr:bool = False):
	global bus
	count_sensors = 0

	for i in range(0x03, 0x78):
		ex = 1
		try:
			bus.read_byte(i)
		except OSError as e:
			ex = e.args[0]
		finally:
			if  ex == 1:
				count_sensors += 1

	if set_new_addr:
		set_sensors_new_addr()

	return count_sensors

def set_sensors_addr_ascending(get_count:bool = False):
	global bus

	count = 0
	addr = 0x03
	for i in range(0x03, 0x78):
		try:
			bus.write_i2c_block_data(i,0xfd,[addr])
			addr += 1
			count += 1
		except:
			pass

	if get_count:
		return count

def get_addr_changed():
	global bus
	global map_i2c
	global map_i2c_old

	get_sensors_map()

	chg_addr = []

	for addr in range(0x03,0x78):
		if map_i2c_old.get(addr) != map_i2c.get(addr):
			chg_addr.append(addr)
	#print(chg_addr)
	get_sensors_map()
	#print(map_i2c)
	#print(map_i2c_old)
	return chg_addr

def print_addr():
	global bus
	print('\t00\t01\t02\t03\t04\t05\t06\t07\t08\t09\ta\tb\tc\td\te\tf')
	for i in range(0x00,0x80):
		if i % 16 == 0:
			print()
			print(hex(i) + str(':\t'),end='')
		try:
			bus.read_byte(int(i))
			print(str('\u001b[41m')+str(i) + str('\u001b[40m'),end='')
			print('\t',end='')
		except:
			print('--\t',end='')

	print()
	print('=================================================================================================')

set_sensors_default_addr()
get_sensors_map()


new_sensors = True
iter_seekers = 3

while new_sensors:
	count = get_sensors_count()

	find_seekers = False

	for i in range(0x03,0x03+count):
		set_sensor_random_addr(i, i+count+1)

		time.sleep(0.08)

		list_chg = get_addr_changed()

		if len(list_chg) > 2:
			find_seekers = True

		get_sensors_map()
		#print_addr()
		set_sensors_addr_ascending()
		get_sensors_map();

	if find_seekers:
		if iter_seekers == 0:
			iter_seekers += 1
	else:
		if iter_seekers == 0:
			new_sensors = False
		else:
			iter_seekers -= 1

	#print_addr()
	#print('-------------------------')

try:
	out = []
	out.append(get_sensors_count())

	for i in range(0x03,0x78):
		try:
			uid_len = bus.read_byte_data(i,0x02)
			uid = bus.read_i2c_block_data(i, 0x02,uid_len+1)

			text = ''

			for i in range(1, uid_len+1):
				text += chr(uid[i])
			out.append(text)

		except:
			pass

	print(out)
finally:
	bus.close()
