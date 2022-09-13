[![ci](https://github.com/clairesrc/inkydash/actions/workflows/build.yml/badge.svg)](https://github.com/clairesrc/inkydash/actions/workflows/build.yml)
# InkyDash
A WFH-oriented eInk dashboard for your Raspberry Pi. I wanted a low-power way for my wife to quickly check if I'm currently in a meeting, so I hacked this together.

InkyDash should start when the Raspberry Pi boots. You can alter the contents of `config/inkydash.toml` to personalize your dashboard, disable or reorder widgets, etc.

This repository contains the backend API code and everything an end-user needs to set up InkyDash on their Pi. For the Inky HAT frontend's source code, see [clairesrc/inkydash-frontend](https://github.com/clairesrc/inkydash-frontend).

## Preview

![image0](https://user-images.githubusercontent.com/22794371/189393215-f9f5f492-9d88-431c-9473-89ad479f4bf0.jpeg)

## Requirements
### Hardware
- Raspberry Pi: tested on a 4B+ model running Raspbian.
- [Inky screen](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371): I used the Impression variant, but any of them should work.
### Software
#### Raspberry Pi settings
- GPIO enabled

## Initial Setup
### On your PC
First [create a project](https://developers.google.com/workspace/guides/create-project) and [create desktop application credentials](https://developers.google.com/workspace/guides/create-credentials) through the Google console.
Save the credentials Oauth JSON file as `./config/inkydash.apps.googleusercontent.com.json`.

Clone this repository:
```
$ git clone https://github.com/clairesrc/inkydash
```

`cd` into this repository, then complete the Oauth flow from your PC by running:
```
$ pip install -r requirements.txt
$ ./setup.py
```

Click the link in terminal to authenticate the Google account you want to give calendar access to. Once this completes, InkyDash should be ready to get your calendar data without needing to re-complete the flow. 

Next get an API secret key from [Openweathermap](https://openweathermap.org). 

Create an `.env` file and set the following values:
```
OPENWEATHERMAP_WEATHER_API_SECRET=
TZ=America/Chicago
```

Copy the entire directory to your Raspberry Pi over SSH using `scp`:
```
$ scp -rv inkydash pi@raspberrypi:~/inkydash
```



### On your Raspberry Pi
If you don't have `docker-compose` set up, run these on your Raspberry Pi.
```
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo apt install -y docker-compose
$ sudo sh get-docker.sh
$ sudo usermod -aG docker $USER
$ sudo systemctl start docker
$ sudo systemctl enable docker
## Then log out of your SSH session or reboot your Raspberry Pi to refresh your user group. 
```

`cd` to the directory you just copied over from your PC, then run:
```
$ docker-compose up -d
```


## Writing modules
Add your module file to `modules/` and it will be auto-loaded at startup. Remember to also add it to the `modules` array in `config/inkydash.toml`.

All modules should define `MODULE_NAME`, `REFRESH_INTERVAL`, `LABEL`, `SIZE` and `PARAMS` at the top level of the file, and the module class should be named `module` so that it can be properly imported.

| Variable name        | Variable description                                                                  |
|----------------------|---------------------------------------------------------------------------------------|
| **MODULE_NAME**      | Module filename e.g. `freebusy`                                                       |
| **REFRESH_INTERVAL** | Module state update frequency in minutes                                              |
| **LABEL**            | Module widget label for display on frontend e.g. `MEETING STATUS`                     |
| **SIZE**             | Module font size for display on frontend e.g. `large`, `medium`, `small`              |
| **PARAMS**           | List of environment variables to pass down to module e.g. `["GOOGLE_TOKEN_FILENAME"]` |

Module "Hello world" boilerplate:
```python
from inkymodule import InkyModule

MODULE_NAME = "hello"
REFRESH_INTERVAL = 1
LABEL = "HELLO WORLD"
SIZE = "large"
PARAMS = []

class module(InkyModule):
    def _hydrate(self):
        return "Hello, world!"
```

Any initial setup can be added to the end of `__init__()` after calling `self._setup()`. This method gets run once, when InkyDash first starts up.

`_hydrate()` is run at the interval set in `REFRESH_INTERVAL` to set the data that will be passed down to the frontend. When the module is rendered in between intervals, the previous value is loaded from memory. The data type returned must be a number or a string. 

Module parameters (the `PARAMS` list) are for passing down individual environment variables to the module. Use `self._get_params()["PARAM_NAME"]` to access the value in your module code. 

You can specify a `_setup()` method that will be run once, on app initialization. Also, an optional `DEFAULT_CONFIG` dictionary can specify default config values in the form `{"key": "default_value"}`, to render them optional in the `inkydash.toml` config file.

## Feature roadmap
Planned:
- More customization options
- Expanded module options with multi-column widgets
- Non-blocking external API updates
- Faster frontend Docker image builds
