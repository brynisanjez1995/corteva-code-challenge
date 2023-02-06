from rest_framework import serializers
from .models import DailyWeather, YearlyWeatherStats


class DailyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWeather
        fields = ['id', 'station_id', 'date', 'min_temp', 'max_temp', 'precipitation']


class YearlyWeatherStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyWeatherStats
        fields = ['id', 'station_id', 'year', 'avg_min_temp', 'avg_max_temp', 'total_precipitation']
