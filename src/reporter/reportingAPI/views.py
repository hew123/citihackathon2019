from django.shortcuts import render
from .models import Event, User, Eventcategory, Eventregistration
from django.http import JsonResponse
import json

# Create your views here.
def demographic(request):
    eventid = request.GET.get('eventId', None)
    eventdetails = Event.objects.get(id__exact=eventid)
    eventcategories = Eventcategory.objects.values_list('categoryid', flat=True).filter(eventid=eventid)
    eventvolunteersid = Eventregistration.objects.values_list('userid', flat=True).filter(eventid=eventid)

    volunteers = []
    for value in eventvolunteersid:
        user = User.objects.get(id__exact=value).__dict__
        del user['_state']
        volunteers.append(user)

    categories = [value for value in eventcategories]

    if eventid == None:
        pass #Return error

    data = {
        "eventId": eventdetails.id,
        "eventName":eventdetails.eventname,
        "startDateTime":eventdetails.startdatetime,
        "endDateTime":eventdetails.enddatetime,
        "numParticipants":eventdetails.maxparticipants,
        "organizerName":eventdetails.organizername,
        "categoryId":categories,
        "volunteers":volunteers,
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
