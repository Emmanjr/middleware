from django.urls import path
from .views import get_all_abc_operation_cities, get_available_seats_by_schedule, \
    get_trip_details_by_schedule, make_booking

urlpatterns = [

    path('get-abc-operation-cities/', get_all_abc_operation_cities, name='get-all-abc-cities'),
    path('get-available-schedule-seats/', get_available_seats_by_schedule, name='get-available-seats'),
    path('get-trip-schedule-detail/', get_trip_details_by_schedule, name='get-available-schedule-trip'),
    path('book-schedule-trip/', make_booking, name='book-schedule-trip'),
]
