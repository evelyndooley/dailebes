from omni_epd import displayfactory

DEFAULT_DISPLAY_TYPE = "waveshare_epd.epd7in3f"

def display_image(img, display_type=DEFAULT_DISPLAY_TYPE):
    epd = displayfactory.load_display_driver(display_type)

    epd.prepare()

    epd.display(img)

    epd.close()

    return

