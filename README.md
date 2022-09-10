# InkyDash
A WFH-oriented eInk dashboard for your Raspberry Pi. I wanted a low-power way for my wife to quickly check if I'm currently in a meeting, so I hacked this together.

InkyDash should start when the Raspberry Pi boots. You can alter the contents of `config/inkydash.toml` to personalize your dashboard, disable or reorder widgets, etc.

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

| **MODULE_NAME**      | Module filename e.g. `freebusy`                                                       |
|----------------------|---------------------------------------------------------------------------------------|
| **REFRESH_INTERVAL** | Module state update frequency in minutes                                              |
| **LABEL**            | Module widget label for display on frontend e.g. `MEETING STATUS`                     |
| **SIZE**             | Module font size for display on frontend e.g. `large`, `medium`, `small`              |
| **PARAMS**           | List of environment variables to pass down to module e.g. `["GOOGLE_TOKEN_FILENAME"]` |

Module "Hello world" boilerplate:
```python
class module(InkyModule):
    def __init__(self, config={}):
        super().__init__(
            config,
            {
                "name": MODULE_NAME, 
                "refreshInterval": REFRESH_INTERVAL,
                "label": LABEL,
                "size": SIZE,
                "params": PARAMS
            },
        )

    def _hydrate(self):
        self._set_state("Hello, World!")
        return
```

`_hydrate()` is run at the interval set in `REFRESH_INTERVAL`. When the module is rendered in between intervals, data passed into `_set_state()` is loaded from memory.

## Feature roadmap
Planned:
- More customization options
- Expanded module options with multi-column widgets
