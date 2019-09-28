from .models import Event, User, Eventcategory, Eventregistration
import datetime


def get_volunteers_event(eventIdArray, fromDateTime, toDateTime):
    events = []
    for id in eventIdArray:

        event = Event.objects.values('eventId', 'eventName', 'startDateTime',
                                     'endDateTime', 'organizerName',
                                     'eventStatus'
                                    ).get(eventId=id)
        # print(event.filter(startDateTime__gte = endDateTime).filter(endDateTime__lte = startDateTime))
        if int((event['startDateTime'].replace(tzinfo=None) - fromDateTime).total_seconds()) >= 0 and int((event['endDateTime'].replace(tzinfo=None) - toDateTime).total_seconds()) <= 0:

            categoryIdArray = Eventcategory.objects.values_list('categoryId', flat=True).filter(eventId=id)
            diff = event['endDateTime'] - event['startDateTime']
            numHours = (diff.total_seconds()) / 3600

            categories = [value for value in categoryIdArray]
            event['categoryId'] = categories
            event['numHours'] = int(numHours)
            events.append(event)
    return events


def get_volunteers_from_eventId(eventId):
    eventvolunteersids = Eventregistration.objects.values_list('userId', flat=True).filter(eventId=eventId).filter(status='attended')

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
    numHours = (diff.total_seconds())/3600

    if eventId == None:
        pass #Return error

    data = {
        "eventId": eventdetails.eventId,
        "eventName":eventdetails.eventName,
        "startDateTime":eventdetails.startDateTime,
        "endDateTime":eventdetails.endDateTime,
        "numHours": int(numHours),
        "organizerName":eventdetails.organizerName,
        "categoryId":categories,
        "eventStatus": eventdetails.eventStatus
    }
    return data

def convertDate(fromdate, todate):
    fromDateArray = (fromdate.split('-'))
    dateA = datetime.datetime(int(fromDateArray[0]),int(fromDateArray[1]),int(fromDateArray[2]))
    toDateArray = (todate.split('-'))
    dateB = datetime.datetime(int(toDateArray[0]),int(toDateArray[1]),int(toDateArray[2]))
    return(dateA,dateB)
