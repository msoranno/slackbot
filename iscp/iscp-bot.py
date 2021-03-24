import os
import feedparser
import slack
import certifi
import requests
import threading
from flask import Flask, request, Response, jsonify, json, make_response
import ssl as ssl_lib
from random import randrange
from datetime import date, timedelta, datetime
import calendar

app = Flask(__name__)

@app.route('/slackresp', methods=['POST'])
def outbound():
    # --
	# From here we will receive the submit response from the modal form
	# also we will receive every user iteractions in case we want to treat them.
	#
	# On slack: this is confiures under "interactive components"
    # --

	# -- Print the entire form
	#print("------------------raw resp-----------------")
	#print(request.form)
	# --
	message_action = json.loads(request.form["payload"])
	message_type = message_action["type"]

	#--
	# - view_submission payloads are received when a modal is submitted.
	# - block_actions payloads  are received when a user clicks a Block Kit interactive 
	# --
	if message_type == "view_submission":
		#print("------------------view_submission-----------------")
		#print(message_action)
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		triggerID =  message_action["trigger_id"]
		dg_selected_value = message_action["view"]["state"]["values"]["input000"]["action000"]["selected_option"]["value"]
		dg_selected_text = message_action["view"]["state"]["values"]["input000"]["action000"]["selected_option"]["text"]["text"] 
		print(userID,userName,triggerID,dg_selected_value,dg_selected_text)

		
	if message_type == "block_actions":
		#print("------------------block_actions-----------------")
		#print(message_action)
		actionID = message_action["actions"][0]["action_id"]
		blockID = message_action["actions"][0]["block_id"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		print(actionID,blockID,userID,userName)

	
	# Making empty responses to make slack api happy
	return make_response("", 200)

@app.route('/slackcmd', methods=['POST'])
def inbound():
	# -- Print the entire form
	#print("------------------raw-----------------")
	#print(request.form)
	# --
    
	slack_request = request.form
	trigger_id = slack_request["trigger_id"]
	callback_id = slack_request["response_url"]
	text = str(slack_request["text"]).lower()
	channel_id = slack_request["channel_id"]
	user_id = slack_request["user_id"]
	user_name =slack_request["user_name"]
	
	
	#print("-----------------------------------------------------------------")
	print(trigger_id, callback_id, text, channel_id, user_id,user_name)
	canhelp = 0
	if text.lower() == "help" or text == "ayuda":
		canhelp = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=help,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if text.lower() == "get-vault-token":
		canhelp = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=ask_for_dg,args=(trigger_id,callback_id,client))
		x.start()		
		return txtWait

	
	#------
	# sorry we can not help
	#------
	if canhelp == 0 :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=cantHelp,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait


#------------------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------------------------------------------------------------

def ask_for_dg(trigger_id,callback_id,client,vaultToken = "None"):
	
	open_dialog = client.views_open(
				trigger_id = trigger_id,
				view={
					"type": "modal",
					"callback_id": callback_id,
					"title": {"type": "plain_text",	"text": "Token vault request"},
					"submit": {"type": "plain_text","text": "Submit"},
					"blocks": [
						{
							"type": "section",
							"block_id": "input000",
							"text": {"type": "mrkdwn","text": "Select delivery group"},
							"accessory": {
								"action_id": "action000","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Select"},
									"options": [
										{"text": {"type": "plain_text","text": "mad01"},"value": "dg-0"},
										{"text": {"type": "plain_text","text": "mad02"},"value": "dg-1"},
										{"text": {"type": "plain_text","text": "cac01"},"value": "dg-2"},
										{"text": {"type": "plain_text","text": "tst01"},"value": "dg-3"},
										{"text": {"type": "plain_text","text": "imf01"},"value": "dg-4"}
									]
							}
						},
						{"type": "section", "text": {"type": "mrkdwn","text": ":warning: token: "+str(vaultToken)}}						

					]					
				}
			)

	# response to Slack after processing is finished
	message = {"text": txtBye}
	res = requests.post(callback_id, json=message)
	print('respuesta:',res)

def get_vault_token(trigger_id,callback_id,client):

	fakeToken = "12345"
	
	open_dialog = client.views_open(
				trigger_id = trigger_id,
				view={
					"type": "modal",
					"callback_id": callback_id,
					"title": {"type": "plain_text",	"text": "Token vault request"},
					"blocks": [
						{"type": "section", "text": {"type": "mrkdwn","text": ":warning: vault-token: "+fakeToken}}					
					]					
				}
			)

	# response to Slack after processing is finished
	message = {"text": txtBye}
	res = requests.post(callback_id, json=message)
	print('respuesta:',res)

def cantHelp(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text":f"Hello <@{user}>!  ¯\_(ツ)_/¯  sorry, can't help you with that."}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def help(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hello <@{user}>! , i can help you with this:")
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text": "*- [/iscpbot* help] view this help."}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*- [/iscpbot* get-vault-token] request a token vault"}},
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)


@app.route('/', methods=['GET'])
def test():
	return Response('It works!')

#------
#Main
#------

# Globals
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'], ssl=ssl_context)
txtWait = "please wait...."


txtBye = "request completed"
user_id = ""
callback_id = ""

#------------------
# DataHolders
#------------------


if __name__ == "__main__":
	app.run(debug=True)
