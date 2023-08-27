from datetime import datetime
from PIL import Image
import os

def xkcd(path):
    # The datetime for August 27, 2023, 2:00 PM
    start_time = datetime(2023, 8, 27, 13, 0)

    # The current datetime
    current_time = datetime.now()

    # Calculate the difference
    time_difference = current_time - start_time

    # Convert the difference to hours
    hours_passed = int(time_difference.total_seconds() / 3600)  # Convert seconds to hours

    if hours_passed > 3099:
        hours_passed = hours_passed - 3099 * int(hours_passed / 3099)

    # load file
    time_name = f'time/time{hours_passed}.jpg'
    filename = os.path.join(path, time_name)

    time_image = Image.open(filename)
    img = time_image.crop((123, 0, 676,480))

    return img

