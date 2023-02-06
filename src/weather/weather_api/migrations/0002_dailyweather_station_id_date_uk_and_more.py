# Generated by Django 4.1.6 on 2023-02-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_api', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='dailyweather',
            constraint=models.UniqueConstraint(fields=('station_id', 'date'), name='station_id_date_uk'),
        ),
        migrations.AddConstraint(
            model_name='yearlyweatherstats',
            constraint=models.UniqueConstraint(fields=('station_id', 'year'), name='station_id_year_uk'),
        ),
    ]