from rest_framework import serializers
from accounts.models import Users, Cards


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = "__all__"