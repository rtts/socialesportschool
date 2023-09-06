from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', bootcamps, name='bootcamps'),
    url(r'^bootcamp/([0-9]+)/aanmelden/$', participate, name='participate'),
    url(r'^bootcamp/add/$', bootcamp, name='add_bootcamp'),
    url(r'^bootcamp/([0-9]+)/$', bootcamp, name='change_bootcamp'),
    url(r'^bootcamp/([0-9]+)/delete/$', delete_bootcamp, name='delete_bootcamp'),
    url(r'^bootcamp/([0-9]+)/deelnemers/$', participants, name='participants'),
    url(r'^deelnemer/([0-9]+)/$', participant, name='participant'),
    url(r'^deelnemer/([0-9]+)/delete/$', delete_participant, name='delete_participant'),
    url(r'^factuur/([0-9]+)/$', invoice, name='invoice'),
    url(r'^org/([0-9]+)/$', change_org, name='change_org'),
    url(r'^nieuwe_zorglocatie/$', pay, {'orgtype': 'zorg'}, name='paybig'),
    url(r'^nieuwe_sportclub/$', pay, {'orgtype': 'sport'}, name='paysmall'),
]
