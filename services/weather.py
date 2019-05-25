from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
import config

class WeatherService:

    def __init__(self):
        self.weather_service = YahooWeather(APP_ID=config.YAHOO_CLIENT_ID,
                            api_key=config.YAHOO_CLIENT_KEY,
                            api_secret=config.YAHOO_CLIENT_SECRET)

    def getWeatherByCity(self, city):
        self.weather_service.get_yahoo_weather_by_city(city, Unit.celsius)
        cond = config.WEATHER_CONSTANTS[str(self.weather_service.condition.code)]
        temp = self.weather_service.condition.temperature
        return cond, temp

    def getForecastsByCity(self, city):
        self.weather_service.get_yahoo_weather_by_city(city, Unit.celsius)
        return self.weather_service.forecasts
