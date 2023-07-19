from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta, timezone
from weather import get_weather, fig2img
import os
import pytz

# Define constants
API_KEY = os.environ.get('WEATHER_API')
WIDTH, HEIGHT = 800, 480
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 20
FONT_SIZE_SMALL = 16
FONT_SIZE_BIG = 32
NAME = os.environ.get('USER')

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    import config as cfg
else:
    import configenv as cfg

# Get the current time
eastern = pytz.timezone('US/Eastern')
current_time = datetime.now().astimezone(eastern)

# Create a new image with a white background
pic = Image.new('RGB', (WIDTH, HEIGHT), 'white')
draw = ImageDraw.Draw(pic)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_small = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)
font_big = ImageFont.truetype(FONT_PATH, FONT_SIZE_BIG)

# Create header text
header_text = f"Hello, {NAME}"
if current_time.hour < 12:
    header_text = f"Good morning, {NAME}"
elif 12 <= current_time.hour < 17:
    header_text = f"Good afternoon, {NAME}"
elif 17 <= current_time.hour:
    header_text = f"Good evening, {NAME}"

draw.text((20, 20), header_text, fill='black', font=font_big)

# for i, item in enumerate(data['list'][:24]):  # get data for 24 hours 
#     time = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
#     time_format = time.strftime("%A, %B %d - %I:%M %p")
#     # Draw the time
#     draw.text((20, 20 + i*20), time_format, fill='black', font=font)

#     # Draw the temperature
#     draw.text((400, 20 + i*20), str(int(item['main']['temp'])) + '°F', fill='black', font=font)

#     # Draw the icon
#     icon_response = requests.get(f'http://openweathermap.org/img/w/{item["weather"][0]["icon"]}.png')
#     icon_img = Image.open(BytesIO(icon_response.content))
#     img.paste(icon_img, (600, 20 + i*20))

fig = get_weather(cfg.OPENWEATHERMAP_API_KEY)

fig = fig2img(fig)

pic.paste(fig, (-25, 260))

# Save the image
pic.save('weather_forecast.png')

