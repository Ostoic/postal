import functools
import os
import sys
from base64 import b64encode
from datetime import timedelta

import trio
from loguru import logger
from postal import cpost
from typing import List


async def log_request(pin, proxies):
    details = await cpost.request_details(pin=pin, proxies=proxies)
    logger.info(f'{details.pin=}')
    logger.info(f'{details.status=}')
    logger.info(f'{details.shipper_name=}')
    logger.info(f'{details.shipper_city=}')
    logger.info(f'{details.delivery_type=}')
    logger.info(f'{details.accepted_date=}')
    logger.info(f'{details.delivery_date=}')

    for event in details.events:
        logger.debug(f'{str(event)}')

    return details.events[0] if len(details.events) > 0 else None

async def monitor_pin(nursery, pin: int):
    proxy_addr = 'socks5://server:9050'
    proxies = dict(http=proxy_addr, https=proxy_addr)
    previous_event = None

    while True:
        try:
            latest_event = await log_request(pin, proxies)
            if str(latest_event) != str(previous_event):
                previous_event = latest_event
                cmd64 = b64encode(f'notify-send -t {30 * 1000} -a "postal [{pin}]" \'{str(latest_event)}\''.encode()).decode()
                logger.info(f'{cmd64=}')
                nursery.start_soon(
                    trio.to_thread.run_sync,
                    functools.partial(os.system, f'echo {cmd64} | base64 -d | sh')
                )

                nursery.start_soon(
                    trio.to_thread.run_sync,
                    functools.partial(os.system, f'ssh owner@desktop \'echo {cmd64} | base64 -d | sh\'')
                )

        except Exception as e:
            logger.exception(e)

        await trio.sleep(timedelta(minutes=5).seconds)

async def main():
    if len(sys.argv) == 1:
        raise ValueError('No pin specified')

    pins = [int(sys.argv[1]), ]
    async with trio.open_nursery() as n:
        for pin in pins:
            n.start_soon(monitor_pin, n, pin)

trio.run(main)
