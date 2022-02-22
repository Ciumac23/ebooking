from django.http import HttpResponse
from django.shortcuts import render, redirect
from ebooking.forms import BookForm, RoomForm
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .filters import RoomFilter
from django.contrib.auth.decorators import login_required
import psycopg2

@login_required(login_url='login')
def home(request):

    conn = psycopg2.connect(
        host = "localhost",
        database = "ebooking",
        user = "postgres",
        password = "admin")
    cur = conn.cursor()

    cur.callproc('total_rooms', ())
    total_rooms = cur.fetchone()
    cur.callproc('most_booked_country', ())
    best_country = cur.fetchone()
    print(best_country)
    cur.close()
    conn.close()
    host_q = Host.objects.all()
    users_q = User.objects.all()
    books = Book.objects.all()

    last_three = Room.objects.all().order_by('-price')[:3]
    renting_rooms = books.filter(status='Renting').count()
    context = {'hosts' : host_q,
                'users' : users_q,
                'top3' : last_three,
                'total_rooms' : total_rooms[0],
                'renting_rooms' : renting_rooms,
                'best_country' : best_country[0]}
    return render(request, "dashboard.html", context)
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid credentials. Try again")
            return redirect('login')
    else:
        return render(request, "login.html")

@login_required(login_url='login')
def list_rooms(request):
    rooms = Room.objects.all()
    fltrs = RoomFilter(request.GET, queryset=rooms)
    rooms = fltrs.qs
    context = {'rooms' : rooms, 'filter' : fltrs}

    return render(request, "rooms.html", context)
def logout(request):
    auth.logout(request)
    return redirect('login')
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        second_name = request.POST.get("second_name")
        language = request.POST.get("language")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        email = request.POST.get("email")
        username = request.POST.get("username")

        if pass1 == pass2 and not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            host_model = User.objects.create_user(first_name=first_name, last_name=second_name, username=username, password=pass1, email=email)
            host_model.save()
            return HttpResponse("Need to add a new room into the list" + first_name)
        elif pass1 != pass2:
            return HttpResponse("Incorrect password")
        elif User.objects.filter(email=email).exists():
            return HttpResponse("User already exists with this mail")
        else:
            return HttpResponse("Try another username. {} is already taken!".format(username))
    return render(request, "register_host.html")

@login_required(login_url='login')
def book_room(request):
    bookForm = BookForm()
    if request.method == "POST":
        bookForm = BookForm(request.POST)
        if bookForm.is_valid():
            bookForm.save()
            return redirect('/')
    context = {'form' : bookForm}
    return render(request, "order_from.html", context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    roomForm = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form' : roomForm}
    return render(request, 'order_from.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('/')
    context = {'item' : room}
    return render(request, "delete.html", context)

def show_room(reqeust, pk):
    pass
@login_required(login_url='login')
def show_host(request, pk):
    host = Host.objects.get(id=pk)
    books = host.book_set.all()
    context = {'host' : host, 'book' : books}
    return render(request, "host_id.html", context)