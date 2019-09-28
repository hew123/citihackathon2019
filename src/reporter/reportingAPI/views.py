from django.shortcuts import render
from .models import Event, User, Eventcategory, Eventregistration
from django.http import JsonResponse
import json
from .utils import get_volunteers_from_eventId, get_volunteers_event
from .utils import getEventById
from .utils import convertDate
from .utils import getEventById_DateTime

from datetime import datetime, date
import datetime as _datetime

# Create your views here.
# Retrieve event details based on event id
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

# Retrieve events based on organisation that organised it
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

# Retrieval of historical event data from "fromDate" to "endDate"
def historical(request):
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)
    fromDate, toDate = convertDate(fromdate,todate)

    if fromDate > toDate or (toDate-fromDate).days > 365:
        return JsonResponse({"error":"change this later"})

    eventIdList = Event.objects.values_list('eventId',flat=True).filter(startDateTime__gte = fromDate).filter(endDateTime__lte = toDate)

    events=[]
    totalHours = 0
    for id in eventIdList:
        temp = getEventById_DateTime(id)
        events.append(temp)
        totalHours += temp["numHours"]

    # data = {
    # "numEvents": len(events),
    # "totalHours":totalHours,
    # "fromDate":_fromDate,
    # "toDate":_toDate,
    # "events": events
    #          }

    return JsonResponse({"events": events})

#Retrieve events of all volunteers
def user_historical(request):
    userid = request.GET.get('userId', None)
    _fromdate = request.GET.get('fromDate', None)
    _todate = request.GET.get('toDate', None)

    if _fromdate:
        if _todate:
            fromDate, toDate = convertDate(_fromdate,_todate)

            if fromDate > toDate or (toDate-fromDate).days > 365:
                return JsonResponse({"error":"change this later"})
        else:
            return JsonResponse({"error":"change this later"})
    else:
        if _todate:
            return JsonResponse({"error":"change this later"})
        if not _todate:
            return JsonResponse({
                "numEvents": 0,
                "totalHours": 0,
                "fromDate": "",
                "toDate": "",
                "events": [],
            })
        else:
            fromDate = date.today() - _datetime.timedelta(days=365)
            toDate = datetime.combine(date.today(), datetime.max.time())

    eventIdArray = Eventregistration.objects.values_list('eventId', flat=True).filter(userId=userid)
    events = get_volunteers_event(eventIdArray, fromDate, toDate)
    totalHours = 0
    for e in events:
        totalHours += e['numHours']

    data = {
        "numEvents": len(events),
        "totalHours":totalHours,
        "fromDate":_fromdate,
        "toDate":_todate,
        "events": events
     }

    return JsonResponse(data)

def export_csv_single_event(request):
    eventid = request.GET.get('eventId', None)
    eventdetails = Event.objects.get(id__exact=eventid)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventid)
    eventvolunteersid = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventid)

    volunteers = []
    for value in eventvolunteersid:
        user = User.objects.values('userId', 'userName', 'emailAddress', 'firstName', 'lastName', 'gender', 'dateOfBirth', 'accountType').get(userId__exact=value)
        print(user)# del user['_state']
        volunteers.append(user)

    categories = [value for value in eventcategories]

    return writecsv_single_event(eventid, eventdetails, categories, volunteers)

def writecsv_single_event(eventid, eventdetails, categories, volunteers):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + eventdetails.eventName + '.csv"'

    writer = csv.writer(response)

    writer.writerow(['Event ID: ' + eventid])
    writer.writerow(['Event name: ' + eventdetails.eventName])
    writer.writerow(['Event start datetime: ' + str(eventdetails.startDateTime)])
    writer.writerow(['Event end datetime: ' + str(eventdetails.endDateTime)])
    writer.writerow(['Number of participants required: ' + str(eventdetails.maxParticipants)])
    writer.writerow(['Organizer name: ' + eventdetails.organizerName])
    writer.writerow(['Category: ' + str(categories)])
    writer.writerow([ ])
    writer.writerow(['User ID', 'Username', 'Email address', 'First name', 'Last name', 'Gender', 'Date of birth'])
    for volunteer in volunteers:
        writer.writerow([volunteer['userId'], volunteer['userName'], volunteer['emailAddress'], volunteer['firstName'], volunteer['lastName'], volunteer['gender'], volunteer['dateOfBirth']])

    return response

def export_csv_events(request):
    fromDate = request.GET.get('fromDate', None)
    toDate = request.GET.get('toDate', None)
    fromDate, toDate = convertDateTimes(fromdate,todate)
    _fromDate, _toDate = convertDates(fromdate,todate)

    if fromDate > toDate or (toDate-fromDate).days > 365:
        return JsonResponse({"error":"change this later"})

    eventdetails = Event.objects.get(id__exact=eventid)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventid)
    eventvolunteersid = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventid)

    volunteers = []
    for value in eventvolunteersid:
        user = User.objects.values('userId', 'userName', 'emailAddress', 'firstName', 'lastName', 'gender', 'dateOfBirth', 'accountType').get(userId__exact=value)
        print(user)# del user['_state']
        volunteers.append(user)

    categories = [value for value in eventcategories]

    return writecsv(eventid, eventdetails, categories, volunteers)

def writecsv(eventid, eventdetails, categories, volunteers):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + eventdetails.eventName + '.csv"'

    writer = csv.writer(response)

    writer.writerow(['Event ID: ' + eventid])
    writer.writerow(['Event name: ' + eventdetails.eventName])
    writer.writerow(['Event start datetime: ' + str(eventdetails.startDateTime)])
    writer.writerow(['Event end datetime: ' + str(eventdetails.endDateTime)])
    writer.writerow(['Number of participants required: ' + str(eventdetails.maxParticipants)])
    writer.writerow(['Organizer name: ' + eventdetails.organizerName])
    writer.writerow(['Category: ' + str(categories)])
    writer.writerow([ ])
    writer.writerow(['User ID', 'Username', 'Email address', 'First name', 'Last name', 'Gender', 'Date of birth'])
    for volunteer in volunteers:
        writer.writerow([volunteer['userId'], volunteer['userName'], volunteer['emailAddress'], volunteer['firstName'], volunteer['lastName'], volunteer['gender'], volunteer['dateOfBirth']])

    return response
