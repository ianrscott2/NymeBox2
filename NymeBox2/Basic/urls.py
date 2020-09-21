from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.nymebox_home, name='nymebox_home'),
    path('FTPLog/', views.FTPLog, name='FTPLog'),
    path('ftpCheck_home/', views.nymebox_home, name='ftpCheck_home'),
    path('app/', views.index, name='index'),
    path('do_ftp/', views.do_ftp, name='do_ftp'),
    path('last_results/', views.last_results, name='last_results'),
    path('ConfigItem/<int:config_id>', views.config_by_id, name='config_by_id'),
    path('do_ftp/FTPLog', views.FTPLog, name='FTPLog'),
    path('ftpCheck/', views.ftpCheck, name='ftpCheck'),
    path(r'^pics/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': config.PICS_FILE_FOLDER}),
              ))
]