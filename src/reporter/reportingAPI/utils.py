from .models import Event, User, Eventcategory, Eventregistration
import datetime

def get_volunteers_from_eventId(eventId):
    eventvolunteersids = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventId)

    volunteers = []
    for id in eventvolunteersids:
        user = User.objects.values('userId', 'firstName', 'lastName', 'gender',
                                   'dateOfBirth', 'accountType').get(userId__exact=id)
        volunteers.append(user)
    return volunteers

def getEventById(eventId):
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
    return data

def getEventById_DateTime(eventId):
    eventdetails = Event.objects.get(eventId__exact=eventId)
    eventcategories = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=eventId)
    categories = [value for value in eventcategories]

    diff = eventdetails.endDateTime - eventdetails.startDateTime
    numHours = (diff.seconds)/3600

    if eventId == None:
        pass #Return error

    data = {
        "eventId": eventdetails.eventId,
        "eventName":eventdetails.eventName,
        "startDateTime":eventdetails.startDateTime,
        "endDateTime":eventdetails.endDateTime,
        "numHours":numHours,
        "organizerName":eventdetails.organizerName,
        "categoryId":categories,
        "eventStatus": eventdetails.eventStatus
    }
    return data

def convertDateTimes(fromdate, todate):
    strA = (fromdate.split('-')) #"fromDate=2018","06","01"
    yearA = (strA[0]).split('=')[1]
    dateA = datetime.datetime(int(yearA),int(strA[1]),int(strA[2]))
    strB = (todate.split('-')) #"2018","06","01"
    dateB = datetime.datetime(int(strB[0]),int(strB[1]),int(strB[2]))
    print(dateA, dateB)
    return(dateA,dateB)

def convertDates(fromdate, todate):
    strA = (fromdate.split('-')) #"fromDate=2018","06","01"
    yearA = (strA[0]).split('=')[1]
    dateA = datetime.date(int(yearA),int(strA[1]),int(strA[2]))
    strB = (todate.split('-')) #"2018","06","01"
    dateB = datetime.date(int(strB[0]),int(strB[1]),int(strB[2]))
    print(dateA, dateB)
    return(dateA,dateB)
