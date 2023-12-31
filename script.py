from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta, timezone
from weather import get_weather, fig2img
from epd import display_image
from rss import print_top_headlines
from xkcd import xkcd
import os
import sys
import pytz

# Define constants
WIDTH, HEIGHT = 800, 480
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_PATH_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 20
FONT_SIZE_SMALL = 16
FONT_SIZE_BIG = 32
FONT_COLOR = 'white'
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Get app config from absolute file path
if os.path.exists(os.path.join(script_directory, "config.py")):
    import config as cfg
else:
    import configenv as cfg

# Get the current time
eastern = pytz.timezone('US/Eastern')
current_time = datetime.now().astimezone(eastern)

# Create a new image
pic = Image.new('RGB', (WIDTH, HEIGHT), 'black')
draw = ImageDraw.Draw(pic)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
font_small = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)
font_big = ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_BIG)

# Add background image
pic.paste(xkcd(script_directory), (0, 0))

# Create header text
header_text = f"Hello, {cfg.NAME}"
if current_time.hour < 12:
    header_text = f"Good morning, {cfg.NAME}"
elif 12 <= current_time.hour < 17:
    header_text = f"Good afternoon, {cfg.NAME}"
elif 17 <= current_time.hour:
    header_text = f"Good evening, {cfg.NAME}"

draw.text((20, 20), header_text, fill="black", font=font_big)

# last updated
draw.text((570, 10), f"Last updated: {current_time.strftime('%I:%M %p')}\n{current_time.strftime('%A, %B %d')}", fill=FONT_COLOR, font=font_small)

# Create RSS feed
# feed = print_top_headlines(cfg.RSS_URL, 7)
# for i, item in enumerate(feed):  # get data for 24 hours 
#     draw.text((20, 60 + i*20), item.title, fill=FONT_COLOR, font=font_small)

# Draw weather
fig = get_weather(cfg.OPENWEATHERMAP_API_KEY, 4, 6)
fig = fig2img(fig)
pic.paste(fig, (525, 75), fig)

# Save the image
pic.save(os.path.join(script_directory, 'weather_forecast.png'))

# Render to EPD
if cfg.EPD:
    display_image(pic, display_type=cfg.EPD)

