from django.urls import path, include
from .views import portfolio_list
from . import views

urlpatterns = [
    path('', portfolio_list, name='portfolio_list'),
    path('rebalance/manual/', views.manual_rebalance, name='manual_rebalance'),	
    path('rebalance/manual/apply/', views.apply_manual_rebalance, name='apply_manual_rebalance'),	
]
