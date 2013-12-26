Simple Home Automation Message Bus
==================================

This project aims to be a simple, lightweight message bus to be used
in home automation projects. It is written in Python 2.7 and should
be able to run on a server or Raspberry Pi, Arduino Yun, Beaglebone, etc.

Messages are broken down into two broad categories: Events and Commands

Messages contain a timestamp, source, type and a payload. Command messages may
also specify a target. Message payloads should be modeled after JSON with
maps containing primitive types, lists and nested maps.

Things (sensors, services, etc) should publish events, such as a sensor reading
or that an action has occurred. Listeners can subscribe to events based on their
type, source, etc. Listeners can then perform rules or send out subsequent
events or commands.

This is still very much a work in progress.

Prerequesites
-----------

- The Flask framework ("pip install flask")
- The Python Xively client (optional)

Usage
-----

There are two sample scripts:

main.py - Starts the mesage bus, sends a sample message and then shuts down

web_main.py - Starts up the message bus and a flask server. Provides a web
interface for posting new Events and logs them to a file.