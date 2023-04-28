# Connect to BYU AV couchdb and pull data
# couchdb is at: https://couchdb-prd.avs.byu.edu/
# get the 'devices' table
# get the devices that its id ends in D1
# from the docs, get the 'type' "_id"
# from the docs get the 'ports', count them
# create a csv file with the following columns:
#   device_id, device_type, number_of_ports
#   ASB-A203-D1,   SonyXBR,        48

import couchdb
import csv
import os
import sys

couch_url = '@couchdb-prd.avs.byu.edu/'

user = sys.argv[1]
password = sys.argv[2]

couch_server = 'https://' + user + ':' + password + couch_url

# connect to couchdb
print('Connecting to couchdb...')
couch = couchdb.Server(couch_server)
db = couch['devices']

# get all devices
print('Getting all devices...')
devices = db.view('_all_docs', include_docs=True)
print('Number of devices: ', len(devices))

# get all devices that end in D1
print('Getting all devices that end in D1...')
d1_devices = []
for device in devices:
    if device['id'].endswith('-D1'):
        d1_devices.append(device)
print('Number of D1 devices: ', len(d1_devices))
video_switchers = {video_switchers['id']: video_switchers['doc'] for video_switchers in devices}

# from the 'device_types' table get the number of ports available for each device types to into a map
db2 = couch['device_types']
device_types = db2.view('_all_docs', include_docs=True)
device_types = {device_type['id']: device_type['doc'] for device_type in device_types}

# create csv file
print('Creating csv file...')
csv_file = open('av_inputs.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Room Name', 'D1 Device', 'Available Ports in D1', 'Has SW1', 'Available Ports in SW1'])

# get device type and number and available ports
print('Getting device type, switcher, and available ports ...')
for device in d1_devices:
    room_name = device['id'][:-3]
    device_type = device['doc']['type']['_id']
    device_ports = 0
    available_ports = len(device_types[device_type]['ports'])
    
    if 'ports' in device['doc']:
        device_ports = len(device['doc']['ports'])
        for port in device['doc']['ports']:
            # check if port has a source and destination device
            if 'source_device' in port and 'destination_device' in port:
                continue
            else:
                device_ports -= 1
        device_ports = available_ports - device_ports        
    else:
        device_ports = available_ports
    
    # check if room has a switcher and get available ports
    has_sw1 = False
    sw1_name = room_name + '-SW1'
    
    if sw1_name in video_switchers:
        has_sw1 = True
        available_sw1_ports = 0
        for port in video_switchers[sw1_name]['ports']:
            # if port is input, add to available ports
            if "IN" in port['_id']:
                if 'source_device' in port and 'destination_device' in port:
                    continue
                else:
                    available_sw1_ports += 1
            else:
                continue


    csv_writer.writerow([room_name, device_type, device_ports, has_sw1, available_sw1_ports])
print('Done!')

csv_file.close()


