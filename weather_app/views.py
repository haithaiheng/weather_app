from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import JsonResponse
from .models import City
from django.contrib import messages

# Create your views here.
def home(request):
    # city = 'phnom penh'
    api_key = '483f477eff3167d4a7c481a325cef73d'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        city_name = request.POST.get('city')
        response = requests.get(url.format(city_name,api_key)).json()
        if response['cod'] == 200:
            if not City.objects.filter(name=city_name).exists():
                City.objects.create(name=city_name)
                messages.success(request, f'{city_name} has been addes successfully')
            else:
                messages.info(request, f'{city_name} already existed!')
        else:
            messages.error(request, f'City {city_name} not found.')
        return redirect('home')
    
    weather_data = []
    try:
        cities = City.objects.all()
        for city in cities:
            response = requests.get(url.format(city.name,api_key))
            data = response.json()
            
            if data['cod'] == 200:
                city_weather = {
                    'city': city.name,
                    'temp': data['main']['temp'],
                    'desc': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                weather_data.append(city_weather)
            else:
                City.objects.filter(name=city.name).delete()
    except requests.RequestException as e:
        print(e)

    context = {'weather_data': weather_data}
    return render(request, 'index.html', context)