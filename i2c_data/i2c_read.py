import smbus,argparse

parser = argparse.ArgumentParser(usage='i2c_read.py -n [num]')

parser.add_argument('-n', metavar='3',required=True, help='Address I2C', default=3, action='store', dest='addr')
parser.add_argument('-uid', action='store_true', default=False, dest='uid', help='Get UID sensor')
parser.add_argument('-sen', action='store_true', default=False, dest='count', help='Get count sensors in module')
parser.add_argument('-cli', metavar='0',action='store', default=False, dest='climate', help='Get temperature and humidity')

options = parser.parse_args()

addr = int(options.addr) #int(input('Введите номер канала(0x03 - 0x77): '))
bus = smbus.SMBus(1)

try:
	out = []

	if options.count:
		len_data = bus.read_byte_data(addr, 0x01)
		data = bus.read_i2c_block_data(addr, 0x01, len_data+1)

		text = ''
		for i in range(1, len_data+1):
			text += chr(data[i])
		out.append(text)
	if options.uid:
		len_uid = bus.read_byte_data(addr, 0x02)
		uid = bus.read_i2c_block_data(addr, 0x02, len_uid+1)

		text = ''
		for i in range(1, len_uid+1):
			text += chr(uid[i])

		out.append(text)
	if options.climate:
		request = 0x04
		if int(options.climate) == 0:
			request = 0x03

		len_dht = bus.read_byte_data(addr, request)
		dht = bus.read_i2c_block_data(addr, request, len_dht+1)

		text = ''
		for i in range(1, len_dht+1):
			if i == 3 or i == 7:
				text += '.'
			elif i == 5:
				text += ' '
			text += chr(dht[i])

		out.append(text)

	print(out)
finally:
	bus.close()
