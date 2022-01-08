import json
from datetime import date, datetime, timedelta, timezone
from loguru import logger
from postal.cpost import CPostDetails, _parse_dict_datetime

def test_cpost_datetime_parser():
    data = json.loads(r'''{"date":"2021-12-27","time":"14:18:58","zoneOffset":"-05:00"}''')
    dt = _parse_dict_datetime(data)
    logger.debug(f'{dt=}')
    assert dt == datetime(2021, 12, 27, 14, 18, 58, tzinfo=timezone(timedelta(days=-1, seconds=68400)))

def test_cpost_parser():
    text = r'''{"pin":"9440170513551280","productNmEn":"Xpresspost","productNmFr":"Xpresspost","productNbr":"000000000000000908","deliveryOptions":[{"cd":"FlexDelivery","compliance":"NotYetDelivered","descEn":"Flex Delivery","descFr":"FlexiLivraison"}],"status":"InTransit","shippedDateTime":{"date":"2021-12-27","time":"14:18:58","zoneOffset":"-05:00"},"acceptedDate":"2021-12-27","expectedDlvryDateTime":{"dlvryDate":"2022-01-06"},"shipFromAddr":{"addrLn1":"","addrLn2":"","countryCd":"","city":"","regionCd":"","postCd":"5612292e80666fed670b120cfa41b2d7"},"shipToAddr":{"addrLn1":"","addrLn2":"","countryCd":"","city":"","regionCd":"","postCd":"6e7ed1b90001ddc630a967e5cadf56e3"},"events":[{"cd":"1703","webCd":"CODE-829","datetime":{"date":"2021-12-31","time":"06:44:12","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"cc680f0a057387c7fb881251c7709d4b"},"descEn":"Item in transit to Post Office","descFr":"Article en transit au bureau de poste","type":"ToRetail"},{"cd":"0170","webCd":"CODE-446","datetime":{"date":"2021-12-31","time":"06:44:11","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"e999488d9a3fbd1831261b98023bddbb"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0170","webCd":"CODE-446","datetime":{"date":"2021-12-30","time":"10:44:07","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"6d82e8e4f7afbbc0b142e8b3f648a0e3"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0175","webCd":"CODE-850","datetime":{"date":"2021-12-29","time":"19:20:42","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"9952fd51d1b3a4342555cdd0fadba9b0"},"descEn":"Item in transit","descFr":"Article en transit","type":"Info"},{"cd":"0100","webCd":"CODE-446","datetime":{"date":"2021-12-29","time":"12:56:22","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"9952fd51d1b3a4342555cdd0fadba9b0"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0162","webCd":"CODE-603","datetime":{"date":"2021-12-28","time":"20:00:02","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"2f792423c234a148561e3d864be1c9aa"},"descEn":"Delivery may be delayed due to transportation delay","descFr":"La livraison pourrait être retardée en raison d'un retard de transport","type":"Info"},{"cd":"0162","webCd":"CODE-603","datetime":{"date":"2021-12-27","time":"20:00:06","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"2f792423c234a148561e3d864be1c9aa"},"descEn":"Delivery may be delayed due to transportation delay","descFr":"La livraison pourrait être retardée en raison d'un retard de transport","type":"Info"},{"cd":"PR01_RECEIVED","webCd":"CODE-838","datetime":{"date":"2021-12-27","time":"16:44:00","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"fe7f8a34497e70e049433b14ffa4b205"},"descEn":"Item received at originating postal facility","descFr":"Article reçu à l'installation postale d'origine","type":"PrReceived"},{"cd":"3000","webCd":"CODE-020A","datetime":{"date":"2021-12-27","time":"14:18:58","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"","city":"","regionCd":"","postCd":""},"descEn":"Electronic information submitted by shipper","descFr":"Les renseignements électroniques ont été soumis par l'expéditeur","type":"Induction"}],"custNm":"Bill's Electronics","addtnlOrigInfo":"OTTAWA, ON","addtnlDestInfo":"MONTREAL, QC","suppressSignature":false,"lagTime":false,"returnPinIndicator":false,"refundAllowed":false,"dtcBarcode":false,"canadianDest":true,"dlvryInstruction":"","correctedPostalCode":"","sigReqByAmtDue":false,"expectedDlvryWindow":{"dlvryWindowEOD":true},"shipperPostalCode":"","recipientNm":"*****"}'''
    details = CPostDetails(json.loads(text))
    assert details.status == 'InTransit'
    assert details.pin == 9440170513551280
    assert details.delivery_type == 'Flex Delivery via Xpresspost'
    assert details.shipper_name == "Bill's Electronics"
    assert details.shipper_city == 'OTTAWA, ON'
    assert details.accepted_date == date(2021, 12, 27)
    assert details.expected_delivery_date == date(2022, 1, 6)

    logger.debug(f'{details.status=}')
    logger.debug(f'{details.pin=}')
    logger.debug(f'{details.shipper_name=}')
    logger.debug(f'{details.shipper_city=}')
    logger.debug(f'{details.delivery_type=}')
    logger.debug(f'{details.accepted_date=}')
    logger.debug(f'{details.expected_delivery_date=}')
    pickup = details.events[0]
    assert pickup.type == 'ToRetail'
    assert pickup.description == 'Item in transit to Post Office'
    assert pickup.address == 'MONTREAL, ON'

    for event in details.events:
        logger.debug(f'{str(event)}')

    text = r'''{"pin":"2740170516551280","productNmEn":"Xpresspost","productNmFr":"Xpresspost","productNbr":"000000000000000908","deliveryOptions":[{"cd":"FlexDelivery","compliance":"NotYetDelivered","descEn":"Flex Delivery","descFr":"FlexiLivraison"}],"status":"ReadyPickup","shippedDateTime":{"date":"2021-12-27","time":"14:18:58","zoneOffset":"-05:00"},"acceptedDate":"2021-12-27","expectedDlvryDateTime":{"dlvryDate":"2022-01-06"},"shipFromAddr":{"addrLn1":"","addrLn2":"","countryCd":"","city":"","regionCd":"","postCd":"5612292e80666fed670b120cfa41b2d7"},"shipToAddr":{"addrLn1":"","addrLn2":"","countryCd":"","city":"","regionCd":"","postCd":"6e7ed1b90001ddc630a967e5cadf56e3"},"events":[{"cd":"1701","webCd":"CODE-805","datetime":{"date":"2021-12-31","time":"10:24:22","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"cc680f0a057387c7fb881251c7709d4b"},"descEn":"Item available for pickup at Post Office","descFr":"Article peut être ramassé au bureau de poste","retailLocationId":"385964","retailNmEn":"MONTREAL PO","retailNmFr":"MONTREAL PO","dnc":"385964018250","type":"ToRetail"},{"cd":"1703","webCd":"CODE-829","datetime":{"date":"2021-12-31","time":"06:44:12","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"cc680f0a057387c7fb881251c7709d4b"},"descEn":"Item in transit to Post Office","descFr":"Article en transit au bureau de poste","type":"ToRetail"},{"cd":"0170","webCd":"CODE-446","datetime":{"date":"2021-12-31","time":"06:44:11","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"e999488d9a3fbd1831261b98023bddbb"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0170","webCd":"CODE-446","datetime":{"date":"2021-12-30","time":"10:44:07","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"MONTREAL","regionCd":"ON","postCd":"6d82e8e4f7afbbc0b142e8b3f648a0e3"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0175","webCd":"CODE-850","datetime":{"date":"2021-12-29","time":"19:20:42","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"9952fd51d1b3a4342555cdd0fadba9b0"},"descEn":"Item in transit","descFr":"Article en transit","type":"Info"},{"cd":"0100","webCd":"CODE-446","datetime":{"date":"2021-12-29","time":"12:56:22","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"9952fd51d1b3a4342555cdd0fadba9b0"},"descEn":"Item processed","descFr":"Article traité","type":"Info"},{"cd":"0162","webCd":"CODE-603","datetime":{"date":"2021-12-28","time":"20:00:02","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"2f792423c234a148561e3d864be1c9aa"},"descEn":"Delivery may be delayed due to transportation delay","descFr":"La livraison pourrait être retardée en raison d'un retard de transport","type":"Info"},{"cd":"0162","webCd":"CODE-603","datetime":{"date":"2021-12-27","time":"20:00:06","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"2f792423c234a148561e3d864be1c9aa"},"descEn":"Delivery may be delayed due to transportation delay","descFr":"La livraison pourrait être retardée en raison d'un retard de transport","type":"Info"},{"cd":"PR01_RECEIVED","webCd":"CODE-838","datetime":{"date":"2021-12-27","time":"16:44:00","zoneOffset":"-08:00"},"locationAddr":{"countryCd":"CA","countryNmEn":"Canada","countryNmFr":"Canada","city":"OTTAWA","regionCd":"ON","postCd":"fe7f8a34497e70e049433b14ffa4b205"},"descEn":"Item received at originating postal facility","descFr":"Article reçu à l'installation postale d'origine","type":"PrReceived"},{"cd":"3000","webCd":"CODE-020A","datetime":{"date":"2021-12-27","time":"14:18:58","zoneOffset":"-05:00"},"locationAddr":{"countryCd":"","city":"","regionCd":"","postCd":""},"descEn":"Electronic information submitted by shipper","descFr":"Les renseignements électroniques ont été soumis par l'expéditeur","type":"Induction"}],"custNm":"Bill's Electronics","addtnlOrigInfo":"OTTAWA, ON","addtnlDestInfo":"MONTREAL, QC","suppressSignature":false,"lagTime":false,"returnPinIndicator":false,"refundAllowed":false,"dtcBarcode":false,"canadianDest":true,"dlvryInstruction":"","correctedPostalCode":"","sigReqByAmtDue":false,"shipperPostalCode":"","recipientNm":"*****"}'''
    details = CPostDetails(json.loads(text))
    assert details.status == 'ReadyPickup'
    assert details.pin == 2740170516551280
    assert details.delivery_type == 'Flex Delivery via Xpresspost'
    assert details.shipper_name == "Bill's Electronics"
    assert details.shipper_city == 'OTTAWA, ON'
    assert details.accepted_date == date(2021, 12, 27)
    assert details.expected_delivery_date == date(2022, 1, 6)

    logger.debug(f'{details.status=}')
    logger.debug(f'{details.pin=}')
    logger.debug(f'{details.shipper_name=}')
    logger.debug(f'{details.shipper_city=}')
    logger.debug(f'{details.delivery_type=}')
    logger.debug(f'{details.accepted_date=}')
    logger.debug(f'{details.expected_delivery_date=}')

    pickup = details.events[0]
    assert pickup.type == 'ToRetail'
    assert pickup.description == 'Item available for pickup at Post Office'
    assert pickup.address == 'MONTREAL, ON'
    for event in details.events:
        logger.debug(f'{str(event)}')
