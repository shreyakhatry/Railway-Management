import json
from datetime import datetime
from uuid import uuid4
from random import randint

import jwt
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from auth.views import authReq
from booking.utils.helper import extract, getAvailableTrains, toDateTime, updateSeats
from dataaccess.models import Route, Station, Train, Ticket


@csrf_exempt
def get_train_details(req, stn_codes, doj):

    # Example
    # Request Endpoint: /book/trains/BBS-BNC/2023-07-10
    # Payload: None
    # Request Type: GET
    # Header: "Authorization": "<Token you get from signup/signin>"

    try:
        token = req.headers["Authorization"]
    except:
        return JsonResponse({"error": "PLease login First"})
    if authReq(token):
        doj = toDateTime(doj)
        doj1 = datetime.strptime(doj, "%Y/%m/%d")
        today = datetime.today()
        delta = doj1 - today
        if delta.days > 120:
            return JsonResponse(
                {"error": "Booking Not allowed beyond 3 months"}, status=403
            )
        elif delta.days < -1:
            return JsonResponse({"error": "You can't travel in past ;)"}, status=404)

        src, dest = extract(stn_codes)

        try:
            source = Station.objects.filter(station_code=src).values()
        except:
            return JsonResponse({"error": "Source Station Not found"}, status=404)
        try:
            destination = Station.objects.filter(station_code=dest.upper()).values()
        except Exception as e:
            return JsonResponse({"error": "Destination Station Not found"}, status=404)

        try:
            routes = Route.objects.get(source=source[0].get('id'), destination=destination[0].get('id'))
            trains = routes.train.all()
        except:
            return JsonResponse(
                {"error": "No trains in this route available"}, status=404
            )
        trains_list = [train for train in trains.values()]
        avlTrains = getAvailableTrains(list(trains_list), doj)
        for avlTrain in avlTrains:
            avlTrain['source'] = source[0].get('station_name')
            avlTrain['destination'] = destination[0].get('station_name')
            avlTrain.pop('train_source_id')
            avlTrain.pop('train_destination_id')
        return JsonResponse({"trains": trains_list})


@csrf_exempt
def book_ticket(req, train_number):
    # Example
    # Request Endpoint: /book/trains/<train_number>
    # Payload: {
        # "date_of_journey": "",
        # "passenger_first_name": ""
        # "passenger_last_name": ""
        # "passenger_age": ""
        # "passenger_gender": ""
        # "seatclass": ""
        # "boarding_station: ""

    # }
    # Request Type: POST
    # Header: "Authorization": "<Token you get from signup/signin>"

    if req.method == "POST":
        try:
            token = req.headers["Authorization"]
        except:
            return JsonResponse({"error": "Please login first"})
        if authReq(token):
            user_id = jwt.decode(token, "secret", algorithms="HS256")
            user_id = user_id["id"]
            user = User.objects.get(id=user_id)
            data = json.loads(req.body)
            doj = data["date_of_journey"]
            doj1 = toDateTime(doj)
            doj2 = datetime.strptime(doj1, "%Y/%m/%d")
            train = Train.objects.get(pk=train_number)
            fname = data["passenger_first_name"]
            lname = data["passenger_last_name"]
            age = data["passenger_age"]
            gender = data["passenger_gender"]
            seatclass = data["seatclass"]
            boarding_station = Station.objects.get(station_name=data['boarding_station'])
            ticket = Ticket(
                pnr=randint(100000000, 10000000000),
                buyer=user,
                train=train,
                first_name=fname,
                last_name=lname,
                age=age,
                gender=gender,
                seatclass=seatclass,
                doj=doj2,
                boarding_station=boarding_station
            )
            ticket.save()
            updateSeats(train, seatclass)
            return JsonResponse({"booked": "ok"})
        else:
            return JsonResponse({"error": "Please login first"})
    else:
        return JsonResponse({"error": "Method not allowed"})

@csrf_exempt
def seats_availabilty(req, train_number):
    # Example
    # Request Endpoint: /book/seatinfo/<train_number>
    # Payload: {}
    # Request Type: GET
    # Header: "Authorization": "<Token you get from signup/signin>"
    try:
        token = req.headers["Authorization"]
    except:
        return JsonResponse({"error": "Please login First"})
    if authReq(token):
        train = Train.objects.get(pk=train_number)
        first_ac = train.first_ac
        second_ac = train.second_ac
        third_ac = train.third_ac
        sleeper = train.sleeper
        numr = train.train_name
        payload = {
            "train_number": numr,
            "first_ac": first_ac,
            "second_ac": second_ac,
            "third_ac": third_ac,
            "sleeper": sleeper,
        }
        return JsonResponse("payload", status=200)

@csrf_exempt
def my_bookings(req):
    # Example
    # Request Endpoint: /book/mybookings
    # Payload: {}
    # Request Type: GET
    # Header: "Authorization": "<Token you get from signup/signin>"
    try:
        token = req.headers["Authorization"]
    except:
        return JsonResponse({"error": "Please login first"})
    if authReq(token):
        user_id = jwt.decode(token, "secret", algorithms="HS256")
        user_id = user_id["id"]
        user = User.objects.get(id=user_id)
        tickets = Ticket.objects.filter(buyer=user).values()
        tickets = list(tickets)
        for i in range(len(tickets)):
            train_number = tickets[i]["train_id"]
            train = Train.objects.get(pk=train_number)
            tickets[i]["train_number"] = train.train_number
            tickets[i]["train"] = train.train_name
            tickets[i]["platform"] = randint(0, 9)
            tickets[i]["arrival"] = train.arrival
            tickets[i]["departure"] = train.departure

            tickets[i]["destination"] = train.train_destination.station_name
            tickets[i]["destination_code"] = train.train_destination.station_code

            boarding_station = Station.objects.get(pk=tickets[i]["boarding_station_id"])
            tickets[i]["boarding_station"] = boarding_station.station_name
            tickets[i]["boarding_station_code"] = boarding_station.station_code
            tickets[i].pop('boarding_station_id')

        return JsonResponse({"tickets": tickets})
    return HttpResponse("<h1></h1>")
