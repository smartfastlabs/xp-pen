***THIS REPOSITORY IS NOT ASSOCIATED WITH XP-PEN IN ANY WAY***
--------------------------------------------------------------

Summary:
--------
I was on a mission to build a remote for my house, after a bunch of research I found the [XP Pen ACK05 Wireless Shortcut Remote](https://www.amazon.com/ACK05-Wireless-Bluetooth-Programmable-Customized/dp/B0BVW3S1QR), it is very cool!

![image](https://github.com/user-attachments/assets/318ddcfb-1a94-48fc-a8e4-303b093bf31d)

I'm already using [Home Assistant](https://www.home-assistant.io/) and some other stuff, but I couldn't figure out how to connect the remote. So here we are 🤷‍♂️.


Installation:
-------------
  
```
pip install xp-pen
```

Usage:
--------------

**YOU MUST USE THE USB "DONGLE", BLUETOOTH DOES NOT WORK**

See [examples](https://github.com/smartfastlabs/xp-pen/tree/main/examples).

There are 5 *methods* and event can have:

- down
- up
- scroll
- double-down (Click within .5 seconds of the previous)
- long-down (Down for more than 1 second)

Every event has a value, this corresponds to the button pressed.  See key map below:

<img width="1718" alt="image" src="https://github.com/user-attachments/assets/c1cb42a7-918b-4efb-ba70-b09ce3c78fda">


License:
--------
See LICENSE
