#FROM registry.cafebazaar.ir:5000/common-images/ubuntu:trusty-py2-django
FROM ubuntu:14.04
MAINTAINER Sahel Sarcheshmehpour <sarcheshmehpours@gmail.com>
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y python
RUN apt-get install -y python-dev
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip

RUN pip install Django==1.8.11
RUN pip install gunicorn==19.3.0
RUN pip install Jinja2==2.8
RUN pip install python-daemon==2.1.0
RUN pip install mock==1.3.0
RUN pip install ipython==5.4.1


# Get Gunicorn port as ARG
ARG gunicorn_port

# Add files
ADD . /opt/dbproject

# Expose port
EXPOSE $gunicorn_port
#EXPOSE 54333

# Switch to project dir
WORKDIR /opt/dbproject

# Add CMD
CMD python anbardari_service.py start

# Install pip dependencies
RUN pip install -r requirements-prod.txt

# Make scripts executable & Create Gunicorn dir
RUN \
    chmod +x manage.py && \
    chmod +x anbardari_service.py && \
    mkdir -p /etc/gunicorn
