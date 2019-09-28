from django.shortcuts import render

# Create your views here.
def index(request):
    a = request.GET.get('eventId', 'none')
    print(a)
    return render(request, 'index.html')
