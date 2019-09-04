from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime
from rest_framework.response import Response
from .models import Flight, Booking
from .serializers import FlightSerializer,NormalUpdateBookingSerializer, BookingSerializer, BookingDetailsSerializer, UpdateBookingSerializer, RegisterSerializer


class FlightsList(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingsList(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.filter(date__gte=datetime.today(), user=self.request.user)
        return queryset


class BookingDetails(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class UpdateBooking(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = UpdateBookingSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UpdateBookingSerializer
        else:
            return NormalUpdateBookingSerializer

            
            # serializer.save(passengers=serializer.data['passengers'])

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
        
    #     instance = self.get_object()
        
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     print(serializer.data)
    #     return Response(serializer.data)



class CancelBooking(DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class BookFlight(CreateAPIView):
    serializer_class = UpdateBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
