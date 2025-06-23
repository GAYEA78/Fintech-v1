from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from ledger import views as ledger_views
from ledger.forms import CustomAuthForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', ledger_views.login_2fa, name='login'),
    path('accounts/verify/', ledger_views.otp_verify, name='otp_verify'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'),
        name='logout'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('ledger.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler403 = 'ledger.views.custom_permission_denied'
