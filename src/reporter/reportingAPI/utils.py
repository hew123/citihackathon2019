from .models import Event, User, Eventcategory, Eventregistration

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
