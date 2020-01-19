import os
import feedparser
import slack
import certifi
import requests
import threading
from flask import Flask, request, Response, jsonify, json, make_response
import ssl as ssl_lib
from random import randrange
from datetime import datetime

# Globals
app = Flask(__name__)
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'], ssl=ssl_context)
txtWait = "procesando la petición .... por favor espere"
SALIDABICI = {}
g_channel_id = "CRB74AX8U" 
txtBye = "mensaje de repuesta enviado al canal " + g_channel_id
user_id = ""
callback_id = ""
FOTOSDRIVE = {}
FOTOSDRIVE['0'] = "1KLGikwvC1QKWlvvImkMOhi0P3BiBt80a"
FOTOSDRIVE['1'] = "1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO"
FOTOSDRIVE['2'] = "1KIkzRCVF4yGaenTvb4e6SkIjSXcigKr1"
FOTOSDRIVE['3'] = "1K_7jzDeeC58s0hlpUOTCtSnfUU-Q727j"
FOTOSDRIVE['4'] = "1K_xTQrdLevfEMYUfa3oJAYEVfQ7Ih15z"
FOTOSDRIVE['5'] = "1LWkD-ELw60gQyR4IDEdQzWOtg_A3IJgb"
FOTOSDRIVE['6'] = "1MIm8RuxjlG1vc2zkRwkALFeTzGedUFXP"
FOTOSDRIVE['7'] = "1Lo9T_nOXCglDVfGZaxrx7iCqTvuF_alP"
FOTOSDRIVE['8'] = "1KyUMBu-t_Q4JJifW13ku7bQ7vWDNWW8X"
FOTOSDRIVE['9'] = "1L0GFard7_toEDFsk8sF5PguVahzA5eZ7"
FOTOSDRIVE['10'] = "1ST_NMzdzMuOmihzkqz5dYmgsZWK9a-c8"
FOTOSDRIVE['11'] = "1LM_jMxNkI5a3kr2CFMfgmmUH23w3xzHf"
FOTOSDRIVE['12'] = "1LKqMNsRMjhlqPQJFgGs0Zwsectdf-2yp"
FOTOSDRIVE['13'] = "1KoHGVZ_O0cyLfzPeAg-4JNZI1Lqf9K9E"
FOTOSDRIVE['14'] = "1SP-WH7J92JPbWYaRCTEGQJen9NGBPUGN"
FOTOSDRIVE['15'] = "1S51LEfVffX5i8soCwpoc9s1UXALxrSOt"
FOTOSDRIVE['16'] = "1QOxSqyyxs79P0JhZcLAp88wqAZo7R9nH"
FOTOSDRIVE['17'] = "1T2LqeTMIIQOm4XK5Rr1aikTKoZrNnX3Q"
FOTOSDRIVE['18'] = "1SzwCNJGYQgVZspru2RFnKLLHeU3DBrmr"
FOTOSDRIVE['19'] = "1SiPnxgUE3Kw6yhydm1W2R_WEZfefWIxz"
FOTOSDRIVE['20'] = "1SOva3qHNpTdH5U9qq56KawA-ujcC6J52"
FOTOSDRIVE['21'] = "1RpOGAHGhWf8ryyl8zk1XQLzLTHEZnLoT"
FOTOSDRIVE['22'] = "1RZWj3MXvYVUk_WgrKNEQjMOj_S1ph4KP"
FOTOSDRIVE['23'] = "1Re2pHa15CGfGE2AcOh77OD1poLcAhqRG"
FOTOSDRIVE['24'] = "1RYB-6g_Nj2AoUY9YA6bxYcZIw9L-CVSt"
FOTOSDRIVE['25'] = "1RQ180FsAZNJkgM2FUO0vSQvX7IhVzxO0"
FOTOSDRIVE['26'] = "1RCbSU_SUxxvZxVbckQfdHmu3ovyiLLos"
FOTOSDRIVE['27'] = "1RKivuxjFzVBfaBSjG8G3y31oBo8XvJ-r"
FOTOSDRIVE['28'] = "1R4C4mUNiqS8A1oJfznIlGOlyEYU0EhlU"
FOTOSDRIVE['29'] = "1R0Cyf8MIVYJKgsL9g2pxtsMBNFsqDueK"
FOTOSDRIVE['30'] = "1QolF12rPTIv4dqC2ta2MCSvdOvsPymqd"
FOTOSDRIVE['31'] = "1QhrRx_cwKYyxe2zAlKtE2TTAxmsvFcep"
FOTOSDRIVE['32'] = "1QWK5VT1QKg-tpU8q_ZUv5p-VErgqQvyE"
FOTOSDRIVE['33'] = "1QMtZP1A6W3sK54A7T4pQ8XOoKbzRUYPs"
FOTOSDRIVE['34'] = "1Q0IJr_Jj5JlHNBwZS4NDDfJSM9479SR4"
FOTOSDRIVE['35'] = "1P1TKRrJRMscPITNIeVQv8RCt0hdDZu3y"
FOTOSDRIVE['36'] = "1OcJZh-mP3zVr4vBhsoF5pt4kEApRGWPZ"
FOTOSDRIVE['37'] = "1Oz7z01l33T9mjlAcXGLIzFN6hCyVDVcF"
FOTOSDRIVE['38'] = "1OZbYyDAg5wNtbtoAD8P2mQ7ZvoTmMOCW"
FOTOSDRIVE['39'] = "1ODUT45ypsEI-XpQNtjht4rADB49i2bEq"
FOTOSDRIVE['40'] = "1NSblbIa8Lw9K-_XxFwKfe8jZ9sLScR4t"
FOTOSDRIVE['41'] = "1NRmZ8Gx6__CWP-9iojebBY1Q6lwBvXlY"
FOTOSDRIVE['42'] = "1ONyqsPbAr7p1ZqvO1o3JETnUA8JgjQGa"
FOTOSDRIVE['43'] = "1NbaBp0Uux5rsbXnuiFQdzEuSEiVwNVRL"
FOTOSDRIVE['44'] = "1N1NjDZTWlh8Jy-B6wxExj05q6gA3Q5rO"
FOTOSDRIVE['45'] = "1MscI1TwL0OPJkvL8vs8gVRQYm80VwNkP"
FOTOSDRIVE['46'] = "1MpLIgyu6P9-PAqrC8eyoUKyR5LpSf0gO"
FOTOSDRIVE['47'] = "1MhmREfi1zPF7DvZK_nxCSz2IQyOE9JL4"
FOTOSDRIVE['48'] = "1LGLIvg3L2WVp4r270zoX087WRmcPBsyG"
FOTOSDRIVE['49'] = "1KyUMBu-t_Q4JJifW13ku7bQ7vWDNWW8X"
FOTOSDRIVE['50'] = "1KtfBy3WfFYwzaopoELTX4b2PGQz_vmCm"




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
	txtRuta = ""
	actionID = ""
	blockID = ""
	nivelSalida = ""
	fechaSalida = ""
	horaSalida = ""
	userName = ""
	userID = ""

	#--
	# - view_submission payloads are received when a modal is submitted.
	# - block_actions payloads  are received when a user clicks a Block Kit interactive 
	# --
	if message_type == "view_submission":
		#print("------------------view_submission-----------------")
		#print(request.form)
		txtRuta = message_action["view"]["state"]["values"]["input001"]["plain_input"]["value"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		# nos inventamos una key para que en el dict el valor sea unico
		keypart1 = userID+'.'+userName
		keypart2 = keypart1+'.txtRuta'
		SALIDABICI[keypart2] = txtRuta 
		#print(txtRuta)
		print(SALIDABICI)
		
		# verificamos que todos los campos tengan valores.
		# sacamos los datos del dict si existen
		requiredValues = 0

		checkKey =  userID + '.' + userName + '.nivelSalida'
		if checkKey in SALIDABICI:
			nivelSalida = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1
	
		checkKey =  userID + '.' + userName + '.duracionSalida'
		if checkKey in SALIDABICI:
			duracionSalida = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1

		checkKey =  userID + '.' + userName + '.txtRuta'
		if checkKey in SALIDABICI:
			txtRuta = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1

		checkKey =  userID + '.' + userName + '.fechaSalida'
		if checkKey in SALIDABICI:
			fechaSalida = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1

		checkKey =  userID + '.' + userName + '.horaSalida'
		if checkKey in SALIDABICI:
			horaSalida = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1

		if requiredValues == 0:
			proponerSalidaBici(g_channel_id, userName, client,callback_id,nivelSalida,duracionSalida, txtRuta,fechaSalida, horaSalida )
		else:
			helpError(g_channel_id, userID, client,callback_id)
	
	if message_type == "block_actions":
		#print("------------------block_actions-----------------")
		#print(request.form)
		
		actionID = message_action["actions"][0]["action_id"]
		blockID = message_action["actions"][0]["block_id"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		# nos inventamos una key para que en el dict el valor sea unico
		keypart1 = userID+'.'+userName
		
		if actionID == "action002" and blockID == "input002" :
			# Nivel de la salida
			nivelSalida =  message_action["actions"][0]["selected_option"]["text"]["text"]
			keypart2 = keypart1+'.nivelSalida'
			print('Nivel Salida:' , nivelSalida)
			SALIDABICI[keypart2] = nivelSalida  
		if actionID == "action003" and blockID == "input003" :
			# Duracion estimada
			duracionSalida =  message_action["actions"][0]["selected_option"]["text"]["text"]
			keypart2 = keypart1+'.duracionSalida'
			print('Duración Salida:' , duracionSalida)
			SALIDABICI[keypart2] = duracionSalida  
		if blockID == "input004" :
			# Fecha de la salida
			fechaSalida =  message_action["actions"][0]["selected_date"]
			keypart2 = keypart1+'.fechaSalida'
			print('Fecha Salida:' , fechaSalida)
			SALIDABICI[keypart2] = fechaSalida  
		if actionID == "action005" and blockID == "input005" :
			# Hora de la salida
			horaSalida =  message_action["actions"][0]["selected_option"]["text"]["text"]
			keypart2 = keypart1+'.horaSalida'
			print('Hora Salida:' , horaSalida)
			SALIDABICI[keypart2] = horaSalida  

		#--
		# En caso de querer retomar el tema de las botones de accion
		#--
		#
		if blockID == "voyNoVoy":
			clickValue = message_action["actions"][0]["value"]
			if clickValue == "click_noSeguro":
				voy_channel_id = message_action["channel"]["id"]
				voy_message_ts = message_action["message"]["ts"]
				respondProponerSalidaBici(voy_channel_id, user_id, client,callback_id,voy_message_ts,userName, 'no seguro' )
			if clickValue == "click_voy":
				#nivelSalida = SALIDABICI[userID + '.' + userName + '.nivelSalida']
				#duracionSalida = SALIDABICI[userID + '.' + userName + '.duracionSalida']
				#txtRuta = SALIDABICI[userID + '.' + userName + '.txtRuta']
				#voy_action_ts = message_action["actions"][0]["action_ts"]
				voy_channel_id = message_action["channel"]["id"]
				#voy_channel_name = message_action["channel"]["name"]
				#voy_token =  message_action["token"]
				voy_message_ts = message_action["message"]["ts"]
				#UpdateproponerSalidaBici(voy_channel_id, user_id, client,callback_id,nivelSalida,duracionSalida,txtRuta,voy_message_ts,userName )
				respondProponerSalidaBici(voy_channel_id, user_id, client,callback_id,voy_message_ts,userName, 'voy' )
			
	
	# Making empty responses to make slack api happy
	return make_response("", 200)

@app.route('/slackcmd', methods=['POST'])
def inbound():
	# -- Print the entire form
	#print("------------------raw-----------------")
	#print(request.form)
	# --

	# --
	# example of the entire response
    # ImmutableMultiDict([('token', 'Ol1Y4KZRMUcPvvcC7yUxt16e'),
	#  ('team_id', 'TRBLUFYAH'),
	# ('team_domain', 'mipiri'),
	# ('channel_id', 'DREDQNAUQ'),
	# ('channel_name', 'directmessage'),
	# ('user_id', 'URBLUFZFF'),
	# ('user_name', 'msoranno'),
	#  ('command', '/fstbot'),
	#  ('text', ''),
	# ('response_url', 'https://hooks.slack.com/commands/TRBLUFYAH/902962838352/X7nxg9gCx5ohKPj8Y8YIZCmW'),
	# ('trigger_id', '905169528534.861708542357.1dab914da529c471b93ab600fd0b9ba2')])
    # --
    
	slack_request = request.form
	trigger_id = slack_request["trigger_id"]
	callback_id = slack_request["response_url"]
	text = str(slack_request["text"]).lower()
	channel_id = slack_request["channel_id"]
	user_id = slack_request["user_id"]
	user_name =slack_request["user_name"]

	#print("-----------------------------------------------------------------")
	#print(trigger_id, callback_id, text, channel_id, user_id,user_name)

	if text == "help":
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=help,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "quien es juanjo" in text :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=quienesjuano,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "foto aleatoria" in text :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=randomPic,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "horario gym" in text or "horarios gym" in text :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=horariosFitness,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "tri noticias" in text :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=triNews,args=(ssl_context,channel_id,user_id,client,callback_id))
		x.start()		
		return txtWait

	if "salida bici" in text :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=salidaBici,args=(trigger_id,callback_id,client))
		x.start()		
		return txtWait

