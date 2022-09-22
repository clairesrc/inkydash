FROM python:alpine

ENV OPENWEATHERMAP_WEATHER_API_SECRET ""
ENV TZ "America/Chicago"
ENV GOOGLE_TOKEN_FILENAME "/root/.credentials/inkydash.json"
ENV GOOGLE_CLIENT_SECRET_FILENAME "/inkydash/config/inkydash.apps.googleusercontent.com.json"

RUN pip install --upgrade pip

RUN mkdir /inkydash
WORKDIR /inkydash

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /inkydash/config
RUN mkdir /inkydash/cache
RUN mkdir -p /root/.credentials

ADD credentials.py .
ADD app.py .
ADD modules/* modules/
ADD inkymodule.py .
ADD inkydash.py .

VOLUME ["/root/.credentials", "/inkydash/config", "/inkydash/cache"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
