#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import jinja2
import csv
from my_devices import nxos1,nxos2
from netmiko import ConnectHandler
csv_file = 'bgp.csv'
with open(csv_file) as f:
	read_csv = csv.DictReader(f)
	#csv to dictionary conversion 
	print(read_csv)
	for bgp_vars in read_csv:
		
		advertised_routes = bgp_vars['advertised_routes']
	
#splitting the bgp advertised routes as it is together in the csv file
		advertised_routes = advertised_routes.split()
	
		bgp_vars['advertised_routes'] = advertised_routes
		 
		output = bgp_vars['advertised_routes']
#splitting the bgp advertised routes
		
		if bgp_vars['device_name'] == 'sw1':
			nxos1['my_var1'] = bgp_vars
			#condition to select nxos1
		if bgp_vars['device_name'] == 'sw2':
			nxos2['my_var1'] = bgp_vars
			#condition to select nxo2

#appending the config files  for nxos1 and nxos2 respectively

	for devices in nxos1,nxos2:
		tmp_device = devices.copy()
		
		topsy = tmp_device.pop('my_var1')
#exposes the config files according to nxos1 and nxos2
		
		template_file = 'bgp_cond_j2.j2'
		
		with open(template_file) as f:
			output = f.read()

#JINJA2 templating
		new_output = jinja2.Template(output)
		
		print('-'*80)
		new_output1 = (new_output.render(topsy))


#converting the JINJA2 output to device configuration format
		for new_output1 in [new_output1.strip()]:
			output2 = new_output1.splitlines()
			print(output2)
	
		net_connect = ConnectHandler(**tmp_device)
		#print(net_connect.base_prompt)
		output3 = net_connect.send_config_set(output2)
		
		print(output3)
