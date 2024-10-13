from rest_framework import serializers
from .models import Deposite
from account.models import CustomUser

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposite
        fields = ['user','amount']
        read_only_fields = ['user',]

    def validate_amount(self, value):
        min_deposit_amount = 100
        if value < min_deposit_amount:
            raise serializers.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        return value

