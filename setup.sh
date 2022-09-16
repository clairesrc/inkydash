#!/bin/sh

GCAL_CREDS_FILENAME="inkydash.apps.googleusercontent.com.json"

BASEDIR=$(dirname "$0")
CONFIG_DIR="$BASEDIR/config"

printf "InkyDash setup tool\n\n"

git clone https://github.com/clairesrc/inkydash && cd inkydash

if [ -z "$TZ" ]; then
    TZ=$(find /usr/share/zoneinfo -type f -exec cmp -s /etc/localtime '{}' \; -print | sed -e 's|^\./||' -e '/posix/d' | head -n 1 | sed 's/\/usr\/share\/zoneinfo\///')
fi

printf "Timezone set to $TZ\n\n"

read -p "Choose theme: light or default [default]" THEME

if [ -z $THEME ]; then
    THEME="default"
fi
printf "Theme set to $THEME\n\n"

ENV_CONTENTS="TZ=$TZ\nINKYDASH_THEME=$THEME" > "$BASEDIR/.env"

if [ -e "$BASEDIR/credentials/inkydash.json" ]; then
    echo "Found $BASEDIR/credentials/inkydash.json, skipping Google Calendar setup. Delete this file if you need to reset."
else
    printf "\n\nCreate a Google Developer project: https://developers.google.com/workspace/guides/create-project"
    echo "Then, create credentials for a DESKTOP application: https://developers.google.com/workspace/guides/create-credentials"
    read -p "When finished, paste credentials Oauth JSON here:" GCAL_CREDS

    if [ -z $GCAL_CREDS ]; then
        echo "Error: empty Google Calendar credentials"
        exit 0
    fi
    echo $GCAL_CREDS > "$CONFIG_DIR/$GCAL_CREDS_FILENAME"
    echo "Google Calendar credentials saved to $CONFIG_DIR/$GCAL_CREDS_FILENAME"
    python3 "$BASEDIR/setup.py"
    cp ./credentials/inkydash.json "$BASEDIR/credentials/inkydash.json" 2> /dev/null
    echo "Google Calendar credentials set up successfully."
fi

printf "\nCreate an OpenWeatherMap project: https://openweathermap.org/\n"
read -p "Paste API secret key here:" OPENWEATHERMAP_CREDS
if [ -z $OPENWEATHERMAP_CREDS ]; then
    echo "Error: empty OpenWeatherMap API secret"
    exit 0
fi


printf "$ENV_CONTENTS\nOPENWEATHERMAP_WEATHER_API_SECRET=$OPENWEATHERMAP_CREDS" > $BASEDIR/.env

printf "\nSaved $BASEDIR/.env\n"

printf "\nPreparing to deploy to Raspberry Pi: make sure your Raspberry Pi is online and has SSH enabled!\n"

read -p "Raspberry Pi IP:" PI_IP
if [ -z $PI_IP ]; then
    echo "Error: empty Raspberry Pi IP"
    exit 0
fi
printf "\n"
read -p "Raspberry Pi username: [pi]" PI_USERNAME
if [ -z $PI_IP ]; then
    PI_IP="pi"
fi

scp -r ./* $PI_USERNAME@$PI_IP:~/inkydash

printf "\n\nDeployed to $PI_IP successfully, running docker-compose"
ssh $PI_USERNAME@$PI_IP -c "cd ~/inkydash && docker-compose up -d"

printf "\n\nAll done!"