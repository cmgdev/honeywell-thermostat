honeywell-thermostat
====================

This started as a fork from nottings' https://github.com/nottings/python-honeywell-thermostat

Huge thanks to him for the initial code, which honeywell_get.py borrows generously from. 

So far, I've added Heroku config-vars, and a simple HTTP GET.

To execute, either set up a .env file with the properties, or set these as environment variables
* PORT (optional)
* USERNAME - your Total Connect Comfort login id
* PASSWORD - your Total Connect Comfort password
* DEVICE_ID - device id can be obtained by viewing source after logging in to total connect comfort page. It should also be the last part of the URI when visiting the remote control of your thermostat online.
