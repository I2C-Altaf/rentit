from rest_framework import serializers
from cars.models import Cars, Bookings, Reviews, Services


class CarsSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    
    def get_review(self, obj):
        query = Reviews.objects.filter(cid = obj.id).all()
        review = ReviewSerializer(query, many=True)
        return review.data
    
    class Meta:
        model = Cars
        # fields = "__all__"
        exclude = ('created_at','modified_at')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = "__all__"
        exclude = ('id','created_at','modified_at')


class DetailedCarsSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()

    def get_review(self, obj):
        query = Reviews.objects.filter(cid = obj.id).all()
        review = ReviewSerializer(query, many=True)
        return review.data

    class Meta:
        model = Cars
        # fields = "__all__"
        exclude = ('created_at','modified_at')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many = True)

    class Meta:
        model = Bookings
        fields = "__all__"
