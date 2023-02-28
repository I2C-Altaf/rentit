from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Users
# Create your models here.

class Services(models.Model):
    service_name = models.CharField(max_length=1000)
    price = models.PositiveIntegerField(blank=False, unique=False)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Service"
    
    def __str__(self):
        return str(self.service_name)

class Cars(models.Model):
    brand_name = models.CharField(max_length=1000)
    categories = [
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
        ('MUV', 'MUV'),
        ('SUV', 'SUV'),
        ('Sedan', 'Sedan'),
        ('Hatchback', 'Hatchback'),
    ]
    category = models.CharField(choices=categories, max_length=1000, default='Sedan')
    description = models.CharField(max_length=1500)
    model_year = models.CharField(max_length=1000)
    engine = [
        ('Electric', 'Electric'),
        ('Diesel', 'Diesel'),
        ('Petrol','Petrol'),
    ]
    engine_type = models.CharField(choices=engine, max_length=1000, default='Petrol')
    gear = [
        ('Auto', 'Auto'),
        ('Manual', 'Manual'),
    ]
    gear_type = models.CharField(choices=gear, max_length=1000, default='Manual')
    total_km = models.PositiveBigIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(blank=True, null=True, upload_to='media/')
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cars"
        verbose_name_plural = "Cars"
    
    def __str__(self):
        return str(self.brand_name)
    

class Discount(models.Model):
    name = models.CharField(max_length=1000)
    discount_percentage = models.FloatField(validators=[MaxValueValidator(99.99)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
    
    def __str__(self):
        return str(self.name)


class Bookings(models.Model):
    BOOKING_STATUS_BOOKED = 'Booked'
    BOOKING_STATUS_CANCELLED = 'Cancelled'
    BOOKING_STATUS_CHOICES = [
        (BOOKING_STATUS_BOOKED, 'Booked'),
        (BOOKING_STATUS_CANCELLED ,'Cancelled')
    ]
    
    uid = models.ForeignKey(Users, on_delete=models.CASCADE)
    cid = models.ForeignKey(Cars, on_delete=models.CASCADE)
    pickup_location = models.TextField(null=False)
    drop_location = models.TextField(null=False)
    pickup_date = models.DateField(null=False)
    drop_date = models.DateField(null=False)
    pickup_hour = models.TimeField(null=False, default="09:00:00")
    drop_hour = models.TimeField(null=False, default="21:00:00")
    discount_id = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=1000,choices=BOOKING_STATUS_CHOICES, default=BOOKING_STATUS_BOOKED)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    payment_type = models.CharField(max_length=1000, default="Card")
    services = models.ManyToManyField(Services, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bookings"
        verbose_name_plural = "Bookings"
    
    def __str__(self):
        return str(self.uid)

class Reviews(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False)
    cid = models.ForeignKey(Cars, on_delete=models.CASCADE, blank=False)
    review = models.TextField()
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return str(self.review)
