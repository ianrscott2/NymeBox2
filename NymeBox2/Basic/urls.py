from django.urls import path
#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from .Dajaxice import Dajaxice, dajaxice_autodiscover
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.nymebox_home, name='nymebox_home'),
    path('app/', views.index, name='index'),
    path('do_ftp/', views.do_ftp, name='do_ftp'),
    path('last_results/', views.last_results, name='last_results'),
    path('ConfigItem/<int:config_id>', views.config_by_id, name='config_by_id'),
    url(r'^dreamreal/', 'dreamreal', name = 'dreamreal'),
]

urlpatterns += patterns('',
   url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),)
	
urlpatterns += staticfiles_urlpatterns()