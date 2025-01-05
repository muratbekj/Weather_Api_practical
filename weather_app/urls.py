from os import name
from django.conf.urls.i18n import urlpatterns
from django.urls import path
from weather_app.views import WeatherInfoView

urlpatterns = [
    path('weather/', WeatherInfoView.as_view(), name='weather')
]