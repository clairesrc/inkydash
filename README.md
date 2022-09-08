# InkyDash
A WFH-oriented eInk dashboard for your Raspberry Pi. I wanted a low-power way for my wife to quickly check if I'm currently in a meeting, so I hacked this together.

## Preview
![free](https://user-images.githubusercontent.com/22794371/188255893-9b05c94a-6bd3-4ccb-8c20-d672e9773510.jpeg)

## Requirements
### Hardware
- Raspberry Pi: tested on a 4B+ model running Raspbian.
- [Inky screen](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371): I used the Impression variant, but any of them should work.
### Software
#### Raspberry Pi settings
- GPIO enabled
- SPI enabled
#### raspbian packages
- python3
- python3-pip
- fonts-noto-ui-core
- wget
## Initial Setup
First [create a project](https://developers.google.com/workspace/guides/create-project) and [create desktop application credentials](https://developers.google.com/workspace/guides/create-credentials) through the Google console.
Save the credentials Oauth JSON file as `./inkydash-config/inkydash.apps.googleusercontent.com.json`.

CLone this repo onto both your Raspberry Pi and your PC. You will need to run a setup script from your PC and copy over its output to the Raspberry Pi.

Complete the Oauth flow from your PC by running:
```
$ pip install -r server_requirements.txt
$ ./setup.py
```

Click the link in terminal to authenticate the Google account you want to give calendar access to. Once this completes, InkyDash should be ready to get your calendar data without needing to re-complete the flow. 

Copy over `./inkydash-credentials/inkydash.json` and `./inkydash-config/inkydash.apps.googleusercontent.com.json` to your Raspberry Pi over SSH using `scp`.

Next get an API secret key from [Openweathermap](https://openweathermap.org). 

Adjust the values under `environment` in `docker-compose.yml` to pass down your weather API key and timezone, or define them in an `.env` file so they persist across git pulls.

If you don't have `docker-compose` set up, run these on your Raspberry Pi.
```
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo apt install -y docker-compose
$ sudo sh get-docker.sh
$ sudo usermod -aG docker $USER
$ sudo systemctl start docker
$ sudo systemctl enable docker

# Log out of your SSH session or reboot your Raspberry Pi to refresh your user group

$ docker-compose up -d
```

Install requirements for the clientside script on the Raspberry Pi:
```
$ pip install -r client_requirements.txt
```

At this you should be able to manually run `./inkydash.py` on the Pi to fetch data and draw it to the screen.

Finally add a cron job to re-draw the screen every minute:
```
$ crontab -e
# At end of file, add:
*/1 * * * * /path/to/inkydash.py > /tmp/inkydash-client.log
```

## Feature Roadmap

Done:
- Google Calendar Free/Busy
- Weather
- Time
- Client/server architecture
- Decouple screen refresh from API calls
- Module system

Planned:
- Personalization options
- Improved initial setup experience
