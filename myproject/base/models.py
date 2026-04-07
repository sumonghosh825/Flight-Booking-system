from django.db import models

# Create your models here.

#  flight_company , flight_name, flight_no , from_city, to_city, departure_time, departure_date, price 

class FlightModel(models.Model):
    flight_company=models.CharField(max_length=200)
    flight_name=models.CharField(max_length=500)
    flight_no=models.IntegerField()
    from_city=models.CharField(max_length=100)
    to_city=models.CharField(max_length=100)
    departure_time=models.TimeField()
    departure_date=models.DateField()
    price=models.IntegerField()


    def __str__(self):
        return self.flight_name


#booking model flight_company , flight_name, flight_no , from_city, to_city, departure_time, departure_date,
#  price, passenger_name , email , phone_no , adhar_no , age , seat_class, seat_no 


class BookingModel(models.Model):
    flight = models.ForeignKey(FlightModel, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.IntegerField()
    adhar_no = models.IntegerField()
    age = models.IntegerField()
    SEAT_CHOICES = (
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    )
    seat_class = models.CharField(max_length=20, choices=SEAT_CHOICES)
    seat_no = models.CharField(max_length=10)
    booking_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked')

    def __str__(self):
        return f"{self.passenger_name} - {self.flight.flight_name}"