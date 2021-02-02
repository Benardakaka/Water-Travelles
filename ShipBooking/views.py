from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import AdduserModel,AddRouteModel,AddShipModel,Transactions
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import AdduserForm,AddRouteForm,AddShipForm
import datetime
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request, 'ShipBooking/home.html')

def admincheck(request):
     if request.method == "POST":
         username = request.POST.get('username')
         password = request.POST.get('psw')
         if username == 'useradmin':
             if password == 'admin@123':
                 all_ships = AddShipModel.objects.all()
                 all_routes = AddRouteModel.objects.all()
                 return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})
             else:
                 return render(request, 'ShipBooking/home.html', {'pass_error': True})
         else:
             return render(request, 'ShipBooking/home.html', {'user_error': True})

def new_user(request):
    if request.method == "POST":
        form=AdduserForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('view_home'))
    else:
        form=AdduserForm()
        return render(request, 'ShipBooking/newuser.html', {'form':form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        checkname = AdduserModel.objects.filter(Name=username)
        if checkname:
            passwords=[x.Password for x in checkname]
            if password in passwords:
                 return render(request, 'ShipBooking/usersdashboard.html',{'name':username})
            else:
                 return render(request, 'ShipBooking/home.html', {'pass_error': True})
        else:
             return render(request, 'ShipBooking/home.html', {'user_error': True})

def add_ship(request):
    all_routes=AddRouteModel.objects.all()
    all_ships=AddShipModel.objects.all()
    if request.method == "POST":
        s=AddShipModel()
        s.Ship_number = request.POST.get('ship_no')
        route = request.POST.get('route')
        s.Route = AddRouteModel.objects.get(Route_id=route)
        hours = int(request.POST.get('hours'))
        minutes = int(request.POST.get('minutes'))
        s.Start_time = datetime.time(hours,minutes)
        s.Total_seats = request.POST.get('total_seats')
        s.save()
        return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})
    else:
        return render(request, 'ShipBooking/addship.html', {'all_routes':all_routes, 'hours':range(0,24), 'minutes':range(0,61)})



def add_route(request):
    all_routes=AddRouteModel.objects.all()
    all_ships=AddShipModel.objects.all()
    if request.method == "POST":
        form=AddRouteForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})
    else:
        form=AddRouteForm()
        return render(request, 'ShipBooking/addroute.html', {'form':form})

def update_ship(request,**kwargs):
    all_ships = AddShipModel.objects.all()
    all_routes = AddRouteModel.objects.all()
    if kwargs["action"] == 'edit':
        return render(request, "ShipBooking/updateship.html", {'all_ships':all_ships,'all_routes':all_routes})
    if kwargs["action"] == 'submit':
        ship_no = request.GET.get("ship_no")
        s = AddShipModel.objects.get(Ship_number=ship_no)
        new_route = request.GET.get("newroute")
        s.Route = AddRouteModel.objects.get(Route_id=new_route)
        hrs = int(request.GET.get("hours"))
        mins = int(request.GET.get("minutes"))
        s.Start_time = datetime.time(hrs,mins)
        s.Total_seats = request.GET.get("seats")
        s.save()
        return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})


def getUserInfo(request):
    if request.method == "GET" and request.is_ajax():
        Ship_num = request.GET.get("ship_no")
        try:
            ship_no = AddShipModel.objects.get(Ship_number = Ship_num)
        except:
            return JsonResponse({"success":False}, status=400)
        ship_info ={
        "Ship_no": ship_no.Ship_number,
        "Route_id": ship_no.Route.Route_id,
        "Ship_from": ship_no.Route.Ship_from,
        "Ship_to": ship_no.Route.Ship_to,
        "Journey_time": ship_no.Route.Journey_time,
        "Price_per_seat": ship_no.Route.Price_per_seat,
        "Total_seats":ship_no.Total_seats,
        "hrs":ship_no.Start_time.strftime("%H"),
        "mins":ship_no.Start_time.strftime("%M")
        }
        return JsonResponse({"ship_info":ship_info}, status=200)
    return JsonResponse({"success":False}, status=400)

def get_ships_info(request):
    if request.method == "GET" and request.is_ajax():
        get_ship_from = request.GET.get("shipFrom")
        get_ship_to = request.GET.get("shipTo")
        try:
            selected_ships=AddShipModel.objects.filter(Route__Ship_from=get_ship_from) and AddShipModel.objects.filter(Route__Ship_to=get_ship_to)
        except:
            return JsonResponse({"success":False}, status=400)

        data = []
        for ships in selected_ships:
            ships_info={
                "Ship_no": ships.Ship_number,
                "Route_id": ships.Route.Route_id,
                "Ship_from": ships.Route.Ship_from,
                "Ship_to": ships.Route.Ship_to,
                "Journey_time": ships.Route.Journey_time,
                "Price_per_seat": ships.Route.Price_per_seat,
                "Total_seats":ships.Total_seats,
                "hrs":ships.Start_time.strftime("%H"),
                "mins":ships.Start_time.strftime("%M")}
            data.append(ships_info)

        return JsonResponse({"ships_info":data}, status=200)
    return JsonResponse({"success":False}, status=400)


def delete_ship(request):
    all_routes=AddRouteModel.objects.all()
    all_ships=AddShipModel.objects.all()
    if request.method == "GET":
        ship_no = request.GET.get("ship_no")
        AddShipModel.objects.get(Ship_number=ship_no).delete()
        return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})

def delete_route(request):
    all_routes=AddRouteModel.objects.all()
    all_ships=AddShipModel.objects.all()
    if request.method == "GET":
        route_no = request.GET.get("route")
        AddRouteModel.objects.get(Route_id=route_no).delete()
        return render(request, 'ShipBooking/adminpage.html',{'all_ships':all_ships,'all_routes':all_routes})

def ship_booking(request,name):
    all_ships = AddShipModel.objects.all()
    all_routes = AddRouteModel.objects.all()
    return render(request, 'ShipBooking/booking.html', {'name':name,'all_ships':all_ships,'all_routes':all_routes})

def book_tickets(request,name):
    if request.method == "POST":
        passenger_name = request.POST.get("passenger_name")
        ship_no = request.POST.get("ship_no")
        ship_details = AddShipModel.objects.get(Ship_number=ship_no)
        date = request.POST.get("traveldate")
        seats = int(request.POST.get("seating"))
        s = Transactions()
        s.User_name = name
        s.Passenger_name = passenger_name
        s.Ship_details = ship_details
        s.Travel_date = date
        s.No_of_passengers = seats
        s.save()
        return render(request, 'ShipBooking/home.html',{'thanks':True})

def booking_history(request,name):
    transactions = Transactions.objects.filter(User_name=name)
    return render(request, 'ShipBooking/bookhistory.html', {'transactions':transactions})

# def services(request):
#     all_routes=AddRouteModel.objects.all()
#     all_ships=AddShipModel.objects.all()
#     if request.method == "GET":
#         ship_no = request.GET.get("ship_no")
#         AddShipModel.objects.get(Ship_number=ship_no).delete()
#         return render(request, 'ShipBooking/services.html',{'all_ships':all_ships,'all_routes':all_routes})
