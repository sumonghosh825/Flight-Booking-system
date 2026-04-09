from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def home(request):
    data = FlightModel.objects.all()
    if request.method =='POST':
        source=request.POST['source']
        destination=request.POST['destination']
        date_=request.POST['date_']
        data = FlightModel.objects.filter(
            from_city__icontains=source,
            to_city__icontains=destination,
            departure_date=date_
        )
    return render(request,'home.html',{'data':data})


def bookings_form(request,id):

    data = FlightModel.objects.get(id=id)

    if request.method == "POST":
        passenger_name = request.POST['passenger_name']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        adhar_no = request.POST['adhar_no']
        age = request.POST['age']
        seat_class = request.POST['seat_class']
        seat_no = request.POST['seat_no']

        BookingModel.objects.create(
            flight=data,
            passenger_name=passenger_name,
            email=email,
            phone_no=phone_no,
            adhar_no=adhar_no,
            age=age,
            seat_class=seat_class,
            seat_no=seat_no
        )

        return redirect('booking')   # booking er por home e chole jabe
    return render(request,'bookings_form.html',{'data':data})


def booking(request):
    data = BookingModel.objects.last()
    return render(request, 'booking.html', {'data': data})


def update_booking(request, id):
    data = BookingModel.objects.get(id=id)

    if request.method == "POST":
        passenger_name = request.POST['passenger_name']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        adhar_no = request.POST['adhar_no']
        age = request.POST['age']
        seat_class = request.POST['seat_class']
        seat_no = request.POST['seat_no']

        data.passenger_name = passenger_name
        data.email = email
        data.phone_no = phone_no
        data.adhar_no = adhar_no
        data.age = age
        data.seat_class = seat_class
        data.seat_no = seat_no

        data.save()

        return redirect('booking')

    return render(request, 'update_booking.html', {'data': data})

def delete_booking(request, id):
    booking = BookingModel.objects.get(id=id)
    booking.status = 'Cancelled'
    booking.save()

    return redirect('history')

def history(request):
    data = BookingModel.objects.all()
    return render(request,'history.html', {'data': data})




def logout(request):
    return render(request,'logout.html')


def support(request):
    return render(request,'support.html')


def about(request):
    return render(request,'about.html')