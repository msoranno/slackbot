import ssl as ssl_lib
import certifi
import os
from slack import RTMClient
import feedparser
import datetime
import requests, json
from flask import Flask, request, Response, jsonify, json


def printMsg(txt):
  datetime_object = datetime.datetime.now()
  print('['+str(datetime_object)+'] - ' + txt )

def help(channel_id,user,web_client):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>! , veo que necesitas ayuda. Este es un listado de las cosas que puedes hacer llamandome:")
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text": "*fstbot* tri noticias"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*fstbot* quien es juanjo ?"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*fstbot* horario gym"}}
      ])

def quienesjuano(channel_id,user,web_client,thread_ts):
    web_client.chat_postMessage(
      channel=channel_id,
      thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text": "Madre mia ... El Juanjo, menudo pajaro!!!"},
                "accessory": {
                    "type": "image",
                    "image_url": "https://drive.google.com/uc?id=1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO",
                    "alt_text": "desde colombia para el mundo papa"
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn","text": "de Colombia para el mundo papa...*juepuuuuu*"}
            }
      ]    
    )

def horariosFitness(channel_id,user,web_client,thread_ts):
    web_client.chat_postMessage(
      channel=channel_id,
      thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text": "<http://fitnessports.eu/wp-content/uploads/pdf/Horarios%20Fitness%20Sports%20actualizado.pdf|presione aqui>"}
            }
      ]    
    )

def triNews(ssl_context,channel_id,user,web_client,thread_ts):
    # https://www.triathlon.org/feeds/news
    url = 'http://feeds.feedburner.com/TriatlonNoticias?format=xml'
    ssl_lib._create_default_https_context=ssl_lib._create_unverified_context
    feed = feedparser.parse(url)
    for post in feed.entries:
        title = str(post.title)
        #description = str(post.description)
        link_url = str(post.link)
        web_client.chat_postMessage(
          channel=channel_id,
          thread_ts=thread_ts,
          blocks = [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": title}
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": link_url}
                }

          ]    
        )


def salidaBici(channel_id,user,web_client,thread_ts):
      web_client.views_open(
          trigger_id="123maraco.maraco",
          view = {
            "type": "modal",
            "callback_id": "modal-identifier",
            "title": {
              "type": "plain_text",
              "text": "Just a modal"
            },
            "blocks": [
              {
                "type": "section",
                "block_id": "section-identifier",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Welcome* to ~my~ Block Kit _modal_!"
                },
                "accessory": {
                  "type": "button",
                  "text": {
                    "type": "plain_text",
                    "text": "Just a button"
                  },
                  "action_id": "button-identifier"
                }
              }
            ]
          }
    )
    # web_client.chat_postMessage(
    #   channel=channel_id,
    #   thread_ts=thread_ts,
    #   blocks = 
    # )


@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    print(data)
    print('---------------------------------------------------------------------------------')
    thread_ts = str(data.get('ts'))
    # if 'fstbot' in str(data.get('text')).lower():
    #     channel_id = str(data.get('channel'))
    #     thread_ts = str(data.get('ts'))
    #     user = str(data.get('user'))
        
    #     userObject = {'token': slack_token, 'user': user}
    #     r = requests.get('https://slack.com/api/users.info', params=userObject)
    #     print(r.json())

    #     printMsg('user ' + user + ' has requested ' + '" ' + str(data.get('text')).lower() + ' "')
    #     if 'fstbot' in str(data.get('text')).lower() and 'quien es juanjo' in str(data.get('text')):
    #         quienesjuano(channel_id,user,web_client,thread_ts)
    #     elif 'fstbot' in str(data.get('text')).lower() and 'tri noticias' in str(data.get('text')):
    #         triNews(ssl_context,channel_id,user,web_client,thread_ts)
    #     elif 'fstbot' in str(data.get('text')).lower() and 'horario gym' in str(data.get('text')):
    #         horariosFitness(channel_id,user,web_client,thread_ts)
    #     elif 'fstbot' in str(data.get('text')).lower() and 'salida bici' in str(data.get('text')):
    #         salidaBici(channel_id,user,web_client,thread_ts)
    #     else:
    #         help(channel_id,user,web_client)


# Main
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(
  token=slack_token,
  connect_method='rtm.start',
  ssl=ssl_context
)
printMsg('start..')
rtm_client.start()


