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

Basic Usage:
------------

```
import asyncio

from xp_pen import Event, XPPenClient


async def on_event(event: Event):
    print(f"[XP Pen] EVENT: {event.method}:{event.value}")


if __name__ == "__main__":
    client = XPPenClient(on_event)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start())
```

Home Assistant API

License:
--------
See LICENSE
