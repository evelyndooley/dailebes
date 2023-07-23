from os import environ as env

NAME = env.get('USER')
OPENWEATHERMAP_API_KEY = env.get('WEATHER_API')
OPENAI_API_KEY = env.get('OPENAI_API_KEY')
RSS_URL = "http://rss.cnn.com/rss/edition.rss"
