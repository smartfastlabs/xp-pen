import array
import asyncio
import logging
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Awaitable, Callable, Optional
from uuid import UUID, uuid4

import usb.backend.libusb1
import usb.core
import usb.util

VENDOR_ID = 0x28BD
PRODUCT_ID = 0x0202

logger = logging.getLogger("xp-pen")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@dataclass
class Event:
    value: str
    method: str
    uuid: UUID
    timestamp: datetime


class XPPenClient:
    def __init__(
        self,
        on_event: Callable[[Event], Awaitable[Any]],
        **kwargs,
    ) -> None:
        self._on_event: Callable[[Event], Awaitable[Any]] = on_event
        self._current_event: Optional[Event] = None

    async def start(self) -> None:
        while True:
            try:
                await self.run()
            except Exception as e:
                logger.info(e)

            await asyncio.sleep(5)

    async def run(self) -> None:
        device = usb.core.find(
            idVendor=VENDOR_ID,
            idProduct=PRODUCT_ID,
        )
        if device is None:
            raise FileNotFoundError("usb not found")

        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)
            logger.info("kernel driver detached")
        else:
            logger.info("no kernel driver attached")

        usb.util.claim_interface(device, 0)
        endpoint = device[0][(0, 0)][0]
        is_flushing_old_messages: bool = True
        while True:
            try:
                data: array.array = device.read(endpoint.bEndpointAddress, 100, 100)
                button_value = str(data[1] << 8 | data[2])
                if is_flushing_old_messages:
                    logger.info("USB STALE MESSAGE: %s", button_value)
                else:
                    self._current_event = await self._process_input(button_value)
                    if self._current_event:
                        await self._on_event(self._current_event)

            except usb.core.USBTimeoutError as e:
                if is_flushing_old_messages:
                    is_flushing_old_messages = False
                    logger.info("USB DONE FLUSHING")
                await asyncio.sleep(0.100)

    async def _process_input(self, value: str) -> Optional[Event]:
        method: str = "down"
        event: Optional[Event] = None
        start_time: datetime = datetime.now(UTC)
        if value == "0" and self._current_event and self._current_event.method != "up":
            method = "up"
            value = self._current_event.value
        else:
            if value in ("342", "343"):
                value = "clockwise" if value == "343" else "counter-clockwise"
                method = "scroll"

            elif self._current_event:
                if start_time - timedelta(seconds=0.5) < self._current_event.timestamp:
                    method = "double-down"

        event = Event(
            timestamp=start_time,
            value=value,
            method=method,
            uuid=uuid4(),
        )
        if method not in ("scroll", "up"):
            asyncio.ensure_future(self._check_for_long_press(event))

        if "clockwise" in value and method == "up":
            return

        return event

    async def _check_for_long_press(
        self,
        click: Event,
        delay: float = 0.5,
    ):
        await asyncio.sleep(delay)

        if (
            not self._current_event
            or self._current_event.method == "up"
            or click.uuid != self._current_event.uuid
        ):
            return

        self._current_event.method = "long-down"
        await self._on_event(self._current_event)
