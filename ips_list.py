import nmap # import nmap.py module
nm = nmap.PortScanner() # instantiate nmap.PortScanner object
nm.scan('192.168.1.0', '22-443') # scan host 127.0.0.1, ports from 22 to 443


# a more usefull example :
for host in nm.all_hosts():
	print('----------------------------------------------------')
	print('Host : %s (%s)' % (host, nm[host].hostname()))
	print('State : %s' % nm[host].state())