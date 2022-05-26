from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from userAuth.serializers import CustomUserSerializer, LogoutSerializer
from userAuth.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from datetime import date, datetime
import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserViewById(APIView):
    # Get User By Id
    def get(self, request, id):
        """get() function takes id as input and returns respective user"""
        user = CustomUser.objects.get(id = id)
        user_serializer = CustomUserSerializer(user)
        return JsonResponse(user_serializer.data, safe=False)


    # Delete User
    @csrf_exempt
    def delete(self, request, id):
        """ Takes user id as input to delete user from database"""
        user = CustomUser.objects.get(id = id)
        user.delete()
        return JsonResponse("record deleted", safe=False)


    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, title='First Name', description='string'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, title= 'Last Name', description='string'),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, title='Date of Birth', description='string in yyyy-mm-dd'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, title='Phone Number', description='string'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, title='Address', description='string'),
        },
        required=['first_name', 'last_name', 'date_of_birth', 'phone_number', 'address']
    ))
    @permission_classes([IsAdminUser])
    @csrf_exempt
    def put(self, request, id):   
        """Update user details"""
        print("Id  == ", id)
        token = str(request.auth)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = CustomUser.objects.get(id = payload['user_id'])
        if user.is_staff is True:
            user_data = JSONParser().parse(request)
            date_str = user_data['date_of_birth']
            date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            age = date.today().year - date_time_obj.year
            user_data['age'] = age
            user_old_data = CustomUser.objects.get(id = id)
            user_data['password'] = user_old_data.password    
            user_serializer = CustomUserSerializer(user_old_data, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse("record updated", safe=False, status = status.HTTP_200_OK)
            return JsonResponse("Failed to update", safe=False, status = status.HTTP_400_BAD_REQUEST)            
        return JsonResponse("Only admin can update user details", safe=False, status = status.HTTP_400_BAD_REQUEST)    


class UserView(APIView):
     # Get All Users
    def get(self, request, id=''):
        """Returns list of all users"""
        users = CustomUser.objects.all()
        user_serializer = CustomUserSerializer(users, many = True)
        return JsonResponse(user_serializer.data, safe=False)


    # Update User Details
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'email': openapi.Schema(type=openapi.TYPE_STRING, title='Email', description='string'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, title='First Name', description='string'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, title= 'Last Name', description='string'),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, title='Date of Birth', description='string in yyyy-mm-dd'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, title='Phone Number', description='string'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, title='Address', description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, title='Password', description='string'),
        },
        required=['first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'password']
    ))
    @permission_classes([IsAdminUser])
    @csrf_exempt
    def put(self, request):   
        """Update user details"""
        token = str(request.auth)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_data = JSONParser().parse(request)
        date_str = user_data['date_of_birth']
        date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        age = date.today().year - date_time_obj.year
        user_data['age'] = age
        user = CustomUser.objects.get(id = payload['user_id'])
        if check_password(encoded=user.password, password=user_data['password']):
            user_data['password'] = make_password(user_data['password'])
        else :
            return JsonResponse("Please enter correct password", safe=False, status = status.HTTP_400_BAD_REQUEST)    
        user_serializer = CustomUserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("record updated", safe=False, status = status.HTTP_200_OK)
        return JsonResponse("Failed to update", safe=False, status = status.HTTP_400_BAD_REQUEST)    


# Update Password
@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'password1': openapi.Schema(type=openapi.TYPE_STRING, title='Password', description='string'),
        'password2': openapi.Schema(type=openapi.TYPE_STRING, title='Confirm Password', description='string'),
    },
    required=['password1', 'password2']

))
@api_view(['PUT'])
@csrf_exempt
def update_password(request):
    """Update password"""
    token = str(request.auth)            
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])        
    user_data = JSONParser().parse(request)
    user = CustomUser.objects.get(id = payload['user_id'])
    if user_data['password1'] == user_data['password2']:
        user_data['password'] = make_password(user_data['password1'])
        user_serializer = CustomUserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("password updated", safe=False, status = status.HTTP_200_OK)
    return JsonResponse("Failed to update password", safe=False, status = status.HTTP_400_BAD_REQUEST)      


