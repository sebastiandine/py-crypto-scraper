FROM python:3.9-bullseye

# install dependencies from package manager
RUN apt update && apt install -y \
    sudo \
    wget \
    firefox-esr

# create 'dev' user, add it to sudo group and set password
RUN mkdir /home/dev
RUN useradd dev && chown -R dev /home/dev
RUN adduser dev sudo
RUN echo "dev:dev"|chpasswd 

# create app dir and copy project to it
RUN mkdir /home/dev/app
COPY src/ /home/dev/app
RUN chown -R dev:dev /home/dev/app

USER dev

# get geckodriver
RUN cd /tmp \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz \
    && tar -xvf geckodriver-v0.31.0-linux64.tar.gz

WORKDIR /home/dev/app
RUN pip install .
CMD ["python3", "main.py"]

