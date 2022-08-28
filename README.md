# InkyDash

A WFH-oriented eInk dashboard for your Raspberry Pi.

## Requirements
### Hardware
- Raspberry Pi with a browser installed (tested on a 4B+ model running the graphical Raspbian environment)
- [inky screen](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371)
- keyboard + mouse + Pi-compatible HDMI screen for initial setup
### Software
Raspberry Pi settings:
- GPIO enabled
- SPI enabled

Python3 + python3-pil + python3-pip
## Initial Setup
First [create a project](https://developers.google.com/workspace/guides/create-project) and [create desktop application credentials](https://developers.google.com/workspace/guides/create-credentials) through the Google console.
Save the credentials Oauth JSON file in the same directory. Its name should match `CLIENT_SECRET_FILE` in inkydash.py; default is `inkydash.apps.googleusercontent.com.json`.

Make sure that either you have a working VNC connection, or that input devices and an HDMI monitor are connected to the Pi, as you need to interact with a Web browser to complete the one-time Oauth flow.

On the Pi, run these commands in the directory you cloned this repo:
```
pip install -r requirements.txt
./inkydash.py
```
Click the link in terminal to authenticate the Google account you want to give calendar access to.

Once this completes, the script should be ready to get your calendar data without needing to re-complete the flow. You can rerun `./inkydash.py` to confirm. At this point you should also be able to see it draw to your Inky screen.

Add a cron job to refresh the screen every 4 minutes:
```
crontab -e
# At end of file, add:
*/4 * * * * /path/to/inkydash.py > /tmp/inkydash.log
```

## Feature Roadmap

Done:
- Google Calendar Free/Busy

In Progress:
- Weather

Planned:
- N/a
