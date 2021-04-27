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
		callback_id = message_action["view"]["callback_id"]
		dg_selected_value = message_action["view"]["state"]["values"]["input000"]["action000"]["selected_option"]["value"]
		dg_selected_text = message_action["view"]["state"]["values"]["input000"]["action000"]["selected_option"]["text"]["text"] 
		print('view_submission:',userID,userName,triggerID,dg_selected_value,dg_selected_text,callback_id)

		x = threading.Thread(target=get_vault_token,args=(triggerID,callback_id,client,dg_selected_text))
		x.start()		

		
	if message_type == "block_actions":
		#print("------------------block_actions-----------------")
		#print(message_action)
		actionID = message_action["actions"][0]["action_id"]
		blockID = message_action["actions"][0]["block_id"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		print('block_actions:',actionID,blockID,userID,userName)
		


	
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
	#user_email = get_user_mail(user_id)
	user_email = "miguel.angel.soranno@ibm.com"
	
	
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
		x = threading.Thread(target=ask_for_dg,args=(trigger_id,callback_id,client,user_email))
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

@app.route('/', methods=['GET'])
def test():
	return Response('It works!')

#------------------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------------------------------------------------------------

def getVaultClientToken(sa_token_file_location,vault_role):

	# get the sa token
	sa_token = ""
	with open(sa_token_file_location, 'r') as content_file:
		sa_token = content_file.read()    

	# get client token
	vault_dict = {"jwt": sa_token.strip(), "role": vault_role}
	r = requests.post(vault_api_k8s_login_ep, json=vault_dict, verify=False)
	if r.status_code == 200 or r.status_code == 201:
		print("[info-vault] - " , r.status_code)
		json_result = r.json()  
		result = json_result['auth']['client_token']
		return result
	else:
		print("Error: Get client token process from vault failed, code: " + str(r.status_code) )
		print(r.json())

def iam_login():
	#print('client_id:' ,iam_client_id, 'client_secret:', iam_client_secret, 'username:', iam_user, 'password:', iam_pass, 'grant_type:','password','iam_ca_file:',iam_ca_file, 'iam_realm:', iam_realm)
	data = {'client_id': iam_client_id, 'client_secret': iam_client_secret, 'username': iam_user, 'password': iam_pass, 'grant_type':'password'}
	headers = {"Content-Type":"application/x-www-form-urlencoded"}
	ep_url = iam_url+"/auth/realms/"+iam_realm+"/protocol/openid-connect/token"
	#print('ep_url:', ep_url)
	r = requests.post(ep_url,headers=headers,data=data, verify=iam_ca_file)
	if r.status_code == 200:
		return r.json().get('access_token')
	else:
		print('Error')
		print(r.json())

def iam_get_users(jwt_token,user_email):
	#print(jwt_token)
	headers = {"Authorization": "Bearer " + jwt_token , "Content-Type" : "application/json"}
	ep_url = iam_url+"/auth/admin/realms/"+iam_realm+"/users"
	#print('ep_url:', ep_url)
	r = requests.get(ep_url, headers=headers, verify=iam_ca_file)
	print(r.status_code)
	if r.status_code == 200:
		for iamUser in r.json():
			if user_email == iamUser.get('email'):
				print('User found on IAM:',iamUser.get('id'),iamUser.get('username'), iamUser.get('email'))
				return iamUser.get('id')
				break
	else:
		print('Error')
		print(r.json())	

def iam_get_user_groups(jwt_token,iam_user_id):
	#print(jwt_token)
	headers = {"Authorization": "Bearer " + jwt_token , "Content-Type" : "application/json"}
	ep_url = iam_url+"/auth/admin/realms/"+iam_realm+"/users/"+iam_user_id+"/groups"
	print('ep_url:', ep_url)
	r = requests.get(ep_url, headers=headers, verify=iam_ca_file)
	print(r.status_code)
	if r.status_code == 200:
		return r.json()
	else:
		print('Error')
		print(r.json())	

def get_user_mail(user_id):
	params = {'token': slack_bot_user_oauth_token, 'user': user_id}
	ep_url = slack_api+"/users.info"
	r = requests.get(ep_url,params=params)
	if r.status_code == 200:
		return r.json().get('user').get('profile').get('email')
	else:
		print('Error')
		print(r.json())

def ask_for_dg(trigger_id,callback_id,client,user_email,vaultToken = "None"):
	
	iam_access_token   = iam_login()
	iam_user_id        = iam_get_users(iam_access_token,user_email)
	if not iam_user_id:
		# response to Slack after processing is finished
		message = {"text": "Something whent wrong in your request"}
		res = requests.post(callback_id, json=message)
		print('respuesta:',res)
	else:
		iam_user_groups = iam_get_user_groups(iam_access_token,iam_user_id)
		#dgs="mad01,mad02,cac01,tst01,imf01,maraco"

		# Dinamically populate the json_view with the delivery groups found on iam.
		dgs_options = []
		dg_index = 0
		for group in iam_user_groups:
			dg = group.get('name').split('_')[1]
			dgs_options.append({"text": {"type": "plain_text","text": dg},"value": "dg-"+str(dg_index)})
			dg_index += 1
		
		json_view={
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
										"options": dgs_options
								}
							}

						]					
					}
		# This will open the dialog to choose delivery group
		open_dialog = client.views_open(
					trigger_id = trigger_id,
					view=json_view
				)
		# response to Slack after processing is finished
		message = {"text": txtBye}
		res = requests.post(callback_id, json=message)
		print('respuesta:',res)

