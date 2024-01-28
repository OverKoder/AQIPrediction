import os
import datetime

from . import forecast as fcast
import requests
from django.shortcuts import render
from dotenv import load_dotenv

def home(request):
	
	load_dotenv()

	response = requests.get("https://api.waqi.info/feed/valencia/?token=" + os.getenv("API_TOKEN")).json()

	# Get air quality
	aqi = response['data']['aqi']
	
	# Get other air components
	iaqi = response['data']['iaqi']

	if aqi <= 50:
		display_aqi = "Good"
		aqi_description = "Air quality is satisfactory, and air pollution poses little to no risk."
		aqi_color = "good"

	elif aqi <= 100:
		display_aqi = "Moderate"
		aqi_description = "Air quality is acceptable. There may be a risk for people who are unusually sensitive to air pollution."
		aqi_color = "moderate"

	elif aqi <= 150:
		display_aqi = "Unhealthy for Sensitive Groups"
		aqi_description = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
		aqi_color = "sensitive"

	elif aqi <= 200:
		display_aqi = "Unhealthy in general"
		aqi_description = "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
		aqi_color = "unhealthy"

	elif aqi <= 300:
		display_aqi = "Very Unhealthy in general"
		aqi_description = "The risk of health effects is increased for everyone."
		aqi_color = "veryunhealthy"

	else:
		display_aqi = "Extremely Dangerous"
		aqi_description = "Everyone is very likely to be affected. Outside activity is highly unrecommended"
		aqi_color = "dangerous"

	# Get forecast
	models = fcast.load_models()
	forecast = fcast.get_forecast(models)

	today = datetime.datetime.now()
	context = {
		'today': today.strftime("%d/%m/%y"),
		'next_day_1': (today + datetime.timedelta(1)).strftime("%d/%m/%y"),
		'next_day_2': (today + datetime.timedelta(2)).strftime("%d/%m/%y"),
		'next_day_3': (today + datetime.timedelta(3)).strftime("%d/%m/%y"),
		'next_day_4': (today + datetime.timedelta(4)).strftime("%d/%m/%y"),
		'aqi': aqi,
		'display_aqi': display_aqi, 
		'location': "Valencia", 
		'aqi_description': aqi_description,
		'aqi_color': aqi_color,
		'humidity': iaqi['h']['v'],
		'no2': iaqi['no2']['v'],
		'o3': iaqi['o3']['v'],
		'pm10': iaqi['pm10']['v'],
		'pm25': iaqi['pm25']['v'],
		'so2': iaqi['so2']['v'],
		'temperature': iaqi['t']['v'],
	}
	
	# Join both dictionaries
	context.update(forecast)

	return render(request, 'home.html', context)


def about(request):
	return render(request, 'about.html', {})
