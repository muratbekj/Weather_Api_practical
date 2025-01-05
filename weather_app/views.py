import datetime
import requests
from django.shortcuts import render 
from django.views.generic import TemplateView

class WeatherInfoView(TemplateView):
    template_name = 'weather_app/index.html'
    api_key_file = 'API_KEY'

    def get_context_data(self, **kwargs):
        # Default behavior for GET requests
        context = super().get_context_data(**kwargs)
        city1 = self.request.GET.get('city1')
        city2 = self.request.GET.get('city2', None)

        if city1:
            try:
                weather_data1 = self.fetch_current_weather(city1)
                context['weather_data1'] = weather_data1
                context['city1'] = city1
            except ValueError as e:
                context['error'] = str(e)

        if city2:
            try:
                weather_data2 = self.fetch_current_weather(city2)
                context['weather_data2'] = weather_data2
                context['city2'] = city2
            except ValueError as e:
                context['error'] = str(e)

        return context

    def post(self, request, *args, **kwargs):
        # Handle POST request
        context = self.get_context_data(**kwargs)
        API_KEY = open(self.api_key_file, 'r').read()
        city1 = request.POST.get('city1')
        city2 = request.POST.get('city2', None)

        try:
            if city1:
                weather_data1 = self.fetch_current_weather(city1, API_KEY)
                context['weather_data1'] = weather_data1

            if city2:
                weather_data2 = self.fetch_current_weather(city2, API_KEY)
                context['weather_data2'] = weather_data2

        except ValueError as e:
            context['error'] = str(e)

        return self.render_to_response(context)

    def fetch_current_weather(self, city, api_key):
        current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
        response = requests.get(current_weather_url.format(city, api_key)).json()

        # Check if the response contains the necessary weather data
        if response.get('cod') != 200:
            raise ValueError(f"Error fetching current weather for {city}: {response.get('message', 'Unknown error')}")

        # Process current weather data
        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),  # Convert from Kelvin to Celsius
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        return weather_data