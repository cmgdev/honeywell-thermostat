#!/usr/bin/env python

import datetime
import time
import requests
import sys
import web
import os

urls = (
    '/', 'index'
)

# Login information for Total Connect Comfort web site
USERNAME=os.environ.get('USERNAME')
PASSWORD=os.environ.get('PASSWORD')
DEVICE_ID=os.environ.get('DEVICE_ID')

AUTH="https://rs.alarmnet.com/TotalConnectComfort/"

def get_data():

    retries=5
    auth={
        'timeOffset': 240,
        'UserName': USERNAME,
        'Password': PASSWORD,
        'RememberMe': 'false'
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Host': 'rs.alarmnet.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://rs.alarmnet.com/TotalConnectComfort'
    }
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
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
    r = s.post('https://rs.alarmnet.com/TotalConnectComfort', params=auth, headers=headers)
    r.raise_for_status()

    # Validate
    r = s.get('https://rs.alarmnet.com/TotalConnectComfort/Device/Control/' + DEVICE_ID, headers=headers)
    r.raise_for_status()

    # Get Status
    r = s.get('https://rs.alarmnet.com/TotalConnectComfort/Device/CheckDataSession/' + DEVICE_ID+'?_='+str(utc_seconds), headers=headers2)
    r.raise_for_status()

    return r

class index:
    def GET(self):
        return get_data().text

if __name__ == "__main__":
    app = web.application(urls, globals())
    port = int(os.environ.get('PORT', 8080))
    app.run()
