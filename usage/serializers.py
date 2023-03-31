from rest_framework import serializers
from usage.models import Usage

class StartChargingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usage
        fields = "__all__"