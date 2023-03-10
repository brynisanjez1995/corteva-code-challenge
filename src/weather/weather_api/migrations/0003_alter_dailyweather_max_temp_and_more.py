# Generated by Django 4.1.6 on 2023-02-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_api', '0002_dailyweather_station_id_date_uk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyweather',
            name='max_temp',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='dailyweather',
            name='min_temp',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='dailyweather',
            name='precipitation',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='yearlyweatherstats',
            name='avg_max_temp',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='yearlyweatherstats',
            name='avg_min_temp',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='yearlyweatherstats',
            name='total_precipitation',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
