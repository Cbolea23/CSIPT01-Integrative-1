from django.urls import path
from .views import AccountDetail, DepositAPI, WithdrawAPI

urlpatterns = [
    path('account/', AccountDetail.as_view()),
    path('deposit/', DepositAPI.as_view()),
    path('withdraw/', WithdrawAPI.as_view()),
]