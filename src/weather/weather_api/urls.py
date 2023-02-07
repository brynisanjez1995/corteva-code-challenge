from django.urls import path

from .views import DailyWeatherList, YearlyWeatherStatsList

urlpatterns = [
    path('', DailyWeatherList.as_view()),
    path('stats', YearlyWeatherStatsList.as_view())
]
