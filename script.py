import requests
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

# Define constants
API_KEY = os.environ.get('WEATHER_API')
WIDTH, HEIGHT = 800, 480
ICON_FOLDER = './icons/'
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 20
LOCATION = 'Boston'  # Your location

# Make a request to the OpenWeatherMap API
response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?'
                        f'q={LOCATION}&units=imperial&appid={API_KEY}')
data = response.json()

print(data)

# Create a new image with a white background
img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

for i, item in enumerate(data['list'][:24]):  # get data for 24 hours 
    print(item)
    time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
    time_format = '''
    '''
    # Draw the time
    draw.text((20, 20 + i*20), time_format, fill='black', font=font)

    # Draw the temperature
    draw.text((200, 20 + i*20), str(item['main']['temp']) + '°C', fill='black', font=font)

    # Draw the icon
    icon_response = requests.get(f'http://openweathermap.org/img/w/{item["weather"][0]["icon"]}.png')
    icon_img = Image.open(BytesIO(icon_response.content))
    img.paste(icon_img, (400, 20 + i*20))

# Save the image
img.save('weather.png')

