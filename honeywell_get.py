#!/usr/bin/env python

import datetime
import time
import requests
import sys
import web
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import yaml

urls = (
    '/', 'index',
    '/temps', 'temps',
    '/saveTemps', 'saveTemps'
)

# Login information for Total Connect Comfort web site
USERNAME=os.environ.get('USERNAME')
PASSWORD=os.environ.get('PASSWORD')
DEVICE_ID=os.environ.get('DEVICE_ID')
TEMPS_URL=os.environ.get('TEMPS_URL')
AUTH=os.environ.get('AUTH')
MQTT_HOST=os.environ.get('MQTT_HOST')
MQTT_PORT=os.environ.get('MQTT_PORT')
MQTT_TOPIC=os.environ.get('MQTT_TOPIC')
MQTT_USER=os.environ.get('MQTT_USER')
MQTT_PASS=os.environ.get('MQTT_PASS')

def get_data():

    retries=5
    auth={
        'timeOffset': 360,
        'UserName': USERNAME,
        'Password': PASSWORD,
        'RememberMe': 'false'
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Host': 'rs.alarmnet.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://rs.alarmnet.com/TotalConnectComfort/'
    }
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Host': 'rs.alarmnet.com',
        'Referer': 'https://rs.alarmnet.com/TotalConnectComfort/Device/Control/'+DEVICE_ID,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    s = requests.Session()
    t = datetime.datetime.now()
    utc_seconds = (time.mktime(t.timetuple()))
    utc_seconds = int(utc_seconds*1000)

    # Login
    r = s.post(AUTH, params=auth, headers=headers)
    r.raise_for_status()

    # Validate
    r = s.get(AUTH + '/Device/Control/' + DEVICE_ID, headers=headers)
    r.raise_for_status()

    # Get Status
    r = s.get(AUTH + '/Device/CheckDataSession/' + DEVICE_ID+'?_='+str(utc_seconds), headers=headers2)
    r.raise_for_status()

    return r

class index:
    def GET(self):
        return get_data().text

class saveTemps:
    def GET(self):
        temps = get_data().text
        print temps
        r = requests.post(TEMPS_URL, data={'json' : temps})
		
		d = yaml.load(temps)
		temp = str(d['latestData']['uiData']['DispTemperature'])
		humid = str(d['latestData']['uiData']['IndoorHumidity'])

		# save to mqtt broker
		client = mqtt.Client("thermostat-client", clean_session=False, protocol=mqtt.MQTTv31)
		client.username_pw_set(MQTT_USER, MQTT_PASS);
		client.connect(MQTT_HOST, port=MQTT_PORT)
		client.publish(MQTT_TOPIC + "/temperature", payload=temp, retain=True)
		client.disconnect()
		
		client.connect(MQTT_HOST, port=MQTT_PORT)
		client.publish(MQTT_TOPIC + "/humidity", payload=humid, retain=True)
		
		client.disconnect()
		
        return r.text
        
class temps:
    def GET(self):
        getMonth = time.strftime("%B", time.localtime())
        getYear = time.strftime("%Y", time.localtime())
        input = web.input(month=getMonth,year=getYear)

        getMonth = input.month
        getYear = input.year

        s = requests.Session()
        r = s.get(TEMPS_URL + "?month=" + getMonth + "&year=" + getYear)
        return r.text

if __name__ == "__main__":
    app = web.application(urls, globals())
    port = int(os.environ.get('PORT', 8080))
    app.run()
