from django.shortcuts import render
from .models import Event, User, Eventcategory
from django.http import JsonResponse
import json

# Create your views here.
def demographic(request):
    eventid = request.GET.get('eventId', None)
    eventdetails = Event.objects.get(id__exact=eventid)
    eventcategory = Eventcategory.objects.filter(eventid=eventid)
    print(eventcategory)
    if eventid == None:
        pass #Return error

    data = {
        "eventId": eventdetails.id,
        "eventName":eventdetails.eventname,
        "startDateTime":eventdetails.startdatetime,
        "endDateTime":eventdetails.enddatetime,
        "numParticipants":eventdetails.maxparticipants,
        "organizerName":eventdetails.organizername,
        # "categoryId":,
        # "volunteers":,
        "eventStatus": eventdetails.eventstatus
    }
    return JsonResponse(data)

def organization(request):
    organizerName = request.GET.get('organizerName', None)
    pass

def historical(request):
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)
    pass

def user_historical(request):
    userid = request.GET.get('userId', None)
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)
    pass
