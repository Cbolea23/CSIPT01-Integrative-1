from django.urls import path
from .views import (AccountDetail, DepositAPI, WithdrawAPI, RegisterAPI, LoginAPI, 
                    TransferAPI, ProfileAPI, TransactionHistoryAPI, CloseAccountAPI, ExternalTransferAPI)

urlpatterns = [
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('account/', AccountDetail.as_view()),
    path('deposit/', DepositAPI.as_view()),
    path('withdraw/', WithdrawAPI.as_view()),
    path('transfer/', TransferAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
    path('external-transfer/', ExternalTransferAPI.as_view()),
    path('transactions/', TransactionHistoryAPI.as_view()),
    path('close-account/', CloseAccountAPI.as_view()),
]