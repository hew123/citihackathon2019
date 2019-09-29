from reportingAPI.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date



@csrf_exempt
def accounts_details(request):
    print(request.META)
    print(request)
    print(request.method)
    if request.method == "GET":
        userId = request.GET.get('userId', None)
        user = User.objects.values('userId', 'username', 'password', 'accountType', 'emailAddress', 'firstName', 'lastName', 'gender', 'dateOfBirth').get(userId__exact=userId)
        print(user)
        return JsonResponse(user)

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        print(body_data)
        dateofbirth = body_data['dateOfBirth']
        datearr = dateofbirth.split('-')
        dateOfBirth = date(int(datearr[0]), int(datearr[1]), int(datearr[2]))
        user = User.objects.create(
            username = body_data['username'],
            password = body_data['password'],
            accountType = body_data['accountType'],
            emailAddress = body_data['emailAddress'],
            firstName = body_data['firstName'],
            lastName = body_data['lastName'],
            gender = body_data['gender'],
            dateOfBirth = dateOfBirth,
        )
        createdUser = User.objects.values('userId', 'username', 'password', 'accountType', 'emailAddress', 'firstName', 'lastName', 'gender', 'dateOfBirth').get(emailAddress__exact=body_data['emailAddress'])
        return JsonResponse(createdUser)

    if request.method =="DEL":
        print('helclo')
        userId = request.GET.get('userId', None)
        #print(User.objects.filter(userId=userId))
        user = User.objects.filter(userId=userId)
        user.status = 'deleted'
        #user.update(status="deleted")
        user.save()
        print('hello')








# # for API
# from rest_framework import generics, permissions
# from .serializers import UserSerializer
# from .permissions import IsOwnerOrReadOnly
# #for API formatting
# from rest_framework.decorators import api_view # new
# from rest_framework.response import Response # new
# from rest_framework.reverse import reverse # new
# from rest_framework.views import APIView
# from reportingAPI.models import User
# from django.views.decorators.csrf import csrf_exempt
#
#
# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request,*args,**kwargs):
#         if not request.data:
#             return Response({'Error': "Please provide username/password"}, status="400")
#         print(request.data)
#         username = request.data['username']
#         password = request.data['password']
#         accounttype = request.data['accountType']
#         email = request.data['emailAddress']
#         firstname = request.data['firstName']
#         lastname = request.data['lastName']
#         gender = request.data['gender']
#         dateofbirth = request.data['dateOfBirth']
#         datearr = dateofbirth.split('-')
#         dateOfBirth = date(int(datearr[0]), int(datearr[1]), int(datearr[2]))
#
#         user = User.objects.create(username=username, password=password, accounttype='accounttype',email='email',firstname='firstname',lastname='lastname',gender='gender',dateofbirth=dateOfBirth)
#
#
#         #try:
#         #    user = CustomUser.objects.get(username=username, password=password, accounttype='accounttype',email='email',firstname='firstname',lastname='lastname',gender='gender',dateofbirth=dateOfBirth)
#         #except CustomUser.DoesNotExist:
#         #    return Response({'Error': "Invalid username/password"}, status="400")
#         if user:
#             payload = {
#             'id': user.id,
#             'email': user.email,
#             }
#             jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
#
#             return HttpResponse(
#             json.dumps(jwt_token),
#             status=200,
#             content_type="application/json",
#             )
#         else:
#             return Response(
#             json.dumps({'Error': "Invalid credentials"}),
#             status=400,
#             content_type="application/json"
#             )
#
#
#
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# #class ResetPwd():
#     #queryset = CustomUser.objects.all()
#     #serializer_class = ResetPwdSerializer
#     #pass
#
#
#
#
#
# @api_view(['GET']) # new
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#     })




@csrf_exempt
def reset_password(request):
    if request.method == "GET":
        userId = request.GET.get('userId', None)
        user = User.objects.values('username', 'emailAddress').get(userId__exact=userId)
        print(user)
        return JsonResponse(user)


@csrf_exempt
def display_all(request):
    if request.method == "GET":
        userId = request.GET.get('userId', None)
        user = User.objects.all()
        print(user)
        return JsonResponse(user)
