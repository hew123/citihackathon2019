from .models import Event, User, Eventcategory, Eventregistration

def get_volunteers_from_eventId(eventId):
    eventvolunteersids = Eventregistration.objects.values_list('userid', flat=True).filter(eventid=eventId)

    volunteers = []
    for id in eventvolunteersids:
        user = User.objects.values('id', 'firstname', 'lastname', 'gender',
                                   'dateofbirth', 'accounttype').get(id__exact=id)
        volunteers.append(user)
    return volunteers



