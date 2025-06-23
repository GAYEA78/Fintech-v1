from django.contrib import admin
from .models import ModelPortfolio, PortfolioLine

@admin.register(ModelPortfolio)
class ModelPortfolioAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PortfolioLine)
class PortfolioLineAdmin(admin.ModelAdmin):
    list_display = ('portfolio','asset','target_pct')
    list_filter  = ('portfolio',)
