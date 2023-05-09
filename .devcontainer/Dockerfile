FROM python:3.9-bullseye

# disable interactive ui
ENV DEBIAN_FRONTEND=noninteractive

# install dependencies from package manager
RUN apt update && apt install -y \
    sudo \
    git \
    curl wget \
    firefox-esr

# create 'dev' user, add it to sudo group and set password
RUN mkdir /home/dev
RUN useradd dev && chown -R dev /home/dev
RUN adduser dev sudo
RUN echo "dev:dev"|chpasswd 

USER dev
RUN cd /tmp \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz \
    && tar -xvf geckodriver-v0.31.0-linux64.tar.gz