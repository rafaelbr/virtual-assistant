from services.weather import WeatherService
from services.google_calendar import GoogleCalendarService
from datetime import datetime
import config

class ActionExecutor:

    def __init__(self):
        self.weather = WeatherService()
        self.calendar = GoogleCalendarService()

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
        if action == 'SetEvent':
            date = params['date']
            time = params['time']
            name = params['name']
            #print(date)
            #print(time)
            #print(name)
            event = self.calendar.createEvent(date, time, name)
            data = {
                'link': event['htmlLink']
            }
            return data
        if action == 'GetEvents':
            date = params['date']
            data = self.calendar.getEvents(date)
            return data

