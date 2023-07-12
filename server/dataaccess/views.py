from uuid import uuid4
from django.http import JsonResponse
from django.shortcuts import render

# # Create your views here.
import csv
from dataaccess.models import Route, Station, Ticket, Train

def read_data_from_csv(filename: str) -> list:
    with open(filename, mode ='r') as file:   
        
       # reading the CSV file
       dict_reader = csv.DictReader(file)
 
       # displaying the contents of the CSV file
       return  list(dict_reader)
    

def load_stations_data() :
    filename = "data.csv"

    for data in read_data_from_csv(filename):
        stn_name=data['Station Name']
        station_code=data['Station Code']
        is_station_registered = Station.objects.filter(station_code=station_code)

        if not is_station_registered:
            station=Station(id=str(uuid4())[:8],station_name=stn_name, station_code=station_code)
            station.save()

    print("Stations Model saved...")
    return JsonResponse({"message": "Successfully updated the Stations model"})


def create_train_and_routes_data() :

    filename = "data.csv"

    for data in read_data_from_csv(filename):
        source = Station.objects.filter(station_code=data['Station Code'])
        destination = Station.objects.filter(station_code=data['Destination Station Code'])
        start_source = Station.objects.filter(station_code=data['Source Station Code'])

        if source[0].id == destination[0].id:
            continue

        if source and destination :

            try:
                train = Train.objects.get(train_name=data['Train Name'])
            except:

                train = Train.objects.create(
                            train_name=data['Train Name'],
                            train_number=data['Train No'],
                            train_source=start_source[0],
                            train_destination=destination[0],
                            first_ac=data['Seats'],
                            second_ac=data['Seats'],
                            third_ac=data['Seats'],
                            sleeper=data['Seats'],
                            days_availability=data['Availability'],
                            arrival=data['Train Arrival'],
                            departure=data['Train Departure'])
                train.save()

            route = Route.objects.get_or_create(
                        id=str(uuid4())[:8],
                        source=source[0],
                        destination=destination[0],
                        arrival=data['Arrival Time'],
                        departure=data['Departure Time'],
                    )
            route[0].train.add(train)

            print("Routes Model saved...")
    
    return JsonResponse({"message": "Successfully updated the Trains & Routes model"})


def load_data(req):
    print(load_stations_data())
    print(create_train_and_routes_data())

    return JsonResponse({"message": "Successfully updated the all the models"})


def truncate_data(req):
    Station.objects.all().delete()
    Route.objects.all().delete()
    Train.objects.all().delete()
    Ticket.objects.all().delete()
    return JsonResponse({"message": "Successfully truncated database"})