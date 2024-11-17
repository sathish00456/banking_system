from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Account, Transaction

def home(request):
    return render(request, 'home.html')

from decimal import Decimal

def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    context = {'account': account}
    if request.method == 'POST':
        try:
            # Convert input to Decimal for compatibility
            amount = Decimal(request.POST['amount'])
            if amount <= 0:
                context['error'] = 'Amount must be positive.'
            else:
                account.balance += amount  # Cleaner arithmetic
                account.save()
                # Log the transaction
                Transaction.objects.create(account=account, transaction_type='DEPOSIT', amount=amount)
                context['success'] = f"${amount} deposited successfully!"
        except (ValueError, Decimal.InvalidOperation):
            context['error'] = 'Invalid amount. Please enter a valid number.'
    return render(request, 'deposit.html', context)


from decimal import Decimal, InvalidOperation

def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    context = {'account': account}
    if request.method == 'POST':
        try:
            # Convert input to Decimal for precision and compatibility
            amount = Decimal(request.POST['amount'])
            if amount <= 0:
                context['error'] = 'Amount must be positive.'
            elif amount > account.balance:
                context['error'] = 'Insufficient balance.'
            else:
                # Deduct amount from account balance
                account.balance -= amount
                account.save()
                # Log the transaction
                Transaction.objects.create(account=account, transaction_type='WITHDRAWAL', amount=amount)
                context['success'] = f"${amount} withdrawn successfully!"
        except (ValueError, InvalidOperation):
            context['error'] = 'Invalid amount. Please enter a valid number.'
    return render(request, 'withdraw.html', context)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from .models import Transaction

def transaction(request):
    transactions = Transaction.objects.all()  # Retrieve all transactions
    return render(request, 'transaction.html', {'transactions': transactions})