def get_vault_token(trigger_id,callback_id,client,dg):

	vaultClientToken=""
	vaultClientToken = getVaultClientToken(sa_token_file_location,'dgs_write_'+dg)

	# Repaint!
	open_dialog = client.views_open(
				trigger_id = trigger_id,
				response_action= "push",
				view={
					"type": "modal",
					"callback_id": callback_id,
					"title": {"type": "plain_text",	"text": "Token vault request"},
					"blocks": [
						{"type": "section", "text": {"type": "mrkdwn","text": ":warning: vault-token for [ "+dg+" ]: "+vaultClientToken}}					
					]					
				}
			)

	# response to Slack after processing is finished
	message = {"text": txtBye}
	res = requests.post(callback_id, json=message)
	print('respuesta:',res)

def cantHelp(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text":f"Hello <@{user}>!  ¯\_(ツ)_/¯  sorry, can't help you with that. Try with help"}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def help(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hello <@{user}>! , can help you with this:")
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text": "*- [/iscpbot* help] view this help."}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*- [/iscpbot* get-vault-token] request a token vault"}},
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)



#------
#Main
#------

# Globals
slack_api                     = "https://slack.com/api"
slack_bot_user_oauth_token    = os.environ['SLACK_API_TOKEN']
iam_url                       = os.environ['IAM_URL']
iam_user                      = os.environ['IAM_USER']
iam_pass                      = os.environ['IAM_PASS']
iam_client_id                 = os.environ['IAM_CLIENT_ID']
iam_client_secret             = os.environ['IAM_CLIENT_SECRET']
iam_realm                     = os.environ['IAM_REALM']
iam_ca_file                   = os.environ['IAM_CA_FILE']
sa_token_file_location        = os.environ['SA_TOKEN_FILE_LOCATION']
vault_url                     = os.environ['VAULT_URL'] # https://x-vault.x-vault:8200
vault_api_version             = os.environ['VAULT_API_VERSION'] # v1
vault_api_k8s_login_ep        = vault_url + '/' + vault_api_version + '/' + 'auth/kubernetes/login'
ssl_context                   = ssl_lib.create_default_context(cafile=certifi.where())
client                        = slack.WebClient(token=slack_bot_user_oauth_token, ssl=ssl_context)
txtWait                       = "please wait...."
txtBye                        = "request completed"
user_id                       = ""
callback_id                   = ""

#------------------
# DataHolders
#------------------


if __name__ == "__main__":
	app.run(debug=True)
