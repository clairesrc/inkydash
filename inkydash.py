#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from requests import get

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
    # create an image
    out = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))

    # font
    font_big = ImageFont.truetype(FONT_FILENAME, 90)
    height_big = 130
    font_medium = ImageFont.truetype(FONT_FILENAME, 48)
    height_medium = 100
    font_small = ImageFont.truetype(FONT_FILENAME, 24)
    height_small = 60

    # get a drawing context
    d = ImageDraw.Draw(out)

    cursor = 0
    for widget in state:
        if widget["size"] == "large":
            height = height_big
            font = font_big
        if widget["size"] == "medium":
            height = height_medium
            font = font_medium
        if widget["size"] == "small":
            height = height_small
            font = font_small

        # label
        d.multiline_text(
            (10, cursor), widget["label"], font=font_small, fill=(200, 200, 200)
        )

        # data
        d.multiline_text(
            (5, cursor + 15), widget["data"], font=font, fill=(255, 255, 255)
        )
        cursor = cursor + height

    # save image
    out.save(IMAGE_FILENAME, "PNG")


def main():
    hostname = os.getenv("INKYDASH_SERVER_LOCATION")
    if hostname is None:
        hostname = "localhost:8080"
    draw_image(get(f"http://{hostname}/data").json())
    send_to_screen()


if __name__ == "__main__":
    main()
