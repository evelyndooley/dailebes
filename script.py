import requests
from datetime import datetime, timedelta, timezone
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pytz
import os

# Define constants
API_KEY = os.environ.get('WEATHER_API')
WIDTH, HEIGHT = 800, 480
ICON_FOLDER = './icons/'
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_SIZE = 20
LOCATION = 'Boston'  # Your location
LAT = 42.3875968
LON = -71.0994968

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

# Make a request to the OpenWeatherMap API
response = requests.get(f'http://api.openweathermap.org/data/3.0/onecall?'
                        f'lat={LAT}&lon={LON}&units=imperial&appid={API_KEY}')
data = response.json()

# print(data)

# Create a new image with a white background
# img = Image.new('RGB', (WIDTH, HEIGHT), 'white')
# draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

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

# Convert the 'dt_txt' field to datetime and get the 'temp' field
times_and_temps = [(utc_to_local(datetime.utcfromtimestamp(item['dt'])), item['temp'], item['weather'][0]['icon']) for item in data['hourly']]


eastern = pytz.timezone('US/Eastern')

# Get the current time
current_time = datetime.now().astimezone(eastern)

# Filter the data to include the current time and the next 7 hours
filtered_times_and_temps = [
    item for item in times_and_temps
    if current_time - timedelta(hours=1) <= item[0] <= current_time + timedelta(hours=21)
]

current_weather = ((utc_to_local(datetime.utcfromtimestamp(data['current']['dt'])), data['current']['temp'], data['current']['weather'][0]['icon']))

print(current_weather)

filtered_times_and_temps.append(current_weather)

filtered_times_and_temps.sort()

times = [item[0] for item in filtered_times_and_temps]
temps = [item[1] for item in filtered_times_and_temps]
icons = [item[2] for item in filtered_times_and_temps]

print(current_time)
print(filtered_times_and_temps)

fig, ax = plt.subplots(figsize=(11.11, 4.86))  

# plot the data
ax.plot(times, temps, marker='o')

# Add a colored line indicating the current time
plt.axvline(current_time, color='r', linestyle='--')

# Add temperature values and weather icons as data point labels
for i, icon in enumerate(icons):
    if i % 2:
        continue
    # Add the temperature value as a label
    ax.text(times[i], temps[i], str(temps[i]))

    # Download the weather icon
    icon_url = f'http://openweathermap.org/img/w/{icon}.png'
    response = requests.get(icon_url)
    img = Image.open(BytesIO(response.content))

    # Create an image box
    imagebox = OffsetImage(img, zoom=0.5)
    ab = AnnotationBbox(imagebox, (mdates.date2num(times[i]), temps[i]))

    # Add the weather icon to the plot
    ax.add_artist(ab)

# Format x-axis to show time
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Temperature (F)')
plt.title('Temperature Forecast Throughout the Day')

# Save the figure as an image
plt.savefig('weather_forecast.png', dpi=72)  # 72 dpi is the default dpi for most displays

# Save the image
# img.save('weather.png')

