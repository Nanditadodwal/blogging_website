# from msilib.schema import ListView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from home.helpers import generate_random_string
from .models import BlogModel, Profile
from .helpers import *
from django.conf import settings


# class UserBlogView(ListView):
#     model = BlogModel
#     context_object_name = 'users'
#     template_name='home/BlogModel_home.html'
#     paginate_by = 5
#     queryset = BlogModel.objects.all()

class LoginView(APIView):
    # paginating_class = settings.DEFAULT_PAGINATION_CLASS
   
    def post(self, request):
        
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'Key username not found'
                raise Exception('key username not found')
            if data.get('password') is None:
                response['message'] = 'Key password not found'
                raise Exception('key password not found')
            
            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user is None:
                response['message'] = 'Invalid Username '
                raise Exception('Invalid Username')

            if not Profile.objects.filter(user = check_user).first().is_verified:
                   response['message'] = 'Invalid Profile '
                   raise Exception('Invalid Profile')

            user_obj = authenticate(username= data.get('username'), password= data.get('password'))  

            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = 'Welcome!'
            else:
                response['message'] = 'Invalid password '
                raise Exception('Invalid password')



        except Exception as e:
            print(e)

        return Response(response)


LoginView = LoginView.as_view()



class RegisterView(APIView):

    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'Key username not found'
                raise Exception('key username not found')

            if data.get('password') is None:
                response['message'] = 'Key password not found'
                raise Exception('key password not found')
            
            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user:
                response['message'] = 'Username already taken'
                raise Exception('Username already taken')

            user_obj = User.objects.create(email= data.get('username'), username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_random_string(20)
            Profile.objects.create(user = user_obj, token = generate_random_string(20))
            send_mail_to_user(token, data.get('username'))
            response['message'] = 'User created successfully!'
            response['status'] = 200




        except Exception as e:
            print(e)

        return Response(response)

RegisterView = RegisterView.as_view()