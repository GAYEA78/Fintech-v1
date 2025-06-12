from django.contrib import admin
from .models import KycDocument, Account, Transaction

@admin.register(KycDocument)
class KycDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'status', 'uploaded_at')
    list_filter = ('status', 'uploaded_at', 'user')
    actions = ['mark_approved', 'mark_rejected']

    @admin.action(description='Mark selected documents as Approved')
    def mark_approved(self, request, queryset):
        queryset.update(status=KycDocument.APPROVED)

    @admin.action(description='Mark selected documents as Rejected')
    def mark_rejected(self, request, queryset):
        queryset.update(status=KycDocument.REJECTED)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp', 'description')
    list_filter = ('transaction_type', 'timestamp', 'account')
    search_fields = ('account__user__username', 'description')
