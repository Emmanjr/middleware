from django.db import models
from enum import Enum


# Create your models here.

class SeatStatus(Enum):
    BOOKED = 'BOOKED'
    PENDING = 'PENDING'
    AVAILABLE = 'AVAILABLE'


class Seat(models.Model):
    seat_number = models.CharField(max_length=255)
    status = models.CharField(choices=[(tag, tag.value) for tag in SeatStatus], max_length=20)


class TripStatus(Enum):
    PENDING = 'PENDING'
    ONGOING = 'ONGOING'
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'
    DRAFT = 'DRAFT'


class Trip(models.Model):
    trip_id = models.BigIntegerField()
    route_id = models.BigIntegerField()
    route_departure_terminal_name = models.CharField(max_length=255)
    route_departure_city = models.CharField(max_length=255)
    route_departure_state = models.CharField(max_length=255)
    route_destination_terminal_name = models.CharField(max_length=255)
    route_destination_city = models.CharField(max_length=255)
    route_destination_state = models.CharField(max_length=255)
    route_departure_terminal_image = models.CharField(max_length=255)
    vehicle_capacity = models.IntegerField()
    schedule_id = models.BigIntegerField()
    vehicle_type = models.CharField(max_length=255)
    take_off_date = models.DateField()
    return_date = models.CharField(max_length=255)
    take_off_time = models.CharField(max_length=255)
    trip_amount = models.FloatField()
    discount_amount = models.FloatField()
    active = models.BooleanField()
    status = models.CharField(choices=[(tag, tag.value) for tag in TripStatus], max_length=20)
    transport_company_id = models.BigIntegerField()
    terminal_id = models.BigIntegerField()
    route_destination_id = models.BigIntegerField()
    route_departure_id = models.BigIntegerField()
    terminal_longitude = models.CharField(max_length=255)
    terminal_latitude = models.CharField(max_length=255)
    transport_company_name = models.CharField(max_length=255)
    transport_company_logo = models.CharField(max_length=255)
    transport_company_email = models.EmailField()
    group_id = models.CharField(max_length=255)
    trip_region = models.CharField(max_length=255)
    main_drop_off = models.BooleanField()
    trip_stops = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    departure_query = models.CharField(max_length=255)
    destination_query = models.CharField(max_length=255)


class AbcOperationalCity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    origin_count = models.IntegerField()
    destination_count = models.IntegerField()

    def __str__(self):
        return self.name
