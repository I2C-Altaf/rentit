from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from accounts.email import send_otp_email
from accounts.token import get_tokens_for_user
from accounts.serializers import *
from rentit.settings import MEDIA_DIR

import os
# Create your views here.

def login(request):
    url:str = request.get_full_path()
    try:
        next = url.split('?next=')[1]
    except:
        next = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(username = email, password =password)
        if user is not None:
            auth.login(request , user)
            return redirect('/cars/all' if not next else next)
        else:
            messages.info(request, 'invalid username or password')
            return redirect("/accounts/login")
    else:
        return render(request,'login.html')

def handle_uploaded_file(file):
    with open(os.path.join(f"{MEDIA_DIR}/{file.name}"), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

@csrf_exempt
def signup(request):
    if request.method == "POST":
        
        if request.POST.get('password') != request.POST.get('password2'):
            messages.info(request,"Password fields didn't match.")

        try:
            validate_email(request.POST.get('email'))
        except ValidationError as e:
            print("bad email, details:", e)
        else:
            print("good email")
        
        if str(request.FILES['testimage']).split('.')[-1].lower() == "jpg":
            user = Users.objects.create(
                username = request.POST.get('name'),
                email = request.POST.get('email'),
                password = make_password(request.POST.get('password')),
                phone = request.POST.get('phone'),
                profile = request.FILES['testimage']
            )
            user.save()
            files = request.FILES['testimage']
            handle_uploaded_file(files)
            return redirect("/accounts/login")
        else:
            messages.info(request,"Only .jpg Images allowed")
            return render(request,'signup.html')
    else:
    # serializer = AccountSerializer(user, many=True)
        return render(request,'signup.html')

    # def put(self, request):
    #     permission_classes = (IsAuthenticated,)
    #     user = Users.objects.filter(id=request.user.id).update(
    #         username = request.data['username'],
    #         phone = request.data['phone']
    #         )
    #     if not user:
    #         raise serializers.ValidationError({"message":"User not Found / Unable to Update Profile"})
    #     serializer = AccountSerializer(user, many=True)
    #     return Response({'status':status.HTTP_200_OK,'message':f'''Profile for {request.user.email} Updated'''})

    # def delete(self, request):
    #     permission_classes = (IsAuthenticated,)
    #     user = Users.objects.filter(id=request.user.id).first()
    #     check = check_password(request.data['password'], user.password)
    #     if check == False:
    #         raise serializers.ValidationError({"message": "Password does not match"})
    #     user.delete()
    #     serializer = AccountSerializer(user, many=True)
    #     return Response({'status':status.HTTP_200_OK,'message':f'''Sad to see you go {request.user.email}'''})


class OtpView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = Users.objects.filter(email=request.data['email']).first()
        if user:
            OTP = send_otp_email(request.data['email'])
            user = Users.objects.filter(email=request.data['email']).update(
                otp = OTP
                )
        else:
            raise serializers.ValidationError({"message": "User Doesn't Exists.."})
        serializer = AccountSerializer(user, many=True)
        return Response({'status':status.HTTP_200_OK,'message':f'''OTP Generated'''})


class OtpVerifyView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = Users.objects.filter(email=request.data['email']).first()
        if user:
            if str(user.otp) != str(request.data['otp']):
                raise serializers.ValidationError({"message": "OTP Didn't Match Generate another.."})
            user = Users.objects.filter(email=request.data['email']).update(otp="")
        else:
                raise serializers.ValidationError({"message":"User Doesn't Exists.."})
        serializer = AccountSerializer(user, many=True)
        return Response({'status':status.HTTP_200_OK,'message':f'''OTP Verified for {request.data['email']}'''})


class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.data['password'] != request.data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        user = Users.objects.filter(id=request.user.id).update(password = make_password(request.data['password']))
        serializer = AccountSerializer(user, many=True)
        return Response({'status':status.HTTP_200_OK,'message':f'''Password Changed for {request.user.email}'''})



def subscribe(self, request):
    user = Users.objects.filter(email = request.POST.get('email')).update(is_subscribed = True)
    return redirect('/redirect')
    

class CardView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        ShowCard = Cards.objects.filter(uid = Users.objects.filter(id=request.user.id).first()).all()
        if not ShowCard:
            raise serializers.ValidationError({'status':status.HTTP_404_NOT_FOUND,"message": "It's Empty here..."})
        serializer = CardSerializer(ShowCard, many=True)
        return Response({'status':status.HTTP_200_OK,'messsage':f'''{request.user.email}'s cards''','data':serializer.data})

    def post(self, request):
        user = Users.objects.filter(id=request.user.id).first()
        cards = Cards.objects.create(
            uid = user,
            number = request.data['number'],
            month = request.data['month'],
            year = request.data['year'],
            code = request.data['code']
        )
        cards.save()
        serializer = CardSerializer(cards, many = True)
        return Response({'status':status.HTTP_200_OK,'message':f'''Card Added for {request.user.email}'''})
    
    def put(self, request):
        card = Cards.objects.filter(uid = request.user.id).filter(id= request.data['card_id']).update(
            number = request.data['number'],
            month = request.data['month'],
            year = request.data['year'],
            code = request.data['code']
        )
        if not card:
            raise serializers.ValidationError({"message":"Card Not Found / Unable to update card"})
        serializer = CardSerializer(card, many = True)
        return Response({'status':status.HTTP_200_OK,'message':f'''Card Updated for {request.user.email}'''})

    def delete(self, request):
        Card = Cards.objects.filter(uid = Users.objects.filter(id=request.user.id).first()).filter(id = request.data['id'])
        if not Card:
            raise serializers.ValidationError({'status':status.HTTP_404_NOT_FOUND,"message": "Card Not Found"})
        Card.delete()
        serializer = CardSerializer(Card, many = True)
        return Response({'status':status.HTTP_200_OK,'messsage':f'''{request.user.email}'s card Deleted'''})

def lout(request):
    logout(request)
    return redirect('/home/')