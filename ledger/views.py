from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.core.mail import send_mail
import stripe
from reportlab.pdfgen import canvas
from .forms import CustomAuthForm
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from .models import OtpCode, Account, Transaction, KycDocument
from .forms import SignUpForm, OTPForm, KycForm

stripe.api_key = settings.STRIPE_API_KEY

def home(request):
    return render(request, 'ledger/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name='customer')
            user.groups.add(group)
            Account.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'ledger/signup.html', {'form': form})


def login_2fa(request):
    if request.method == 'POST':
        form = CustomAuthForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            otp = OtpCode.generate_for(user)
            print(f"[DEBUG] Generated OTP for {user.email}: {otp.code}")

            # Send via Gmail SMTP
            send_mail(
                'Your Arona Bank Login Code',
                f'Your one-time login code is: {otp.code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            request.session['pre_2fa_user'] = user.id
            return redirect('otp_verify')
    else:
        form = CustomAuthForm()
    return render(request, 'registration/login.html', { 'form': form })


def otp_verify(request):
    user_id = request.session.get('pre_2fa_user')
    if not user_id:
        return redirect('login')
    user = get_user_model().objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            otp = OtpCode.objects.filter(user=user, code=code).order_by('-created_at').first()
            if otp and not otp.is_expired():
                login(request, user)
                otp.delete()
                return redirect('dashboard')
            form.add_error('code', 'Invalid or expired code')
    else:
        form = OTPForm()
    return render(request, 'registration/otp_verify.html', {'form': form})

@login_required
def dashboard(request):
    account, created = Account.objects.get_or_create(
        user=request.user,
        defaults={'balance': Decimal('0.00')}
    )
    transactions = account.transactions.order_by('-timestamp')[:10]
    return render(request, 'ledger/dashboard.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
def kyc_upload(request):
    if request.method == 'POST':
        form = KycForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect('kyc_status')
    else:
        form = KycForm()
    return render(request, 'ledger/kyc_upload.html', {'form': form})

@login_required
def kyc_status(request):
    docs = KycDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'ledger/kyc_status.html', {'docs': docs})

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
            p.drawString(
                100, y,
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
    if request.method != 'POST':
        return redirect('dashboard')
    amt = request.POST.get('amount')
    try:
        dollars = float(amt)
        if dollars <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return redirect('dashboard')
    cents = int(dollars * 100)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': f'Account Deposit - ${dollars:.2f}'},
                'unit_amount': cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/cancelled/'),
    )
    return redirect(session.url, code=303)

def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('dashboard')
    session = stripe.checkout.Session.retrieve(session_id)
    dollars = session.amount_total / 100
    account = Account.objects.get(user=request.user)
    account.balance += Decimal(str(dollars))
    account.save()
    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.CREDIT,
        amount=Decimal(str(dollars)),
        description=f"Stripe deposit (${dollars:.2f})"
    )
    return render(request, 'ledger/success.html')

def payment_cancelled(request):
    return render(request, 'ledger/cancelled.html')
