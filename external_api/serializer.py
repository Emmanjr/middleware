from .models import Trip, Seat


from rest_framework import serializers


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'trip_amount', 'transport_company_name']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat_number', 'status']


