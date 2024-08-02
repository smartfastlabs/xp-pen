import asyncio
import json
from typing import Optional

import httpx

from xp_pen import Event, XPPenClient

HOMEASSISTANT_TOKEN = "YOUR HOMEASSISTANT TOKEN"


async def set_brightness(entity_id: str, value: int):
    return await make_request(
        f"services/light/turn_on",
        payload={"entity_id": entity_id, "brightness": value},
    )


async def make_request(
    url: str, payload: Optional[dict] = None, method: str = "post"
) -> dict:
    url = f"http://homeassistant.local:8123/api/{url}"
    headers = {
        "Authorization": f"Bearer {HOMEASSISTANT_TOKEN}",
        "content-type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        kwargs = {
            "headers": headers,
        }

        if payload is not None:
            kwargs["data"] = json.dumps(payload)

        response = await getattr(client, method)(url, **kwargs)

        return response.json()


async def on_event(event: Event):
    print(f"[XP Pen] EVENT: {event.method}:{event.value}")
    if event.method == "down":
        if event.value == "0":
            print(await set_brightness("light.living_area_lights", 0))

    elif event.method == "double-down":
        if event.value == "0":
            await set_brightness("light.living_area_lights", 255)

    elif event.method == "long-down":
        if event.value == "0":
            await set_brightness("light.living_area_lights", 45)

    elif event.method == "scroll":
        if event.value == "clockwise":
            await set_brightness("light.living_area_lights", 155)


if __name__ == "__main__":
    client = XPPenClient(on_event)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start())
