import json

from rest_framework import status
from rest_framework.test import APITestCase

from .models import DailyWeather, YearlyWeatherStats

# Initialize static test data

w1 = DailyWeather(id=1, station_id='station_1', date='2022-01-01', min_temp='20.20', max_temp='32.40',
                  precipitation='50.00')
w2 = DailyWeather(id=2, station_id='station_1', date='2022-01-02', min_temp='20.20', max_temp='32.40',
                  precipitation='50.00')
w3 = DailyWeather(id=3, station_id='station_2', date='2022-01-01', min_temp='20.20', max_temp='32.40',
                  precipitation='50.00')
w4 = DailyWeather(id=4, station_id='station_2', date='2022-01-02', min_temp='20.20', max_temp='32.40',
                  precipitation='50.00')

y1 = YearlyWeatherStats(id=1, station_id='station_1', year=2021, avg_min_temp='20.20', avg_max_temp='32.40',
                        total_precipitation='50.00')
y2 = YearlyWeatherStats(id=2, station_id='station_1', year=2022, avg_min_temp='20.20', avg_max_temp='32.40',
                        total_precipitation='50.00')
y3 = YearlyWeatherStats(id=3, station_id='station_2', year=2021, avg_min_temp='20.20', avg_max_temp='32.40',
                        total_precipitation='50.00')
y4 = YearlyWeatherStats(id=4, station_id='station_2', year=2022, avg_min_temp='20.20', avg_max_temp='32.40',
                        total_precipitation='50.00')

# Utility functions to convert to json

def weather_as_json(w):
    return {"id": w.id, "station_id": w.station_id, "date": w.date, "min_temp": w.min_temp, "max_temp": w.max_temp,
            "precipitation": w.precipitation}


def weather_summary_as_json(y):
    return {"id": y.id, "station_id": y.station_id, "year": y.year, "avg_min_temp": y.avg_min_temp,
            "avg_max_temp": y.avg_max_temp,
            "total_precipitation": y.total_precipitation}


# Utility functions to persist test data

def create_weather_data():
    w1.save()
    w2.save()
    w3.save()
    w4.save()


def create_summary_data():
    y1.save()
    y2.save()
    y3.save()
    y4.save()


class DailyWeatherTests(APITestCase):

    def setUp(self):
        create_weather_data()

    def test_all_results(self):
        res = self.client.get('/api/weather/')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w1), weather_as_json(w2), weather_as_json(w3), weather_as_json(w4)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_filter(self):
        res = self.client.get('/api/weather/?station_id=station_2&date=2022-01-02')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w4)]
        response_data = json.loads(res.content)
        self.assertEquals(1, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_pagination(self):
        res = self.client.get('/api/weather/?limit=2&offset=1')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w2), weather_as_json(w3)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)


class YearlyWeatherStatsTests(APITestCase):

    def setUp(self):
        create_summary_data()

    def test_all_results(self):
        res = self.client.get('/api/weather/stats')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y1), weather_summary_as_json(y2), weather_summary_as_json(y3),
                    weather_summary_as_json(y4)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_filter(self):
        res = self.client.get('/api/weather/stats?station_id=station_2&year=2022')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y4)]
        response_data = json.loads(res.content)
        self.assertEquals(1, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_pagination(self):
        res = self.client.get('/api/weather/stats?limit=2&offset=1')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y2), weather_summary_as_json(y3)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)