# Register User and Mail Verification 
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, title="Email", description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, title="Password", description='string'),
    },
    required=['email', 'password'],
))
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    """ Takes email Id and password and sends a verification link on mail Id"""
    user = JSONParser().parse(request)
    user['password'] = make_password(user['password'])
    user_serializer = CustomUserSerializer(data=user)
    print("==",user_serializer)
    if user_serializer.is_valid():
        user_serializer.save()
        user_data = user_serializer.data
        user = CustomUser.objects.get(email = user_data['email']) 
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain  
        relative_link = reverse('verify-email')            
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hello use this link for account activation\n'+absurl
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':"Verify your email"}
        Util.send_mail(data)
        return JsonResponse("Verification mail sent", safe=False, status= status.HTTP_200_OK)
    return JsonResponse("Failed to send mail", safe=False, status = status.HTTP_400_BAD_REQUEST)


# Register Admin and Mail Verification
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, title="Email", description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, title="Password",  description='string'),
    },
    required=['email', 'password'],
))
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def register_admin(request):
    """ Takes email Id and password and sends a verification link on mail Id"""
    # if request.method == 'POST':
    user = JSONParser().parse(request)
    user['password'] = make_password(user['password'])
    user_serializer = CustomUserSerializer(data=user)
    if user_serializer.is_valid():
        user_serializer.validated_data['is_superuser'] = True
        user_serializer.validated_data['is_staff'] = True
        user_serializer.save()
        user_data = user_serializer.data
        user = CustomUser.objects.get(email = user_data['email']) 
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain  
        relative_link = reverse('verify-email')            
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hello use this link for account activation\n'+absurl
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':"Verify your email"}
        Util.send_mail(data)
        return JsonResponse("Verification mail sent", safe=False)
    return JsonResponse("Failed to send mail", safe=False)

   
# Verifies token sent to mail id   
def verify_email(request):
    token = request.GET.get('token')            
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user = CustomUser.objects.get(id=payload['user_id'])
    user.is_active = True
    user.save()
    return JsonResponse("email activated", safe=False)
      

# Reset Password via Mail
@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email':openapi.Schema(type=openapi.TYPE_STRING, title='Email', description='string')
    },
    required=['email']
))
@api_view(['PUT'])    
def reset_password_request(request):
    """Takes mail Id as input and sends password reset link on mail"""
    user = JSONParser().parse(request)
    user_data = CustomUser.objects.get(email = user['email'])
    token = RefreshToken.for_user(user_data).access_token
    current_site = get_current_site(request).domain
    relative_link = reverse('reset-password')
    absurl = 'http://'+current_site+relative_link+'?token='+str(token)
    email_body = 'Hello \n use this link to reset your password\n'+absurl
    data ={'email_body':email_body, 'to_email': user_data.email, 'email_subject': 'Reset your password'}
    Util.send_mail(data)
    return JsonResponse("password reset mail sent", safe=False, status = 200)


# Redirects user to web page where user can enter new password
def reset_password(request):
    token = request.GET.get('token') 
    token_dict = {'token':token}
    return render(request, "reset_password.html", token_dict)


@csrf_exempt
def reset_password1(request):
    token = request.POST['token']         
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    if request.POST['password'] == request.POST['confirm_password']:
        user = CustomUser.objects.get(id=payload['user_id'])
        user.password = make_password(request.POST['password'])
        user.save()
        return JsonResponse("password changed ", safe=False)
    return JsonResponse("password does not match", safe=False)


# Logout User
@api_view(['POST'])
def logout(request):
    serializer_class = LogoutSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return JsonResponse("Logged out", safe=False) 


