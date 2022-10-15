from ast import Raise
from curses import raw
import json
import haversine as hs
import os
import csv

class Packet():
    def __init__(self, packet_path):
        with open(packet_path, 'r') as packet_json:
            self.packet = json.load(packet_json)
        
        if self.packet['type'] == 'uplink':
            self.type = 'uplink'
            self.payload = self.packet['decoded']['payload']
            self.num_hotspots = len(self.packet['hotspots'])
            if self.payload['status'] == 'GPS':
                self.status = self.payload['status']
                self.altitude = self.payload['altitude']
                self.battery = self.payload['battery']
                self.humidity = self.payload['humidity']
                self.lat = self.payload['latitude']
                self.long = self.payload['longitude']
                self.minutes_lost = self.payload['minutes_lost']
                self.pressure = self.payload['pressure']
                self.sats = self.payload['sats']
                self.speed = self.payload['speed']
                self.temperature = self.payload['temperature']
                self.uptime = self.payload['uptime']
                self.uv = self.payload['uv']
            elif self.payload['status'] == 'LOST GPS':
                self.status = self.payload['status']
                self.battery = self.payload['battery']
                self.humidity = self.payload['humidity']
                self.minutes_lost = self.payload['minutes_lost']
                self.pressure = self.payload['pressure']
                self.temperature = self.payload['temperature']
                self.uptime = self.payload['uptime']
                self.uv = self.payload['uv']
            elif self.payload['status'] == 'BOOTED':
                self.status = self.payload['status']
                self.battery = self.payload['battery']
        else:
            self.type = 'join'

    def list_hotspots(self):
        self.hotspots = []
        for hotspot in self.packet['hotspots']:
            self.hotspots.append({'id': hotspot['id'], 'lat': hotspot['lat'], 'long': hotspot['long'], 'rssi': hotspot['rssi'], 'snr': hotspot['snr']})

        return self.hotspots

    def get_best_hotspots(self):
        self.best_hotspots = []
        for hotspot in self.hotspots:
            if hotspot['rssi'] > -130:
                self.best_hotspots.append(hotspot)
        
        return self.best_hotspots
    
    def get_distance_from(self, loc):
        return hs.haversine((self.lat, self.long), loc)

class Hotspot():
    def __init__(self, hotspot_json):
        self.channel = hotspot_json['channel']
        self.lat = hotspot_json['lat']
        self.long = hotspot_json['long']
        self.name = hotspot_json['name']
        self.rssi = hotspot_json['rssi']
        self.snr = hotspot_json['snr']
        self.spreading = hotspot_json['spreading']
        self.status = hotspot_json['status']
        self.time = hotspot_json['reported_at']


# Get a list of packet jsons
packet_json_list = sorted(list(os.listdir('packets/')))
filename = "gps_path_3d.csv"

fields = ['latitude', 'longitude', 'elevation']
rows = []

for raw_packet_path in packet_json_list:
    packet_path = 'packets/' + raw_packet_path
    packet = Packet(packet_path)
    if packet.type == 'uplink':
        if packet.status == 'GPS':
            rows.append([packet.lat, packet.long, packet.altitude])

with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
     
    # writing the fields
    csvwriter.writerow(fields)
     
    # writing the data rows
    csvwriter.writerows(rows)