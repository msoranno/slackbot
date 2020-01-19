# slackbot

## raspi setup

- install pyenv

´´´´
 sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

curl https://pyenv.run | bash

vi  ~/.bashrc (add this to the end)
export PATH="/home/pi/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
´´´´

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

./ngrok http 5000
````

## Desarrollo
### Current status (mipiri - dev)

- Cambiar icono del bot

- Preparar la raspi para poder meter todo alli.

### La ejecución en local

````
python slackcmd.py
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
```
2. Run the program

``` 
python fstbot.py
```

3. Run as a service (optional)

```
sudo cp fstbot.service /etc/systemd/system/
```
