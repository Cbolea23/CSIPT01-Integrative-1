from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from decimal import Decimal
from .models import Account, Transaction
from .serializers import AccountSerializer

class AccountDetail(APIView):
    def get(self, request):
        # For testing purposes, we grab the first account. 
        # Once login is implemented, change to: account = request.user.account
        account = Account.objects.first()
        if not account:
            return Response({"error": "No account found. Create a superuser first."}, status=404)
        return Response(AccountSerializer(account).data)

class DepositAPI(APIView):
    def post(self, request):
        account = Account.objects.first()
        amount = Decimal(request.data.get('amount', 0))
        
        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, type='deposit', amount=amount, description='Cash Deposit')
            
        return Response({"message": "Deposit successful", "new_balance": account.balance})

class WithdrawAPI(APIView):
    def post(self, request):
        account = Account.objects.first()
        amount = Decimal(request.data.get('amount', 0))
        
        if amount > account.balance:
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, type='withdrawal', amount=amount, description='Cash Withdrawal')
            
        return Response({"message": "Withdrawal successful", "new_balance": account.balance})