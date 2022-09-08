FROM python:3.10-alpine
# FROM woahbase/alpine-rpigpio:aarch64

ENV OPENWEATHERMAP_WEATHER_API_SECRET ""
ENV TZ "America/Chicago"

RUN pip install --upgrade pip

RUN mkdir /inkydash
WORKDIR /inkydash

ADD server_requirements.txt .

RUN pip install -r server_requirements.txt

RUN mkdir /inkydash/config
RUN mkdir /inkydash/cache
RUN mkdir -p /root/credentials

ADD credentials.py .
ADD app.py .
ADD modules/* modules/
ADD inkymodule.py .

VOLUME ["/root/.credentials", "/inkydash/config", "/inkydash/cache"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
