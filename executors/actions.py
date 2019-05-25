from services.weather import WeatherService
from datetime import datetime
import config

class ActionExecutor:

    def __init__(self):
        self.weather = WeatherService()

    def executeAction(self, action, params):
        if action == 'GetWeather':
            location = params['location']
            date = params['date']
            dt = datetime.strptime(date, '%Y-%m-%d')
            forecasts = self.weather.getForecastsByCity(location)
            data = None
            for forecast in forecasts:
                if forecast.date == dt:
                    data = {
                        'location': location,
                        'date': date,
                        'text': config.WEATHER_CONSTANTS[str(forecast.code)]
                    }
            return data


