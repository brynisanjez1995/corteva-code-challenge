from django.db import models


class DailyWeather(models.Model):
    """
    Represents the weather data for a station on a particular date
    """

    station_id = models.CharField(max_length=16)
    date = models.DateField()
    min_temp = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    max_temp = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    precipitation = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        db_table = '"weather"."daily_weather"'
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'date'], name='station_id_date_uk')
        ]


class YearlyWeatherStats(models.Model):
    """
    Represents the aggregated weather data for a station by year
    """

    station_id = models.CharField(max_length=16, null=False)
    year = models.IntegerField(null=False)
    avg_min_temp = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    avg_max_temp = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    total_precipitation = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        db_table = '"weather"."yearly_weather_stats"'
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'year'], name='station_id_year_uk')
        ]