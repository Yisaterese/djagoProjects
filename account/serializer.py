from django.db.models import Model
from rest_framework import serializers
from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'transactions']


class DepositSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20,decimal_places=2)


class TransferSerializer(serializers.Serializer):
    sender_account = serializers.CharField(max_length=10)
    receiver_account = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=15,decimal_places=2)


class WithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=20,decimal_places=2)
    pin = serializers.CharField(max_length=4,min_length=4)


class CheckBalanceSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=10)
    pin = serializers.CharField(max_length=4,min_length=4)


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Account
        fields = ["account_number", "first_name", "last_name", "balance", "account_type", 'transactions']


# Serializer for creating an account
class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user", "account_number", "pin", "account_type"]
