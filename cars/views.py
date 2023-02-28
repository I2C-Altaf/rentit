from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from cars.models import *
from cars.serializers import *
from datetime import datetime
import stripe
from PIL import Image
from rentit.settings import BASE_DIR

stripe.api_key = "sk_test_51MdRFWSHNr2btXT7E0iaR6NYnCd2aPkGSoLmaj1YgJHdIdtv8e33WKklDTjwdNHcw5uhwEmNjDl33sBALtyKIaxO00XL8M3HRj"
YOUR_DOMAIN = 'http://127.0.0.1:8000'
# Create your views here.

# @method_decorator(login_required, name='get')
class CarsView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    template = 'car-listing.html'

    def get(self, request):
        return render(request, self.template)
    

def allcars(request):
    cars = Cars.objects.all()
    serializer = CarsSerializer(cars, many=True)
    paginator = Paginator(serializer.data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'cars': page_obj,
        'category':[i[1] for i in Cars.categories],
        'type': [i[1] for i in Cars.engine]
        }
    return render(request, 'car-listing.html', data)


@login_required
def carlist(request, **kwargs):
    ShowCars = Cars.objects.filter(id = kwargs['pk']).all()
    serializer = DetailedCarsSerializer(ShowCars, many=True)
    data = {
        'cars':serializer.data,
        'services':Services.objects.all().values(),
    }
    return render(request, 'booking.html', data)

class PopularCarView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        book = Bookings.objects.all()[:5]
        car_list = [i['cid_id'] for i in book.values()]
        ShowCars = Cars.objects.filter(id__in = car_list).all()
        serializer = DetailedCarsSerializer(ShowCars, many=True)
        return Response({'status':status.HTTP_200_OK,'messsage':'Detailed car','data':serializer.data})

    
def home(request):
    template = 'index.html'
    customers = Users.objects.all()
    cars = Cars.objects.all()
    serializer = CarsSerializer(cars, many=True)
    total_km = 0
    for i in serializer.data:
        total_km = total_km + i['total_km']
    bookings = Bookings.objects.all()
    data = {
        'cars': serializer.data,
        'customers':len(customers.exclude(is_staff = True)),
        'cars_count':len(cars),
        'total_km':total_km,
        'bookings': len(bookings),
        'staff':customers.exclude(is_staff=False),
        }
    return render(request, template, data)


def about(request):
    customers = Users.objects.all()
    data = {
            'staff':customers.exclude(is_staff=False),
            }
    return render(request, 'about.html', data)


def faq(request):
    return render(request, 'faqs.html')


@login_required
def mybook(request):
    book = Bookings.objects.filter(uid = request.user).all()
    id_list = [i.__dict__['cid_id'] for i in book]
    serializer = BookingSerializer(book, many=True)
    paginator = Paginator(serializer.data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {
        'bookings': page_obj,
        'category':[i[1] for i in Cars.categories],
        'type': [i[1] for i in Cars.engine]
        }
    for i in data['bookings']:
        i['created_at'] = datetime.strptime(i['created_at'],'%Y-%m-%dT%H:%M:%S.%fZ').date()
        i['modified_at'] = datetime.strptime(i['modified_at'],'%Y-%m-%dT%H:%M:%S.%fZ').date()
    return render(request, 'mybook.html', data)

    # def put(self, request):
    #     book = Bookings.objects.filter(uid = request.user).filter(id = request.data['id']).update(
    #         pickup_location = request.data['pickup_location'],
    #         drop_location = request.data['drop_location'],
    #         )
    #     if not book:
    #         raise serializers.ValidationError({'message':f'''Booking not Found with id {request.data['id']}'''})
    #     serializer = BookingSerializer(book, many=True)
    #     return Response({'status':status.HTTP_200_OK,'messsage':f'''Booking Location Updated Successfully for {request.user.email}'''})

@login_required
def canclebooking(request):
    book = Bookings.objects.filter(uid = request.user).filter(id = request.GET.get('b_id')).update(status = 'Cancelled')
    if not book:
        return render(request, 'error-page.html')
    serializer = BookingSerializer(book, many=True)
    # return Response({'status':status.HTTP_200_OK,'messsage':f'''Booking cancelled for {request.user.email}'''})
    return redirect('/mybook/')


def contact(request):
    return render(request, 'contact.html')

def auto(request):
    return render(request, 'auto.html')

###########################################################################################
########################################## STRIPE #########################################
###########################################################################################


@csrf_exempt
def create_checkout_session(request):
    user = Users.objects.filter(email = request.POST.get('email')).first()
    car = Cars.objects.filter(id = request.POST.get('cid')).first()
    pdate = datetime.strptime(request.POST.get('pickup_date'), '%m/%d/%Y %H:%M %p').date()
    ddate = datetime.strptime(request.POST.get('drop_date'), '%m/%d/%Y %H:%M %p').date()
    if pdate < datetime.now().date():
        messages.info(request,'Booking cannot be done for past')
        return redirect(f"/cars/{request.POST.get('cid')}")
    if ddate < pdate:
        messages.info(request,'Dropping date should be greater than pickup date')
        return redirect(f"/cars/{request.POST.get('cid')}")
    check_book = Bookings.objects.filter(cid = car).first()
    if check_book:
        if check_book.pickup_date <= pdate <= check_book.drop_date:
            messages.info(request,'Car Already Booked with the date range')
            return redirect(f"/cars/{request.POST.get('cid')}")
    if ddate.day - pdate.day == 0:
        days:int = 1
    else:
        days:int = ddate.day - pdate.day
    try:
        book = Bookings.objects.create(
            uid = user,
            cid = car,
            pickup_location = request.POST.get('pickup_location'),
            drop_location = request.POST.get('drop_location'),
            pickup_date = pdate,
            drop_date = ddate,
            amount = car.price * days,
            payment_type = "Card" 
            )
    except:
        raise serializers.ValidationError({'message':'Error While Booking'})
    serializer = BookingSerializer(book, many=True)
    if request.POST.getlist('service'):
        book.services.add(*request.POST.getlist('service'))
    service = Services.objects.filter(id__in = request.POST.getlist('service')).all()
    for i in service.values():
        book.amount = book.amount + i['price']
    #Stripe Payment 
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Car Booking',},
                    'unit_amount': round(book.amount)*100,  # Default price in paise / cents
                                            # So,convertion into rupees / dollar by multiplying with 100
                },
                'quantity': 1,
                }],
            mode='payment',
            customer_email = request.POST.get('email'),
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + f'/cancel/{book.id}'
            )
    except:
        book.delete()
        messages.info(request,'Issue with payment')
    return redirect(session.url)
    # return JsonResponse({'id': session.id})


@csrf_exempt
def webhook(request):
    print("=====>", request)
    endpoint_secret = ''
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
    # TODO: run some custom code here

    return HttpResponse(status=200)

#success view
@login_required
def success(request):
    return render(request,'success.html')

 #cancel view
def cancel(request, **kwargs):
    delete_booking = Bookings.objects.filter(id = kwargs['pk']).delete()
    return render(request,'cancel.html')