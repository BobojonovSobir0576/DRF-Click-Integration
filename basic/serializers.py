from rest_framework import serializers
from .models import ClickOrder

class ClickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickOrder
        fields = ["amount", "is_paid"]