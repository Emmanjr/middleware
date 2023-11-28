import requests
from urllib.parse import quote


def schedules_api_config(departure_id, destination_id, travel_date):
    # external_api_url = 'http://gds-stg.ticketsimply.africa/gds/api/schedules/1/2/2023-09-26.json'
    converted_departure_id = str(departure_id)
    converted_destination_id = str(destination_id)

    external_api_url = f'http://gds-stg.ticketsimply.africa/gds/api/schedules/{departure_id}/{destination_id}/{travel_date}.json '
    headers = {
        "Content-Type": "application/json",
        "api-key": "TSUCRSAPI64372724",
        "Accept-Encoding": "gzip",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    print(requests.get(external_api_url, headers=headers).url)
    print('<-------------------->')
    return requests.get(external_api_url, headers=headers)


def schedule_api_config(schedule_id):
    external_api_url = f'http://gds-stg.ticketsimply.africa/gds/api/schedule/{schedule_id}.json'
    headers = {
        "Content-Type": "application/json",
        "api-key": "TSUCRSAPI64372724",
        "Accept-Encoding": "gzip",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    print(requests.get(external_api_url, headers=headers).url)
    return requests.get(external_api_url, headers=headers).content


def tentative_booking_config(schedule_id, payload):
    external_api_url = f'http://gds-stg.ticketsimply.africa/gds/api/tentative_booking/{schedule_id}.json'
    headers = {
        "Content-Type": "application/json",
        "api-key": "TSUCRSAPI64372724",
        "Accept-Encoding": "gzip",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    print(requests.post(external_api_url, json=payload, headers=headers).url)
    return requests.post(external_api_url, json=payload, headers=headers).content


def get_all_abc_operational_cities_config():
    external_api_url = 'http://gds-stg.ticketsimply.africa/gds/api/cities.json'
    headers = {
        "Content-Type": "application/json",
        "api-key": "TSUCRSAPI64372724",
        "Accept-Encoding": "gzip",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    return requests.get(external_api_url, headers=headers).content
