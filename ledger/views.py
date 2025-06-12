from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views import View
from django.http import HttpResponse
import stripe
from django.conf import settings
from reportlab.pdfgen import canvas
from .models import Account, Transaction

stripe.api_key = settings.STRIPE_API_KEY

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(group)
            Account.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'ledger/signup.html', {'form': form})

@login_required
def dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = account.transactions.order_by('-timestamp')[:10]
    return render(request, 'ledger/dashboard.html', {
        'account': account,
        'transactions': transactions
    })

class StatementPDFView(View):
    def get(self, request):
        account = Account.objects.get(user=request.user)
        transactions = account.transactions.order_by('-timestamp')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="statement.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Statement for {request.user.username}")
        y = 750
        for tx in transactions:
            p.drawString(100, y,
                f"{tx.timestamp.strftime('%Y-%m-%d')} - "
                f"{tx.get_transaction_type_display()} - "
                f"${tx.amount} - {tx.description}"
            )
            y -= 20
            if y < 50:
                p.showPage()
                y = 800
        p.save()
        return response

def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Account Deposit'},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancelled/'),
    )
    return redirect(session.url, code=303)

def payment_success(request):
    account = Account.objects.get(user=request.user)
    account.balance += 10
    account.save()
    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.CREDIT,
        amount=10,
        description='Stripe deposit'
    )
    return render(request, 'ledger/success.html')

def payment_cancelled(request):
    return render(request, 'ledger/cancelled.html')
