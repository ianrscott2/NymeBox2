from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ConfigItem/<int:config_id>', views.config_by_id, name='config_by_id')
]