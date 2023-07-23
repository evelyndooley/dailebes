from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta, timezone
from weather import get_weather, fig2img
from epd import display_image
from rss import print_top_headlines
import os
import pytz

# Define constants
WIDTH, HEIGHT = 800, 480
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_PATH_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 20
FONT_SIZE_SMALL = 16
FONT_SIZE_BIG = 32

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
font_big = ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_BIG)

# Create header text
header_text = f"Hello, {cfg.NAME}"
if current_time.hour < 12:
    header_text = f"Good morning, {cfg.NAME}"
elif 12 <= current_time.hour < 17:
    header_text = f"Good afternoon, {cfg.NAME}"
elif 17 <= current_time.hour:
    header_text = f"Good evening, {cfg.NAME}"

draw.text((20, 20), header_text, fill='black', font=font_big)

# Create RSS feed
feed = print_top_headlines(cfg.RSS_URL, 8)
for i, item in enumerate(feed):  # get data for 24 hours 
    draw.text((20, 60 + i*20), item.title, fill='black', font=font_small)

# Draw weather
fig = get_weather(cfg.OPENWEATHERMAP_API_KEY, 12, 4)
fig = fig2img(fig)
pic.paste(fig, (-25, 200))

# Save the image
pic.save('weather_forecast.png')

# Render to EPD
display_image(pic)

