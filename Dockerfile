FROM python:3.10-alpine
# FROM woahbase/alpine-rpigpio:aarch64

ENV OPENWEATHERMAP_WEATHER_API_SECRET ""
ENV TIMEZONE "America/Chicago"

RUN apk add build-base linux-headers font-noto zlib-dev libjpeg-turbo-dev
RUN pip install --upgrade pip

RUN mkdir /inkydash
WORKDIR /inkydash

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /inkydash/config
RUN mkdir /inkydash/cache
RUN mkdir -p /root/credentials

ADD app.py .

VOLUME ["/root/.credentials", "/inkydash/config", "/inkydash/cache"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
