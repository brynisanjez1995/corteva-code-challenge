from django.db import models


class DailyWeather(models.Model):
    station_id = models.CharField(max_length=16, null=False)
    date = models.DateField(null=False)
    min_temp = models.DecimalField(max_digits=8, decimal_places=2)
    max_temp = models.DecimalField(max_digits=8, decimal_places=2)
    precipitation = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = '"weather"."daily_weather"'
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'date'], name='station_id_date_uk')
        ]


class YearlyWeatherStats(models.Model):
    station_id = models.CharField(max_length=16, null=False)
    year = models.IntegerField(null=False)
    avg_min_temp = models.DecimalField(max_digits=8, decimal_places=2)
    avg_max_temp = models.DecimalField(max_digits=8, decimal_places=2)
    total_precipitation = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = '"weather"."yearly_weather_stats"'
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'year'], name='station_id_year_uk')
        ]