from django.shortcuts import render
from .models import Event, User, Eventcategory, Eventregistration
from django.http import JsonResponse
import json
from .utils import get_volunteers_from_eventId
from .utils import getEventById
from .utils import convertDateTimes
from .utils import convertDates
from .utils import getEventById_DateTime

import datetime

# Create your views here.
def demographic(request):
    eventId = request.GET.get('eventId', None)
    eventdetails = Event.objects.get(eventId__exact=eventId)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventId)
    eventvolunteersid = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventId)

    volunteers = get_volunteers_from_eventId(eventId)

    categories = [value for value in eventcategories]

    if eventId == None:
        pass #Return error

    data = {
        "eventId": eventdetails.eventId,
        "eventName":eventdetails.eventName,
        "startDateTime":eventdetails.startDateTime,
        "endDateTime":eventdetails.endDateTime,
        "numParticipants":eventdetails.maxParticipants,
        "organizerName":eventdetails.organizerName,
        "categoryId":categories,
        "volunteers":volunteers,
        "eventStatus": eventdetails.eventStatus
    }
    return JsonResponse(data)

def organization(request):
    organizerName = request.GET.get('organizerName', None)
    eventIdList = Event.objects.values_list('eventId',flat=True).filter(organizerName = organizerName)
    events = []
    for id in eventIdList:
        temp = getEventById(id)
        events.append(temp)
    data = {
        "events":events
    }
    return JsonResponse(data)


def historical(request):
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)
    fromDate, toDate = convertDateTimes(fromdate,todate)
    _fromDate, _toDate = convertDates(fromdate,todate)

    if fromDate > toDate or (toDate-fromDate).days > 365:
        return JsonResponse({"error":"change this later"})

    eventIdList = Event.objects.values_list('eventId',flat=True).filter(startDateTime__gte= fromDate)
    events=[]
    totalHours = 0
    for id in eventIdList:
        temp = getEventById_DateTime(id)
        events.append(temp)
        totalHours += temp["numHours"]

    data = {
    "numEvents": len(events),
    "totalHours":totalHours,
    "fromDate":_fromDate,
    "toDate":_toDate,
    "events": events
             }

    return JsonResponse(data)

def user_historical(request):
    userid = request.GET.get('userId', None)
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)
    pass
