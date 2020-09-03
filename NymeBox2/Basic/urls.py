from django.urls import path

from . import views

urlpatterns = [
    path('', views.nymebox_home, name='nymebox_home'),
    path('app/', views.index, name='index'),
    path('do_ftp/', views.do_ftp, name='do_ftp'),
    path('ConfigItem/<int:config_id>', views.config_by_id, name='config_by_id')
]