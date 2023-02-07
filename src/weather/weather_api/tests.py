import json

from rest_framework import status
from rest_framework.test import APITestCase

from .test_support import *


class DailyWeatherTests(APITestCase):
    """
    Tests for Weather API
    """

    def setUp(self):
        """
        Initializes test data in DB
        """
        create_weather_data()

    def test_all_results(self):
        """
        Verify listing of all weather data
        """
        res = self.client.get('/api/weather/')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w1), weather_as_json(w2), weather_as_json(w3), weather_as_json(w4)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_filter(self):
        """
        Verify listing of weather data with filtering using station id and date
        """
        res = self.client.get('/api/weather/?station_id=station_2&date=2022-01-02')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w4)]
        response_data = json.loads(res.content)
        self.assertEquals(1, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_pagination(self):
        """
        Verify listing of weather data with pagination
        """
        res = self.client.get('/api/weather/?limit=2&offset=1')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_as_json(w2), weather_as_json(w3)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)


class YearlyWeatherStatsTests(APITestCase):
    """
    Tests for Weather Stats API
    """

    def setUp(self):
        """
        Initializes test data in DB
        """
        create_summary_data()

    def test_all_results(self):
        """
        Verify listing of weather summary data
        """
        res = self.client.get('/api/weather/stats')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y1), weather_summary_as_json(y2), weather_summary_as_json(y3),
                    weather_summary_as_json(y4)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_filter(self):
        """
        Verify listing of weather summary data with filtering based on station_id and year
        """
        res = self.client.get('/api/weather/stats?station_id=station_2&year=2022')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y4)]
        response_data = json.loads(res.content)
        self.assertEquals(1, response_data['count'])
        self.assertEquals(response_data['results'], expected)

    def test_pagination(self):
        """
        Verify listing of weather summary data with pagination
        """
        res = self.client.get('/api/weather/stats?limit=2&offset=1')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected = [weather_summary_as_json(y2), weather_summary_as_json(y3)]
        response_data = json.loads(res.content)
        self.assertEquals(4, response_data['count'])
        self.assertEquals(response_data['results'], expected)