def respondProponerSalidaBici(channel_id,user,web_client,callback_id,message_ts,userName, vaOnoVa):
	print("El usuario: ", userName, "dice que: ", vaOnoVa)
	if vaOnoVa == "voy":
		web_client.chat_postMessage(
			channel=channel_id,
			thread_ts=message_ts,
			#text=f":heavy_check_mark: <@{user}>"
			text=f"Yo <@{userName}>! me apunto... :heavy_check_mark:"
			# blocks = [
			# 	{
			# 		"type": "section",
			# 		"text": {"type": "mrkdwn","text": "de Colombia para el mundo papa...*juepuuuuu*"}
			# 	}
			# ]    
		)
	
	if vaOnoVa == "no seguro":
		web_client.chat_postMessage(
			channel=channel_id,
			thread_ts=message_ts,
			#text=f":heavy_check_mark: <@{user}>"
			text=f"Yo <@{userName}>! soy duda... :man-shrugging:"
		)



def proponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta, fecha_salida, hora_salida):
    web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
	  blocks = [
	        {
				"type": "divider"
			},
			{
				"type": "section",
				"text": {"type": "mrkdwn","text":":man-biking: *SALIDA EN BICI PROPUESTA POR:* " + user  + ':man-biking:'}
			},
			{
				"type": "context",
				"elements": [
					{
						"text":  texto_ruta.strip(),
						"type": "mrkdwn"
					}
				]
			},			
			{
				"type": "section",
				"fields": [
					{"type": "mrkdwn",	"text": "*Fecha:*\n" + fecha_salida},
					{"type": "mrkdwn",	"text": "*Hora:*\n" + hora_salida},
					{"type": "mrkdwn",	"text": "*Nivel:*\n" + salida_nivel	},
					{"type": "mrkdwn",	"text": "*Duración:*\n" + duracion_salida}
				]
			},
			{
				"type": "image",
				"title": {
					"type": "plain_text",
					"text": "foto aleatoria...."
				},
				"image_url": "https://drive.google.com/uc?id="+ FOTOSDRIVE[str(randrange(len(FOTOSDRIVE)))],
				"alt_text": "Example Image"
			},
			{
				"type": "actions",
				"block_id": "voyNoVoy",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "me apunto"
						},
						"style": "primary",
						"value": "click_voy"
					},
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "soy duda"
						},
						"style": "danger",
						"value": "click_noSeguro"
					}
				]
			}
      ]    
    )

