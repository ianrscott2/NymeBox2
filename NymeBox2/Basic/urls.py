from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.nymebox_home, name='nymebox_home'),
    path('do_ftp/', views.do_ftp, name='do_ftp'),
    path('last_results/', views.last_results, name='last_results'),
    path('ConfigItem/<int:config_id>', views.config_by_id, name='config_by_id'),
    path('ftpCheckList/', views.ftpCheckList, name='ftpCheckList'),
    path('mount_sdcard/', views.mount_sdcard, name='mount_sdcard'),
    path('ftpCheck/', views.ftpCheck, name='ftpCheck'),
]