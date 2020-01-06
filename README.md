# slackbot

## Desarrollo
### Current status (mipiri - dev)

- Al parecer para poder crear un formulario en plan modal, hay que tener datos como el trigger_id que se obtienen agregando un "event action" los event actions necesitan de una url para hacer call_back. El event action se puede ver desde el menu de slack.

- Hemos creado un script en flask que pueda recibir esa info de slack (receive.py).

- La idea ahora es ver como con esa información mandar el mensaje modal a slack para obtener las respuestas adecuadas.

- Probablemente el fstbot quedará aparte de lo que será la propuesta de salidas en bici.

### La ejecución en local

````
python receive.py
````

## Prod
### Requirements

- Python 3.7
- pip libraries

```
pip install slackclient
pip install certifi
pip install feedparser
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