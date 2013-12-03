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
