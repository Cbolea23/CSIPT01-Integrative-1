from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import transaction
from decimal import Decimal
from .models import User, Account, Transaction
from .serializers import AccountSerializer
from .serializers import TransactionSerializer

class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
            Account.objects.create(user=user)
            token, _ = Token.objects.get_or_create(user=user)
            
        return Response({"message": "Registration successful", "token": token.key})

class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        account = request.user.account
        return Response(AccountSerializer(account).data)

class DepositAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        amount = Decimal(request.data.get('amount', 0))
        
        if amount <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, type='deposit', amount=amount, description='Cash Deposit')
            
        return Response({"message": "Deposit successful", "new_balance": account.balance})

class WithdrawAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        account = request.user.account
        amount = Decimal(request.data.get('amount', 0))
        
        if amount > account.balance:
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, type='withdrawal', amount=amount, description='Cash Withdrawal')
            
        return Response({"message": "Withdrawal successful", "new_balance": account.balance})
    
class TransferAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user.account
        amount = Decimal(request.data.get('amount', 0))
        destination_acc = request.data.get('destination_account')

        if amount <= 0 or amount > sender.balance:
            return Response({"error": "Invalid amount or insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
        
        if str(sender.account_number) == str(destination_acc):
            return Response({"error": "You cannot transfer to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = Account.objects.get(account_number=destination_acc)
        except Account.DoesNotExist:
            return Response({"error": "Destination account not found"}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            sender.balance -= amount
            sender.save()
            Transaction.objects.create(account=sender, type='transfer', amount=amount, description=f'Sent to {receiver.account_number}')
            
            receiver.balance += amount
            receiver.save()
            Transaction.objects.create(account=receiver, type='transfer', amount=amount, description=f'Received from {sender.account_number}')
            
        return Response({"message": "Transfer successful", "new_balance": sender.balance})

class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    def put(self, request):
        user = request.user
        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()
        return Response({"message": "Profile updated successfully!"})

class TransactionHistoryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = request.user.account.transactions.all().order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class CloseAccountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete() 
        return Response({"message": "Account successfully closed and deleted."})