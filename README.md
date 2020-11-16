# slackbot

## raspi setup.

- install pyenv

```
 sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

curl https://pyenv.run | bash

vi  ~/.bashrc (add this to the end)
export PATH="/home/pi/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

```

- pyenv setup

````
pyenv install 3.7.4
pyenv virtualenv 3.7.4 slackcmd
pyenv local slackcmd
````

- cloning repo

````
git clone git@github.com:msoranno/slackbot.git
````

- install and run ngrok

````
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-amd64.zip
./ngrok authtoken 1UhGdCtYYrP5P....

./ngrok http -region eu 5000
````

Ngrok en su version free soporta 1 proceso en cada region, hay 4 regiones en total: us,eu,ap,au


## Desarrollo
### Current status (mipiri - dev)

- Pendiente:
   - arreglar el tema de las 5 horas
   - lo mismo hay que subir el voy a no voy sobre la foto.
   - tratar de meter la el día que es en la fecha. ej: domingo 26-01-20

### La ejecución en local

````
python ./slackcmd/slackcmd.py
````

## Prod
### Requirements

- Python 3.7 (pyenv)
- pip libraries

```
pip install --upgrade pip
pip install slackclient
pip install certifi
pip install feedparser
pip install requests 
pip install flask

```

### How to run it ?

1. Export the variable token

``` 
export SLACK_API_TOKEN="xoxb-861708542357-..."
export SLACK_BIKE_CHANNEL_ID=
export SLACK_BIKE_CHANNEL_NAME=salidas-bici
export SLACK_RUN_CHANNEL_ID=
export SLACK_RUN_CHANNEL_NAME=tapias
export SLACK_GENERAL_CHANNEL_ID=
export SLACK_GENERAL_CHANNEL_NAME=general
```
2. Run the program

``` 
python ./slackcmd/slackcmd.py
```


