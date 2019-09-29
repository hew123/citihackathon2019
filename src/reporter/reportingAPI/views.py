from .models import Event, User, Eventcategory, Eventregistration
from django.http import JsonResponse
from .utils import get_volunteers_from_eventId, get_volunteers_event, getEventById, \
    convertDate, is_simple_valid_date

from datetime import datetime, date
import datetime as _datetime
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

import csv
# Create your views here.
# Retrieve event details based on event id
def demographic(request):
    eventId = request.GET.get('eventId', None)
    if not eventId:
        data = {"error": f"eventId query parameter missing"}
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        eventId = request.GET.get('eventId', None)
        if int(eventId) < 1:
            data = {"error": f"eventId: `{eventId}` should be greater than `0`"}
            return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError:
        data = {
            "error": f"eventId: `{eventId}` should be of type `<class 'int'>` not {type(eventId)}"}
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        data = demographic_support(eventId)
    except ObjectDoesNotExist:
        data = {"error": f"`eventId` of {eventId} is not found in db"}
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse(data)


def demographic_support(eventId):
    eventdetails = Event.objects.get(eventId__exact=eventId)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventId)

    volunteers = get_volunteers_from_eventId(eventId)

    categories = [value for value in eventcategories]

    data = {
        "eventId": eventdetails.eventId,
        "eventName": eventdetails.eventName,
        "startDateTime": eventdetails.startDateTime,
        "endDateTime": eventdetails.endDateTime,
        "numParticipants": len(volunteers),
        "organizerName": eventdetails.organizerName,
        "categoryId": categories,
        "volunteers": volunteers,
        "eventStatus": eventdetails.eventStatus
    }
    return data


# Retrieve events based on organisation that organised it
def organization(request):
    organizerName = request.GET.get('organizerName', None)
    if not organizerName:
        data = {"error": f"organizerName query parameter missing"}
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    eventIdList = Event.objects.values_list('eventId', flat=True).filter(organizerName=organizerName)
    if len(eventIdList) == 0:
        data = {"error": f"`eventId` of {organizerName} is not found in db"}
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    events = [getEventById(id) for id in eventIdList]
    data = {
        "events": events
    }
    return JsonResponse(data)


# Retrieval of historical event data from "fromDate" to "endDate"
def historical(request):
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)

    if fromdate and not is_simple_valid_date(fromdate):
        return JsonResponse({"error": "fromDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if todate and not is_simple_valid_date(todate):
        return JsonResponse({"error": "toDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if fromdate:
        if todate:
            try:
                fromDate, toDate = convertDate(fromdate, todate)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if fromDate > toDate:
                return JsonResponse({"error": "fromDate must be earlier than toDate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"error": "toDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if todate:
            return JsonResponse({"error": "fromDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            fromDate = date.today() - _datetime.timedelta(days=365)
            toDate = datetime.combine(date.today(), datetime.max.time())

    eventIdList = Event.objects.values_list('eventId', flat=True).filter(startDateTime__gte=fromDate).filter(endDateTime__lte=toDate)

    events=[]
    for id in eventIdList:
        events.append(demographic_support(id))

    return JsonResponse({"events": events})


#Retrieve events of all volunteers
def user_historical(request):
    userid = request.GET.get('userId', None)
    _fromdate = request.GET.get('fromDate', None)
    _todate = request.GET.get('toDate', None)

    if _fromdate and not is_simple_valid_date(_fromdate):
        return JsonResponse({"error": "fromDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if _todate and not is_simple_valid_date(_todate):
        return JsonResponse({"error": "toDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if _fromdate:
        if _todate:
            try:
                fromDate, toDate = convertDate(_fromdate, _todate)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if fromDate > toDate:
                return JsonResponse({"error": "fromDate must be earlier than toDate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if (toDate-fromDate).days > 365:
                return JsonResponse({"error": "The range of the date should be lesser than 1 year"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"error": "toDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if _todate:
            return JsonResponse({"error": "fromDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
    eventdetails = Event.objects.get(eventId__exact=eventid)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventid)
    eventvolunteersid = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventid)

    volunteers = []
    for value in eventvolunteersid:
        user = User.objects.values('userId', 'userName', 'emailAddress', 'firstName', 'lastName', 'gender', 'dateOfBirth', 'accountType').get(userId__exact=value)
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
    fromdate = request.GET.get('fromDate', None)
    todate = request.GET.get('toDate', None)

    if fromdate and not is_simple_valid_date(fromdate):
        return JsonResponse({"error": "fromDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if todate and not is_simple_valid_date(todate):
        return JsonResponse({"error": "toDate should be in the format of `YYYY-MM-DD`"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if fromdate:
        if todate:
            try:
                fromDate, toDate = convertDate(fromdate, todate)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if fromDate > toDate:
                return JsonResponse({"error": "fromDate must be earlier than toDate"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if (toDate-fromDate).days > 365:
                return JsonResponse({"error": "The range of the date should be lesser than 1 year"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"error": "toDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if todate:
            return JsonResponse({"error": "fromDate should not be empty"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            fromDate = date.today() - _datetime.timedelta(days=365)
            _toDate = date.today()
            toDate = datetime.combine(_toDate, datetime.max.time())

    eventIdList = Event.objects.values_list('eventId', flat=True).filter(startDateTime__gte=fromDate).filter(endDateTime__lte=toDate)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EventSummary.csv"'

    writer = csv.writer(response)

    writer.writerow(['Events Summary'])
    writer.writerow(['Start date range: ' + str(fromDate)])
    writer.writerow(['End date range: ' + str(_toDate)])
    writer.writerow([ ])
    writer.writerow(['Event ID', 'Event name', 'Start datetime', 'End datetime', 'Min participants', 'Max participants', 'Category', 'Organizer', 'Description', 'Event status', '# participated'])

    for eventID in eventIdList:
        eventdetails = Event.objects.get(eventId__exact=eventID)
        eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventID)
        categories = [value for value in eventcategories]
        eventvolunteersid = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventID).filter(status='attended')

        writer.writerow([eventID, eventdetails.eventName, eventdetails.startDateTime, eventdetails.endDateTime, eventdetails.minParticipants, eventdetails.maxParticipants, categories, eventdetails.organizerName, eventdetails.description, eventdetails.eventStatus, len(eventvolunteersid)])

    return response


