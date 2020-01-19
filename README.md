# slackbot

## Desarrollo
### Current status (mipiri - dev)

- Cambiar icono del bot

- Preparar la raspi para poder meter todo alli.

### La ejecución en local

````
python receive.py
````

## Prod
### Requirements

- Python 3.7
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
