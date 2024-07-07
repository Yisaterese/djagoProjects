from decimal import Decimal

from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

import user
from .models import Account, Transaction
from .serializer import AccountSerializer, CreateAccountSerializer, DepositSerializer, WithdrawSerializer, \
    CheckBalanceSerializer, TransferSerializer


# useSet
# combines the related classes(classes with related fields)Mixsins
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = CreateAccountSerializer


# if you are only doing a post method then, you have to define it
class Deposit(APIView):
    # specify the user who can do any form of action on the app
    permission_class = [IsAdminUser]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        transaction_details = {}
        if amount < Decimal(1):
            raise ValidationError("Invalid amount")
        account = get_object_or_404(Account, pk=account_number)
        balance = account.balance
        balance += Decimal(amount)
        Account.objects.filter(account_number=account_number).update(balance=balance)
        transaction = Transaction.objects.create(account=account, amount=amount)
        transaction_details['account_number'] = account_number
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'CREDIT'
        transaction.save()
        return Response(data=transaction_details, status=status.HTTP_200_OK)


class CheckBalance(APIView):
    permission_class = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = CheckBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = request.data['account_number']
        pin = request.data['pin']
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)
        if account.account_number != account_number:
            raise ValidationError("invalid account details")
        if account.pin != pin:
            raise ValidationError("Invalid pin")
        balance = account.balance
        transaction_details["account_number"] = account_number
        transaction_details["balance"] = balance
        message = f"""
        your new balance is {account.balance}
        """
        send_mail(subject='JAGUDA BANK',
                  message=message,
                  from_email='noreply@gmail.com',
                  recipient_list=[f'{user.email}'])
        return Response(data=transaction_details, status=status.HTTP_200_OK)


class Withdraw(APIView):
    permission_class = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = request.data['account_number']
        amount = Decimal(request.data['amount'])
        pin = request.data['pin']
        # create a dictionary for the response
        transaction_details = {}
        account = get_object_or_404(Account, pk=account_number)
        if account.account_number != account_number:
            raise ValidationError("invalid account details")
        if account.balance < amount:
            raise ValidationError("Insufficient funds")
        if account.pin != pin:
            raise ValidationError("Invalid pin")
        balance = account.balance
        balance -= amount
        Account.objects.filter(account_number=account_number).update(balance=balance)
        transaction = Transaction.objects.create(account=account, amount=amount, transaction_type="DEB")
        transaction_details["account_number"] = account_number
        transaction_details["amount"] = amount
        transaction_details["transaction_type"] = 'WITHDRAW'
        transaction.save()
        return Response(data=transaction_details,status=status.HTTP_200_OK)


@api_view()
def list_account(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# generic APIView
# class ListAccount(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer
#
#
# class AccountDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer


class TransferViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TransferSerializer(data=request.data)
        sender_account = serializer.data['sender_account']
        receiver_account = serializer.data['receiver_account']
        amount = Decimal(serializer.data['amount'])
        sender_account_from = get_object_or_404(Account, pk=sender_account)
        receiver_account_to = get_object_or_404(Account, pk=receiver_account)
        balance = sender_account_from.balance
        transaction_details = {}
        if balance > amount:
            balance -= amount
        else:
            return Response(data={"message": "Transfer failed"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transferred_balance = receiver_account_to.balance + amount
            Account.objects.filter(pk=receiver_account_to.pk).update(balance=transferred_balance)
        except Account.DoesNotExist:
            return Response(data={"message": "Transaction failed"}, status=status.HTTP_404_NOT_FOUND)
        Transaction.objects.create(
            account=receiver_account,
            amount='-'+str(amount),
            transaction_type='TRANSFER'
        )
        Transaction.objects.create(
            account=receiver_account,
            amount=amount
        )
        transaction_details['receiver_account'] = receiver_account
        transaction_details['amount'] = amount
        transaction_details['transaction_type'] = 'TRANSFER'
        return Response(data=transaction_details, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response(data="Method not supported", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(data="Method not supported", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', "PUT", 'POST', "PATCH", "DELETE"])
def account_detail(request, pk):
    if request.method == 'GET':
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "PUT":
        account = get_object_or_404(Account, pk=pk)
        serializer = CreateAccountSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# A normal post request function
@api_view(['POST'])
def deposit(request):
    if request.method == "POST":
        account_number = request.data['account_number']
        amount = request.data['amount']
        if amount < 1:
            raise ValidationError("Invalid amount")
        account = get_object_or_404(Account, pk=account_number)
        account.balance += Decimal(amount)
        account.save()
        transaction = Transaction.objects.create(account=account, amount=amount)
        transaction.save()
        return Response(data={"message": "Transaction successful"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def withdraw(request):
    if request.method == 'POST':
        account_number = request.data['account_number']
        amount = request.data['amount']
        pin = request.data['pin']
        account = get_object_or_404(Account, pk=account_number)
        if account.account_number != account_number:
            raise ValidationError("invalid account details")
        if account.balance < amount:
            raise ValidationError("Insufficient funds")
        if account.pin != pin:
            raise ValidationError("Invalid pin")
        account.balance -= amount
        account.save()
        transaction = Transaction.objects.create(account=account, amount=amount, transaction_type="DEB")
        transaction.save()
        return Response(data={"message": "Transaction successful"}, status=status.HTTP_200_OK)

# When using apiview you don't need to specify the request methods cos apiview has it inbuilt

# this is another way of creating an account
# class CreateAccount(CreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = CreateAccountSerializer
