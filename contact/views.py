from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from contact.serializers import ContactSerializer
from contact.models import Contact
# Create your views here.


class ContactView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response({'status':status.HTTP_200_OK,'messsage':'Contacted Us','data':serializer.data})
    
    def post(self, request):
        contacts = Contact.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        contacts.save()
        serializer = ContactSerializer(contacts, many=True)
        return redirect('/redirect')

def confirm(request):
    return render(request, 'confirm.html')

def subredirect(request):
    return render(request, 'subredirect.html')