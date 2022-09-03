# InkyDash
A WFH-oriented eInk dashboard for your Raspberry Pi. I wanted a low-power way for my wife to quickly check if I'm currently in a meeting, so I hacked this together.

## Preview
![free](https://user-images.githubusercontent.com/22794371/188255893-9b05c94a-6bd3-4ccb-8c20-d672e9773510.jpeg)

## Requirements
### Hardware
- Raspberry Pi with a browser installed (tested on a 4B+ model running the graphical Raspbian environment)
- [inky screen](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371)
- keyboard + mouse + Pi-compatible HDMI screen for initial setup
### Software
#### Raspberry Pi settings
- GPIO enabled
- SPI enabled
#### raspbian packages
- python3
- python3-pip
- fonts-noto-ui-core
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

Once this completes, the script should be ready to get your calendar data without needing to re-complete the flow. 

Next get an API secret key from [Openweathermap](https://openweathermap.org). 

Add a .env file and set the following values:
```
OPENWEATHERMAP_WEATHER_API_SECRET=
TIMEZONE=
```

You can then run `./inkydash.py` as a test to see it draw to your Inky screen.

Finally add a cron job to refresh the screen every 4 minutes:
```
crontab -e
# At end of file, add:
*/4 * * * * /path/to/inkydash.py > /tmp/inkydash.log
```

## Feature Roadmap

Done:
- Google Calendar Free/Busy
- Weather

Planned:
- Client/server architecture
- Decouple screen refresh from API calls
- Cache API results
- Module system
- Personalization options

## FAQ
### I'm having trouble completing the Oauth flow from the Raspberry Pi/don't want the Raspbian graphical environment/don't have a display to spare for initial setup
You can complete the Oauth flow from your PC by cloning this repo on it and running `./inkydash`, then copying over `~/.credentials/inkydash.json` and `./inkydash.apps.googleusercontent.com.json` to your Raspberry Pi using `scp`.
