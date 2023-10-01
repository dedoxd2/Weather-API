from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.


def index(request):  # sourcery skip: move-assign

    url = "http://api.openweathermap.org./data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    if cities:
        for city in cities:
            data_url = url + str(city)
            try:
                response = requests.get(data_url).json()
                city_weather = {
                    'city': city.name,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                }

                weather_data.append(city_weather)
            except Exception:
                print("There is No Country With This Name ")

    return render(request, 'weather.html', {'weather_data': weather_data, 'form': form})