def salidaBici(trigger_id,callback_id,client):
	open_dialog = client.views_open(
				trigger_id = trigger_id,
				view={
					"type": "modal",
					"callback_id": callback_id,
					"title": {"type": "plain_text",	"text": "Salida en bici"},
					"submit": {"type": "plain_text","text": "Submit"},
					"close": {"type": "plain_text",	"text": "Cancel"},					
					"blocks": [
						{
							"type": "input",
							"block_id": "input001",
							"label": {"type": "plain_text","text": "*** Todos los campos son obligatorios ***\n\nDescripción, punto de encuentro, etc"},
							"element": {
								"type": "plain_text_input",
								"action_id": "plain_input",
								"multiline": True,
								"placeholder": {"type": "plain_text","text": "Describa la ruta en terminos generales"}
							}
						},
						{
							"type": "section",
							"block_id": "input002",
							"text": {"type": "mrkdwn","text": "Nivel permitido ?"},
							"accessory": {
								"action_id": "action002","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "todos"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "medio"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "alto"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "muy alto"},"value": "value-3"},
										{"text": {"type": "plain_text","text": "Chema Camacho!!"},"value": "value-4"}
									]
							}
						},						
						{
							"type": "section",
							"block_id": "input003",
							"text": {"type": "mrkdwn","text": "Tiempo estimado de la ruta ?"	},
							"accessory": {
								"action_id": "action003","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "1-2 hrs"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "2-3 hrs"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "3-4 hrs"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "4-5 hrs"},"value": "value-3"},
										{"text": {"type": "plain_text","text": "5-6 hrs"},"value": "value-4"},
										{"text": {"type": "plain_text","text": "6-7 hrs"},"value": "value-5"},
										{"text": {"type": "plain_text","text": "no tengo idea"},"value": "value-6"}								
									]
							}
						},						
						{
							"type": "section",
							"block_id": "input004",
							"text": {"type": "mrkdwn","text": "Fecha ?"},
							"accessory": {
											"type": "datepicker",
											"initial_date": datetime.today().strftime('%Y-%m-%d'),
											"placeholder": {"type": "plain_text","text": "Cuando salimos ?"	}
							}
						},						
						{
							"type": "section",
							"block_id": "input005",
							"text": {"type": "mrkdwn","text": "Hora ?"	},
							"accessory": {
								"action_id": "action005","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "05:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "05:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "05:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "05:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "06:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "06:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "06:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "06:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "07:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "07:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "07:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "07:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "08:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "08:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "08:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "08:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "09:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "09:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "09:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "09:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "11:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "10:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "11:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "11:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "11:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "11:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "12:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "12:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "12:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "12:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "13:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "13:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "13:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "13:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "14:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "14:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "14:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "14:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "15:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "15:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "15:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "15:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "16:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "16:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "16:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "16:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "17:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "17:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "17:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "17:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "18:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "18:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "18:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "18:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "19:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "19:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "19:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "19:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "20:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "20:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "20:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "20:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "21:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "21:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "21:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "21:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "22:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "22:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "22:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "22:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "23:00 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "23:15 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "23:30 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "23:45 hrs"},"value": " "},
										{"text": {"type": "plain_text","text": "24:00 hrs"},"value": " "}
									]
							}
						}						
					]					
				}
			)

	# response to Slack after processing is finished
	message = {"text": txtBye}
	res = requests.post(callback_id, json=message)
	print('respuesta:',res)

