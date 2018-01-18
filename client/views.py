from django.shortcuts import render
from .models import Client, ClientFlight, Airports
from tdrivers.models import tDriver
from django.contrib.auth.decorators import login_required
from .forms import clientForm
from django.shortcuts import redirect
import telebot
import sqlite3
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TOKEN = "xxxxxxx"

# Create your views here.
@login_required
def clientsList(request):
    page = request.GET.get('page', 1)
    clients = Client.objects.all()
    paginator = Paginator(clients, 10)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    return render(request, 'client/clientsList.html', {'clients':clients})


@login_required
def flightsList(request, crId):

    page = request.GET.get('page', 1)
    if crId == "0":
        flights = ClientFlight.objects.all().order_by('flDate')
    else:
        flights = ClientFlight.objects.all().order_by('-flDate')

    if crId == "2":
        flights = ClientFlight.objects.all().filter(isAnnounced=False).order_by('flDate')


    paginator = Paginator(flights, 10)

    try:
        flights = paginator.page(page)
    except PageNotAnInteger:
        flights = paginator.page(1)
    except EmptyPage:
        flights = paginator.page(paginator.num_pages)

    return render(request, 'client/flightsList.html', {'flights': flights})


@login_required
def flightAnnounce(request):
    cbList = request.POST.getlist('Announce')
    bot = telebot.TeleBot(TOKEN)
    drvs = tDriver.objects.filter(isActive=True).values()

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("/getorders")
    for c in cbList:
        fl = ClientFlight.objects.filter(id=c).values()
        client = Client.objects.filter(id=fl[0]['fClient_id'])
        airport = Airports.objects.filter(id=fl[0]['fAirport_id'])
        announceText = "Deare colleagues! Our client <b>" + str(client[0]) + "</b> are landing in <b>" + str(airport[0]) + "</b> airport at <b>" + str(fl[0]['flDate']) + \
                       "</b>. The flight number is <b>" + str(fl[0]['flNumber']) + "</b>."

        #annReplyText = "Get " + str(client[0]) + " clients flight#" + str(fl[0]['flNumber']) + " order. Date - " + str(fl[0]['flDate'])

        for d in drvs:
            msg = bot.send_message(d.get('dTlgMsg'),announceText, parse_mode='HTML')
            bot.reply_to(msg, "Get the order.", reply_markup=markup)
            print(d.get('dTlgMsg'))

        conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
        curs = conn.cursor()
        curs.execute("UPDATE client_clientflight SET isAnnounced = 1 WHERE flNumber = '" + str(fl[0]['flNumber']) + "'")
        conn.commit()

    return redirect('flightslist',0) #flightsList(request, 0)


@login_required
def clientInput(request):
    if request.method == "POST":
        form = clientForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.iUser = request.user
            s.save()
            return redirect('clientslist')
        else:
            return render(request, 'errorpage.html', {'errT': "Error saving client"})
    else:
        s = clientForm()
        return render(request, 'client/clientInput.html', {'clientForm': s})

@login_required
def clientEdit(request, clientId):
    client = Client.objects.get(id=clientId)
    cForm = clientForm(request.POST or None, instance=client)
    if cForm.is_valid():
        client = cForm.save(commit=False)
        client.iUser = request.user
        client.save()
        return redirect('clientslist')

    return render(request, 'client/clientInput.html', {'clientForm': cForm})
