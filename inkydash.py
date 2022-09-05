#!/usr/bin/env python3
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from requests import get
from dotenv import load_dotenv

load_dotenv(sys.argv[1])


IMAGE_FILENAME = "/tmp/inkydash.png"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 488
FONT_FILENAME = "Pillow/Tests/fonts/NotoSansMono-Regular.ttf"


def send_to_screen():
    """Sends image file to Inky screen.
    Sets up Inky API, opens given filename, and draws image.
    """
    # setup
    inky = auto(ask_user=True, verbose=True)
    saturation = 0.5

    # open source image
    image = Image.open(IMAGE_FILENAME)
    resizedimage = image.resize(inky.resolution)

    # draw image
    inky.set_image(resizedimage, saturation=saturation)
    inky.show()


def draw_image(state):
    """Create PNG image from dashboard state."""
    freebusy = state["freebusy"]["status"]

    if state["weather"]:
        weather_feels_like_temp = state["weather"]["main"]["feels_like"]
        weather_status = state["weather"]["weather"][0]["main"]

    if state["time"]:
        current_time = state["time"]

    # create an image
    out = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))

    # font
    font_big = ImageFont.truetype(FONT_FILENAME, 90)
    font_medium = ImageFont.truetype(FONT_FILENAME, 48)
    font_small = ImageFont.truetype(FONT_FILENAME, 24)

    # get a drawing context
    d = ImageDraw.Draw(out)

    # draw labels
    d.multiline_text((10, 0), "MEETING STATUS", font=font_small, fill=(200, 200, 200))
    d.multiline_text((10, 130), "WEATHER", font=font_small, fill=(200, 200, 200))
    d.multiline_text((10, 230), "TIME", font=font_small, fill=(200, 200, 200))

    # draw freebusy
    d.multiline_text((5, 10), f"{freebusy}", font=font_big, fill=(255, 255, 255))

    if state["weather"]:
        # draw weather
        d.multiline_text(
            (5, 155),
            f"{weather_feels_like_temp}°F | {weather_status}",
            font=font_medium,
            fill=(255, 255, 255),
        )

    if state["time"]:
        # draw time
        d.multiline_text(
            (5, 255),
            f"{current_time}",
            font=font_medium,
            fill=(255, 255, 255),
        )

    # save image
    out.save(IMAGE_FILENAME, "PNG")


def main():
    hostname = os.getenv("INKYDASH_SERVER_LOCATION")
    draw_image(get(f"http://{hostname}/").json()["data"])
    send_to_screen()


if __name__ == "__main__":
    main()
