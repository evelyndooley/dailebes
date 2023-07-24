import requests
import os
from datetime import datetime, timedelta, timezone
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import pytz
import sys

# Constants
LOCATION = 'Boston'  # Your location
LAT = 42.3875968
LON = -71.0994968
FONT_SIZE = 20
FONT_SIZE_SMALL = 16

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
fonts = {'size': 16, 'weight': 'bold'}
fonts_big = {
    'size': 20,
    'weight': 'bold'
}
eastern = pytz.timezone('US/Eastern')

# Set the font size
plt.rc('font', **fonts_big)
plt.rc('axes', titlesize=FONT_SIZE_SMALL)
plt.rc('axes', labelsize=FONT_SIZE_SMALL)
plt.rc('legend', fontsize=FONT_SIZE)
plt.rc('xtick', labelsize=FONT_SIZE_SMALL)    # fontsize of the tick labels
plt.rc('ytick', labelsize=FONT_SIZE_SMALL)    # fontsize of the tick labels

# Local function defs
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def fig2img(fig):
    # Convert a Matplotlib figure to a PIL Image and return it
    buf = BytesIO()
    fig.savefig(buf, dpi=72, transparent=True)
    buf.seek(0)
    img = Image.open(buf)

    data = np.array(img)

    # Select all black pixels regardless of the alpha value
    mask = (data[..., :3] == [0, 0, 0]).all(axis=-1)

    # Change these pixels to white, while keeping their original alpha values
    data[mask, :3] = 255

    img = Image.fromarray(data)

    img.save('weather.png')

    return img

def get_weather(apikey, length, width):
    # Make a request to the OpenWeatherMap API
    response = requests.get(f'http://api.openweathermap.org/data/3.0/onecall?'
                            f'lat={LAT}&lon={LON}&units=imperial&appid={apikey}')
    data = response.json()

    # Convert the 'dt_txt' field to datetime and get the 'temp' field
    times_and_temps = [(utc_to_local(datetime.utcfromtimestamp(item['dt'])), item['temp'], item['weather'][0]['icon']) for item in data['hourly']]

    # Get the current time
    current_time = datetime.now().astimezone(eastern)

    # Filter the data to include the current time and the next 7 hours
    filtered_times_and_temps = [
        item for item in times_and_temps
        if current_time - timedelta(hours=1) <= item[0] <= current_time + timedelta(hours=21)
    ]

    # Add an entry for the current weather
    # current_weather = ((utc_to_local(datetime.utcfromtimestamp(data['current']['dt'])), data['current']['temp'], data['current']['weather'][0]['icon']))
    # filtered_times_and_temps.append(current_weather)
    filtered_times_and_temps.sort()

    times = [item[0] for item in filtered_times_and_temps]
    temps = [item[1] for item in filtered_times_and_temps]
    icons = [item[2] for item in filtered_times_and_temps]

    fig, ax = plt.subplots(figsize=(length, width))  

    # Add temperature values and weather icons as data point labels
    for i, icon in enumerate(icons):
        if i % 2:
            continue
        # Add the temperature value as a label
        offset_val = 1.5
        avg = sum(temps) / len(temps)
        if temps[i] >= avg: offset_val = -3

        ax.text(times[i], temps[i] + offset_val, str(int(temps[i])) + "°F", fontdict=fonts, zorder=5)

        # Add icons
        if(not os.path.exists(os.path.join(script_directory, "icon/"))): os.mkdir(os.path.join(script_directory, "icon/"))
        if(os.path.exists(os.path.join(script_directory, f"icon/{icon}.png"))):
            img = Image.open(os.path.join(script_directory, f"icon/{icon}.png"))
        else:
            # Download the weather icon
            icon_url = f'http://openweathermap.org/img/w/{icon}.png'
            response = requests.get(icon_url)
            img = Image.open(BytesIO(response.content))
            img_array = np.array(img)
            img_array[:, :, -1] = 255 * (img_array[:, :, -1] > 128)
            img = Image.fromarray(img_array)
            img.save(os.path.join(script_directory, f"icon/{icon}.png"))

        # Create an image box
        imagebox = OffsetImage(img, zoom=1)
        ab = AnnotationBbox(imagebox, (mdates.date2num(times[i]), temps[i]), frameon=False)

        # Add the weather icon to the plot
        ax.add_artist(ab)

    # plot the data
    ax.plot(times, temps, marker='o', zorder=3, color='b')

    # Add a colored line indicating the current time
    plt.axvline(current_time, color='r', linestyle='--', zorder=4)

    # Check if the data spans two days
    if max(times).date() > current_time.date():
        # Add a vertical line at midnight of the next day
        midnight_next_day = datetime(current_time.year, current_time.month, current_time.day) + timedelta(days=1)
        plt.axvline(midnight_next_day.astimezone(eastern), color='r', linestyle='--', zorder=4)
        # Add a label with the month and day
        plt.text(
            midnight_next_day.astimezone(eastern)+timedelta(minutes=10), 
            max(temps), 
            midnight_next_day.strftime("%B %d"), 
            rotation=90, 
            verticalalignment='top', 
            fontdict=fonts
        )

    # Format x-axis to show time
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p', tz="US/Eastern"))

    # Add labels and title
    plt.ylabel('Temperature (F)')
    plt.title(f"{current_time.strftime('%A, %B %d')} - {data['daily'][0]['summary']}", fontdict=fonts_big)

    return plt