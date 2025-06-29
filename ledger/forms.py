from django import forms
from .models import KycDocument
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RiskProfile
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'login-input-field',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'login-input-field',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'login-input-field',
            'placeholder': 'Enter your email'
        })
    )
    enable_2fa = forms.BooleanField(
        required=False,
        label="Enable 2FA",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'login-input-field',
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'login-input-field',
            'placeholder': 'Enter a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'login-input-field',
            'placeholder': 'Confirm your password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("That email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'login-input-field',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'login-input-field',
            'placeholder': 'Enter your password'
        })

class OTPForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Enter the 6-digit code'
        })
    )

class KycForm(ModelForm):
    class Meta:
        model = KycDocument
        fields = ['document']


class AdminKycForm(ModelForm):
    class Meta:
        model = KycDocument
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class':'form-select'})
        }

class AdminAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['balance']
        widgets = {
            'balance': forms.NumberInput(attrs={'class':'form-control'})
        }

from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','is_active','is_staff','groups']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email':    forms.EmailInput(attrs={'class':'form-control'}),
            'is_active':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'groups':   forms.SelectMultiple(attrs={'class':'form-select'}),
        }

class RiskProfileForm(ModelForm):
    class Meta:
        model = RiskProfile
        fields = ['experience','goals','time_horizon','risk_tolerance']
        widgets = {
            'experience':    forms.Select(attrs={'class':'form-select'}),
            'goals':         forms.Select(attrs={'class':'form-select'}),
            'time_horizon':  forms.NumberInput(attrs={'class':'form-control','min':1}),
            'risk_tolerance':forms.Select(attrs={'class':'form-select'}),
        }


class TradeForm(forms.Form):
    TRADE_CHOICES = [('BUY', 'Buy'), ('SELL', 'Sell')]

    ticker = forms.CharField(
        label='Ticker Symbol',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control dark-input',
            'placeholder': 'e.g. AAPL'
        })
    )

    quantity = forms.DecimalField(
        label='Quantity',
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control dark-input',
            'placeholder': 'e.g. 10'
        })
    )

    trade_type = forms.ChoiceField(
        choices=TRADE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select dark-select'
        })
    )
