FROM ubuntu:16.04

MAINTAINER Janis Lesinskis

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


RUN apt-get update -y && apt-get -y install \
	python3-pip \
	ffmpeg \
	sox \
	git \
	nginx \
	supervisor


# -- Install uWSGI and pipenv
RUN pip3 install uwsgi
RUN pip3 install pipenv

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
# -- Install dependencies:
RUN pipenv install --deploy --system

# -- Install Application into container:
RUN mkdir /app
WORKDIR /app

# -- Set up configuration files
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY . /app

# -- Create supervisor log directory
RUN mkdir -p /var/log/supervisord/

EXPOSE 8080

CMD [ "supervisord", "-c", "/etc/supervisor/conf.d/supervisor-app.conf", "-n" ]
