import trio
import requests
import functools
from datetime import datetime, date, timezone, timedelta
from typing import Union, List

from loguru import logger


def _parse_dict_datetime(d: dict) -> datetime:
    offset: str = d['zoneOffset']
    hours, minutes = (int(x) for x in offset.split(':'))
    dt = datetime.fromisoformat(f"{d['date']} {d['time']}")
    return dt.replace(tzinfo=timezone(timedelta(hours=hours, minutes=minutes)))

class CPostEvent:
    def __init__(self, data: dict):
        self._data = data

    @property
    def code(self) -> str:
        return self._data['cd']

    @property
    def web_code(self) -> str:
        return self._data['webCd']

    @property
    def datetime(self) -> datetime:
        return _parse_dict_datetime(self._data['datetime'])

    @property
    def description(self) -> str:
        return self._data['descEn']

    @property
    def address(self) -> Union[str | None]:
        loc = self._data['locationAddr']
        if loc['city'] == '' or loc['regionCd'] == '':
            return None

        return f"{loc['city']}, {loc['regionCd']}"

    @property
    def type(self) -> str:
        return self._data['type']

    @property
    def retail_name(self) -> Union[str | None]:
        if 'retailNmEn' in self._data:
            return self._data['retailNmEn']

    @property
    def retail_location_id(self) -> Union[str | None]:
        if 'retailLocationId' in self._data:
            return self._data['retailLocationId']

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __gt__(self, other):
        return self.datetime > other.datetime

    def __str__(self):
        s = f'<Event {self.type} | {self.description}'
        s += f' | {self.datetime}'

        if self.address:
            s += f' | {self.address}'
        s += '>'
        return s

class CPostDetails:
    def __init__(self, json: dict):
        self._data = json

    @property
    def pin(self) -> int:
        return int(self._data['pin'])

    @property
    def shipper_name(self) -> str:
        return self._data['custNm']

    @property
    def shipper_city(self) -> str:
        return self._data['addtnlOrigInfo']

    @property
    def destination_city(self) -> str:
        return self._data['addtnlDestInfo']

    @property
    def delivery_type(self) -> str:
        return f"{self._data['deliveryOptions'][0]['descEn']} via {self._data['productNmEn']}"

    @property
    def product_number(self) -> int:
        return int(self._data['productNbr'])

    @property
    def status(self):
        return self._data['status']

    @property
    def shipped_datetime(self) -> datetime:
        return _parse_dict_datetime(self._data['shippedDateTime'])

    @property
    def events(self) -> List[CPostEvent]:
        events = []
        for event_data in self._data['events']:
            events.append(CPostEvent(event_data))

        return events

    @property
    def delivery_date(self) -> Union[date | None]:
        if 'actualDlvryDate' in self._data:
            return date.fromisoformat(self._data['actualDlvryDate'])

    @property
    def attempted_delivery_date(self) -> date:
        if 'attemptedDlvryDate' in self._data:
            return date.fromisoformat(self._data['attemptedDlvryDate'])

    @property
    def accepted_date(self) -> date:
        return date.fromisoformat(self._data['acceptedDate'])

    @property
    def expected_delivery_date(self) -> date:
        return date.fromisoformat(self._data['expectedDlvryDateTime']['dlvryDate'])

async def request_details(pin: int, proxies: Union[dict | None] = None) -> CPostDetails:
    response: requests.Response = await trio.to_thread.run_sync(functools.partial(requests.get,
        url=f'https://www.canadapost-postescanada.ca/track-reperage/rs/track/json/package/{pin}/detail',
        proxies=proxies
    ))

    data = response.json()
    logger.debug(data)
    if 'error' in data:
        raise ValueError(data['error']['descEn'])

    return CPostDetails(data)
