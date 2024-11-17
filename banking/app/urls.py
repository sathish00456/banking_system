from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('deposit/<int:account_id>/', views.deposit, name='deposit'),  # Deposit money
    path('withdraw/<int:account_id>/', views.withdraw, name='withdraw'),  # Withdraw money
    path('transactions/', views.transaction, name='transaction'),  # View transaction history
]
