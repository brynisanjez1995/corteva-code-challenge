from rest_framework import generics

from .models import DailyWeather, YearlyWeatherStats
from .serializers import DailyWeatherSerializer, YearlyWeatherStatsSerializer


class DailyWeatherList(generics.ListAPIView):
    """
    API view that handles GET requests to search weather data
    """

    serializer_class = DailyWeatherSerializer

    def get_queryset(self):
        qs = DailyWeather.objects.all()
        station_id = self.request.query_params.get('station_id')
        date = self.request.query_params.get('date')
        if station_id:
            qs = qs.filter(station_id=station_id)
        if date:
            qs = qs.filter(date=date)
        if not qs:
            return None
        return qs


class YearlyWeatherStatsList(generics.ListAPIView):
    """
    API view that handles GET requests to search weather summary data
    """

    serializer_class = YearlyWeatherStatsSerializer

    def get_queryset(self):
        qs = YearlyWeatherStats.objects.all()
        station_id = self.request.query_params.get('station_id')
        year = self.request.query_params.get('year')
        if station_id:
            qs = qs.filter(station_id=station_id)
        if year:
            qs = qs.filter(year=year)
        if not qs:
            return None
        return qs
