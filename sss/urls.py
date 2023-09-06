from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from bootcamps.views import *

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^mijnsss/$', bootcamps, name='bootcamps'),

    # Registration views
    url(r'^aanmelden/$', Register.as_view()),
    url(r'^aanmelden/bedankt/$', thanks, name='registration_complete'),
    url(r'^aanmelden/succes/$', success, name='registration_activation_complete'),
    url(r'^aanmelden/(?P<activation_key>[-:\w]+)/', Activate.as_view(), name='registration_activate'),

    # Password reset views
    url(r'^wachtwoordvergeten/$', PasswordReset.as_view(), name='password_reset'),
    url(r'^wachtwoordvergeten/verstuurd/$', PasswordResetDone.as_view(), name='password_reset_done'),
    url(r'^wachtwoordvergeten/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    url(r'^wachtwoordvergeten/succes/$', PasswordResetComplete.as_view(), name='password_reset_complete'),

    url(r'^algemene_voorwaarden', terms, name='terms'),
    url(r'^mijnsss/', include('bootcamps.urls')),
    url(r'^$', page, name='homepage'),
    url(r'^lettertypetest/$', testpage),
    url(r'^(.*)/$', page, name='page'),
]
