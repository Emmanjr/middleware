import json
from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SeatSerializer
from .models import AbcOperationalCity, Trip, Seat, SeatStatus
from .config import get_all_abc_operational_cities_config, schedules_api_config, schedule_api_config, \
    tentative_booking_config


# Create your views here.
@api_view(['POST'])
def get_available_seats_by_schedule(request):
    try:
        departure_name = request.data.get('departureName')
        destination_name = request.data.get('destinationName')
        travel_date = request.data.get('travelDate')

        departure_id = get_abc_operation_city_id(departure_name)
        print('departure_id: ', departure_id)
        print('-------------------||---------------------')
        destination_id = get_abc_operation_city_id(destination_name)
        print('destination_id: ', destination_id)
        print('-------------------||---------------------')
        print('travel-date: ' + travel_date)

        schedule_id = get_route_schedule_id(departure_id, destination_id, travel_date)
        print('||-------------------||---------------------||')
        print('schedule-id: ', schedule_id)

        api_response = schedule_api_config(schedule_id)

        schedule_api_response = api_response

        print(' <---------------------------||------------------------------------------>')
        print('schedule_response: ' + schedule_api_response.__str__())
        print(' <--------------------------<<<<<<>>>>>>>>>>>---------------------------->')

        seat_list = parse_schedule_to_seat_response(schedule_api_response)

        serializer = SeatSerializer(seat_list, many=True)

        return Response(serializer.data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def get_trip_details_by_schedule(request):
    try:
        departure_name = request.data.get('departureName')
        destination_name = request.data.get('destinationName')
        travel_date = request.data.get('travelDate')

        departure_id = get_abc_operation_city_id(departure_name)
        print('departure_id: ', departure_id)
        print('-------------------||---------------------')
        destination_id = get_abc_operation_city_id(destination_name)
        print('destination_id: ', destination_id)
        print('-------------------||---------------------')
        print('travel-date: ' + travel_date)

        schedule_id = get_route_schedule_id(departure_id, destination_id, travel_date)
        print('||-------------------||---------------------||')
        print('schedule-id: ', schedule_id)

        api_response = schedule_api_config(schedule_id)

        schedule_api_response = api_response

        print(' <---------------------------||------------------------------------------>')
        print('schedule_response: ' + schedule_api_response.__str__())
        print(' <--------------------------<<<<<<>>>>>>>>>>>---------------------------->')

        serialized_data = parse_schedule_to_trip_response(schedule_api_response)

        return Response({'Trip': serialized_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def make_booking(request):
    print('in the make a booking ---------{}')
    try:
        booking_data = process_booking(request)
        schedule_id = request.get('schedule_id')

        response = tentative_booking_config(schedule_id, booking_data)
        print(' <---------------------------||------------------------------------------>')
        print('booking_response: ' + response.__str__())
        print(' <--------------------------<<<<<<>>>>>>>>>>>---------------------------->')

        return Response({'Booking_Response': response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def process_booking(request):
    print('<--------------------||----------------->')
    print('in the process a booking')

    selected_seats = request.get('selectedSeats', [{}])
    traveller_details = request.get('travellerDetails', [{}])
    origin_id = request.get('origin_id')
    destination_id = request.get('destination_id')
    takeoff_date = request.get('takeOffDate')

    if len(selected_seats) != len(traveller_details):
        raise ValueError("Number of selected seats must be the same as the number of traveler details")

    seat_details_list = []
    contact_details_list = []

    for seat, traveller_detail in zip(selected_seats, traveller_details):
        seat_number = seat.get('seatNumber', 'N/A')
        fare = request.get('tripFare', 'N/A')

        # Traveler details
        title = 'Mr' if traveller_detail.get('gender') == 'Male' else 'Mrs'
        name = traveller_detail.get('firstName', 'N/A')
        age = convert_dob_to_age(traveller_detail.get('dateOfBirth', 'N/A'))
        sex = traveller_detail.get('gender', 'N/A')
        is_primary = 'true'
        id_card_type = traveller_detail.get('id_card_type', 'N/A')
        id_card_number = traveller_detail.get('id_card_number', 'N/A')
        id_card_issued_by = traveller_detail.get('id_card_issued_by', 'N/A')

        mobile_number = traveller_detail.get('phoneNumber', 'N/A')
        emergency_name = traveller_detail.get('nextOfKinFirstName', 'N/A')
        email = traveller_detail.get('email', 'N/A')

        seat_detail = {
            "seat_number": seat_number,
            "fare": fare,
            "title": title,
            "name": name,
            "age": age,
            "sex": sex,
            "is_primary": is_primary,
            "id_card_type": id_card_type,
            "id_card_number": id_card_number,
            "id_card_issued_by": id_card_issued_by
        }
        seat_details_list.append(seat_detail)

        contact_detail = {
            "mobile_number": mobile_number,
            "emergency_name": emergency_name,
            "email": email
        }
        contact_details_list.append(contact_detail)

    mapped_data = {
        "book_ticket": {
            "seat_details": seat_details_list,
            "contact_details": contact_details_list
        },
        "origin_id": origin_id,
        "destination_id": destination_id,
        "boarding_at": origin_id,
        "no_of_seats": str(len(selected_seats)),
        "travel_date": takeoff_date
    }

    return mapped_data


def get_route_schedule_id(departure_id, destination_id, travel_date):
    response = schedules_api_config(departure_id, destination_id, travel_date)

    if response.status_code == 200:

        print(response.json())
        print('<-------------------->')
        json_data = response.json()

        first_key_list = json_data.get('result', [])

        second_list = first_key_list[1] if first_key_list else []

        print(second_list)

        schedule_id = second_list[0]

        return schedule_id

    else:

        return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)


def get_abc_operation_city_id(city_name):
    try:

        name = str(city_name)
        print('city-name: ' + name)
        city_id = search_objects(name)
        if city_id != -1:
            print('<--------------------||----------------------->')
            print('City_Id: ', city_id)
            print('<-------------------->')

            return city_id
        else:
            return JsonResponse({'error': 'No matching object found.'}, status=404)
    except Exception as e:

        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def get_all_abc_operation_cities(request):
    external_api_url = get_all_abc_operational_cities_config()

    cities_api_response = external_api_url

    print(' <---------------------------||------------------------------------------>')
    print('cities_response: ' + cities_api_response.__str__())
    print(' <--------------------------<<<<<<>>>>>>>>>>>---------------------------->')

    try:
        abc_operational_cities = parse_cities_response(cities_api_response)
        serialized_cities = serialize_cities(abc_operational_cities)

        return Response({'abc_operation_cities': serialized_cities})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def parse_schedule_to_trip_response(api_response):
    print('In the parse a schedule trip method -----> ')
    schedule_data = json.loads(api_response)

    seat_data = parse_schedule_to_seat_response(api_response)
    seat_list = SeatSerializer(seat_data, many=True)

    serializer_data = {
        'schedule_id': schedule_data.get('result').get('id'),
        'transport_company_name': schedule_data.get('result').get('service_name'),
        'route_departure_id': schedule_data.get('result').get('origin_id'),
        'route_destination_id': schedule_data.get('result').get('destination_id'),
        'take_off_date': schedule_data.get('result').get('travel_date'),
        'take_off_time': schedule_data.get('result').get('dep_time'),
        'vehicle_type': schedule_data.get('result').get('bus_type'),
        'seat_count': schedule_data.get('result').get('available_seats'),
        'seats': seat_list.data
    }

    return serializer_data


def parse_schedule_to_seat_response(api_response):
    seat_list = []
    schedule_data = json.loads(api_response)
    print(schedule_data)
    print('---------||----------||----------||-------')

    available_data = schedule_data.get('result').get('bus_layout').get('available')
    print('available-data: ', available_data)
    seat_pairs = available_data.split(',')
    seat_data = [str(pair.split('|')[0]) for pair in seat_pairs]
    print('---------||----------||----------||-------')
    print(seat_data)

    for entry in seat_data:
        seat = Seat(seat_number=entry,
                    status=SeatStatus.AVAILABLE.value)

        seat_list.append(seat)
    return seat_list


def parse_cities_response(cities_api_response):
    abc_operational_cities = []
    cities_data = json.loads(cities_api_response)
    result_data = cities_data.get('result', [])
    for i in range(1, len(result_data)):
        row = result_data[i]
        operational_city = AbcOperationalCity(
            id=row[0],
            name=row[1],
            origin_count=row[2],
            destination_count=row[3]
        )
        abc_operational_cities.append(operational_city)
    return abc_operational_cities


def serialize_cities(abc_operational_cities):
    serialized_cities = []
    for city in abc_operational_cities:
        serialized_city = {
            'id': city.id,
            'name': city.name,
            'origin_count': city.origin_count,
            'destination_count': city.destination_count,
        }
        serialized_cities.append(serialized_city)
    return serialized_cities


def serialize_cities_to_list(abc_operational_cities):
    serialized_cities = []
    for abc_city in abc_operational_cities:
        serialized_city = [
            abc_city.id,
            abc_city.name
        ]
        serialized_cities.append(serialized_city)
    return serialized_cities


def search_objects(name_of_city):
    data_bytes = get_all_abc_operational_cities_config()
    data_list = parse_cities_response(data_bytes)
    serialized_data_list = serialize_cities_to_list(data_list)
    print(serialized_data_list)
    print('<--------------------------------->>>>>>>>>>------------------------>')

    for elemente in serialized_data_list:
        cities_id, cities_name = elemente[0], elemente[1]

        print('City Id:', cities_id)
        print('City Name:', cities_name)

        # city_name = element[1]
        # print(city_name)
        if compare_strings_ignore_whitespace(cities_name.casefold(), name_of_city.casefold()):
            print('<---------------------------------<<<<<<<<<>>>>>>>>>>------------------------>')

            return cities_id
    else:
        return -1


def compare_strings_ignore_whitespace(str1, str2):
    return ''.join(str1.split()) == ''.join(str2.split())


def convert_dob_to_age(dob):
    # Assuming dob is in the format "YYYY-MM-DD"
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return str(age)
