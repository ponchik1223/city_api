FROM python:3.11

RUN mkdir /cities_app

WORKDIR /cities_app

ADD . /cities_app

RUN pip install -v /cities_app

RUN chmod a+x docker/*.sh

CMD /cities_app/docker/app.sh