def help(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>! , veo que necesitas ayuda. Este es un listado de las cosas que puedes hacer llamandome:")
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text": "*[/fstbot* tri noticias] mostrar noticias del mundo del triatlón"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*[/fstbot* quien es juanjo ?] saber mas del personaje"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* horario gym] conocer horarios actualizados del gimnasio"}},
	  {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* salida bici] proponer salidas de bici"}},
	  {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* foto aleatoria] mostrar foto aleatoria del club y su gente"}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def helpError(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>!. Ha ocurrido un error. El formulario anterior no fue rellenado correctamente. Ningún campo puede quedar vacío.")

def randomPic(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text":f"Hola <@{user}>! esta es la foto que hemos escogido para ti !!"}
            },
			{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "foto aleatoria"
			},
			"image_url": "https://drive.google.com/uc?id="+ FOTOSDRIVE[str(randrange(len(FOTOSDRIVE)))],
			"alt_text": "foto aleatoria"
		    }
      ]    
    )
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def quienesjuano(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text": "de Colombia para el mundo papa...*juepuuuuu*"}
            },
			{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "Menudo pajaro!!!"
			},
			"image_url": "https://drive.google.com/uc?id=1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO",
			"alt_text": "Example Image"
		    }
      ]    
    )
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)


def horariosFitness(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text": "<http://fitnessports.eu/wp-content/uploads/pdf/Horarios%20Fitness%20Sports%20actualizado.pdf|Este link te llevará a los horarios del gym ;)>"}
            }
      ]    
    )
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)


def triNews(ssl_context,channel_id,user,web_client,callback_id):
    # https://www.triathlon.org/feeds/news
    url = 'http://feeds.feedburner.com/TriatlonNoticias?format=xml'
    ssl_lib._create_default_https_context=ssl_lib._create_unverified_context
    feed = feedparser.parse(url)
    for post in feed.entries:
        title = str(post.title)
        # description = str(post.description)
        link_url = str(post.link)
        web_client.chat_postMessage(
          channel=channel_id,
          # thread_ts=thread_ts,
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
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

@app.route('/', methods=['GET'])
def test():
	return Response('It works!')


if __name__ == "__main__":
	app.run(debug=True)
