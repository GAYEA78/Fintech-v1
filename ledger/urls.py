from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),              
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('pdf-statement/', views.StatementPDFView.as_view(), name='pdf_statement'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancelled/', views.payment_cancelled, name='payment_cancelled'),
]
