from django.shortcuts import render

# Create your views here.
def demographic(request):
    eventid = request.GET.get('eventId', None)
    if eventid == None:
        pass #Return error
    print(eventId)

    return render(request, 'index.html')

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
