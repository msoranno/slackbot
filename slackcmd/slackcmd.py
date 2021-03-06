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

# algunos exports requeridos
# testing channel CRB74AX8U (mipiri)
# export SLACK_BIKE_CHANNEL_ID=CRB74AX8U
# export SLACK_BIKE_CHANNEL_NAME=bot-testing
# export SLACK_RUN_CHANNEL_ID=CRB74AX8U
# export SLACK_RUN_CHANNEL_NAME=general
# export SLACK_GENERAL_CHANNEL_ID=CRB74AX8U
# export SLACK_GENERAL_CHANNEL_NAME=varios
# fst
# export SLACK_BIKE_CHANNEL_ID=CQ56F3UL9
# export SLACK_BIKE_CHANNEL_NAME=salidas-bici
# export SLACK_RUN_CHANNEL_ID=CQCKVFVA8
# export SLACK_RUN_CHANNEL_NAME=tapias
# export SLACK_GENERAL_CHANNEL_ID=CQXAF2KUJ
# export SLACK_GENERAL_CHANNEL_NAME=eventossociales

# Globals
app = Flask(__name__)
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'], ssl=ssl_context)
txtWait = "procesando la petición .... por favor espere"
SALIDABICI = {}

SLACK_BIKE_CHANNEL_ID = os.environ['SLACK_BIKE_CHANNEL_ID']
SLACK_BIKE_CHANNEL_NAME = os.environ['SLACK_BIKE_CHANNEL_NAME']
SLACK_RUN_CHANNEL_ID = os.environ['SLACK_RUN_CHANNEL_ID']
SLACK_RUN_CHANNEL_NAME = os.environ['SLACK_RUN_CHANNEL_NAME']
SLACK_GENERAL_CHANNEL_ID = os.environ['SLACK_GENERAL_CHANNEL_ID']
SLACK_GENERAL_CHANNEL_NAME = os.environ['SLACK_GENERAL_CHANNEL_NAME']

txtBye = "petición completada"
user_id = ""
callback_id = ""
FOTOSDRIVE = {}

def loadPics():
	# Using readlines() 
	file1 = open('./slackcmd/pics.txt', 'r') 
	Lines = file1.readlines() 
	
	count = 0
	# Strips the newline character 
	count = 0
	for line in Lines: 
		#print(line.strip(), count) 
		FOTOSDRIVE[str(count)] = line.strip()
		#print(count)
		count += 1

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

		checkKey =  userID + '.' + userName + '.tipoSalida'
		if checkKey in SALIDABICI:
			tipoSalida = SALIDABICI[checkKey]
		else:
			print("Key: ", checkKey, "NO EXISTE" )
			requiredValues = 1

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

		# aseguramos un canal
		canal_slack_id = SLACK_BIKE_CHANNEL_ID
		canal_slack_name = SLACK_BIKE_CHANNEL_NAME
		if requiredValues == 0:
			if tipoSalida == "ruta en bici de carretera" or tipoSalida == "ruta en bici de montaña":
				canal_slack_id = SLACK_BIKE_CHANNEL_ID
				canal_slack_name = SLACK_BIKE_CHANNEL_NAME
			if tipoSalida == "carrera a pie" :
				canal_slack_id = SLACK_RUN_CHANNEL_ID
				canal_slack_name = SLACK_RUN_CHANNEL_NAME
			if tipoSalida == "evento social" :
				canal_slack_id  = SLACK_GENERAL_CHANNEL_ID
				canal_slack_name  = SLACK_GENERAL_CHANNEL_NAME
			
			txtBye = "petición completada, revise el canal " + canal_slack_name
			proponerSalidaBici(canal_slack_id, userName, client,callback_id,nivelSalida,duracionSalida, txtRuta,fechaSalida, horaSalida, tipoSalida )
		else:
			helpError(canal_slack_id, userID, client,callback_id)
	
	if message_type == "block_actions":
		#print("------------------block_actions-----------------")
		#print(request.form)
		
		actionID = message_action["actions"][0]["action_id"]
		blockID = message_action["actions"][0]["block_id"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		# nos inventamos una key para que en el dict el valor sea unico
		keypart1 = userID+'.'+userName
		
		if actionID == "action000" and blockID == "input000" :
			# Typo de quedada
			tipoSalida =  message_action["actions"][0]["selected_option"]["text"]["text"]
			keypart2 = keypart1+'.tipoSalida'
			print('Tipo de Salida:' , tipoSalida)
			SALIDABICI[keypart2] = tipoSalida  
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
		if actionID == "action004" and blockID == "input004" :
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
	podemosAyudar = 0
	if text == "help" or text == "ayuda":
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=help,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "quien es juanjo" in text or "quien juanjo" in text :
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=quienesjuano,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "foto" in text or "fotos" in text or "pics" in text :
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=randomPic,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "horario" in text or "horarios gym" in text :
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=horariosFitness,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

	if "noticia" in text or "news" in text:
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=triNews,args=(ssl_context,channel_id,user_id,client,callback_id))
		x.start()		
		return txtWait

	if "quedar" in text or "quedada" in text or "salida" in text :
		podemosAyudar = 1
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=salidaBici,args=(trigger_id,callback_id,client))
		x.start()		
		return txtWait
	# --
	# si no hay nada para lo introducido
	# --
	if podemosAyudar == 0 :
		# starting a new thread for doing the actual processing
		x = threading.Thread(target=noPodemosAyudar,args=(channel_id, user_id, client,callback_id))
		x.start()		
		return txtWait

def respondProponerSalidaBici(channel_id,user,web_client,callback_id,message_ts,userName, vaOnoVa):
	print("El usuario: ", userName, "dice que: ", vaOnoVa)
	if vaOnoVa == "voy":
		web_client.chat_postMessage(
			channel=channel_id,
			thread_ts=message_ts,
			#text=f":heavy_check_mark: <@{user}>"
			text=f"<@{userName}>! me apunto... :heavy_check_mark:"
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
			text=f"Yo <@{userName}>! soy duda...  ¯\_(ツ)_/¯ "
		)

def findDay(fecha): 
	#datetime_object = datetime.strptime(fecha, '%Y-%m-%d')
	elDiaInt = datetime.strptime(fecha, '%Y-%m-%d').weekday() 
	elDia = (calendar.day_name[elDiaInt]) 
	if elDia.strip() == "Sunday": elDia = "Domingo"
	if elDia.strip() == "Monday": elDia = "Lunes"
	if elDia.strip() == "Tuesday": elDia = "Martes"
	if elDia.strip() == "Wednesday": elDia = "Miércoles"
	if elDia.strip() == "Thursday": elDia = "Jueves"
	if elDia.strip() == "Friday": elDia = "Viernes"
	if elDia.strip() == "Saturday": elDia = "Sábado"
	return (elDia) 
	
def proponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta, fecha_salida, hora_salida, tipoSalida):
	print('total pics: ', len(FOTOSDRIVE))
	print('day:', findDay(fecha_salida)) 
	web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
	  blocks = [
	        {
				"type": "divider"
			},
			{
				"type": "section",
				"text": {"type": "mrkdwn","text":f":mega: *PROPUESTA PARA QUEDAR :mega:* \n >por: <@{user}>"  }
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
					{"type": "mrkdwn",	"text": "*Tipo de quedada:*\n" + tipoSalida},
					{"type": "mrkdwn",	"text": "*Fecha YYYY-MM-DD:*\n" + findDay(fecha_salida) + ' ' + fecha_salida},
					{"type": "mrkdwn",	"text": "*Hora:*\n" + hora_salida},
					{"type": "mrkdwn",	"text": "*Nivel recomendado:*\n" + salida_nivel	},
					{"type": "mrkdwn",	"text": "*Duración:*\n" + duracion_salida}
				]
			},
			{
				"type": "image",
				"title": {
					"type": "plain_text",
					"text": "foto aleatoria...."
				},
				"image_url": "https://drive.google.com/uc?id="+  FOTOSDRIVE[str(randrange(0,len(FOTOSDRIVE),randrange(1,10)))],
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
	yesterday = date.today() - timedelta(days=1)
	yesterdayIs = yesterday.strftime('%Y-%m-%d')

	open_dialog = client.views_open(
				trigger_id = trigger_id,
				view={
					"type": "modal",
					"callback_id": callback_id,
					"title": {"type": "plain_text",	"text": "QUEDAMOS...?"},
					"submit": {"type": "plain_text","text": "Submit"},
					"close": {"type": "plain_text",	"text": "Cancel"},					
					"blocks": [
						{"type": "section", "text": {"type": "mrkdwn","text": "*> :warning: todos los campos son obligatorios*"}},						
						{
							"type": "section",
							"block_id": "input000",
							"text": {"type": "mrkdwn","text": "Propongo...."},
							"accessory": {
								"action_id": "action000","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "ruta en bici de carretera"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "ruta en bici de montaña"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "carrera a pie"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "evento social"},"value": "value-3"}
									]
							}
						},						
						{
							"type": "input",
							"block_id": "input001",
							"label": {"type": "plain_text","text": "Descripción, punto de encuentro, etc"},
							"element": {
								"type": "plain_text_input",
								"action_id": "plain_input",
								"multiline": True,
								"placeholder": {"type": "plain_text","text": "Describe un poco la propuesta..."}
							}
						},
						{
							"type": "section",
							"block_id": "input002",
							"text": {"type": "mrkdwn","text": "Nivel recomendado...?"},
							"accessory": {
								"action_id": "action002","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "todos"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "medio"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "alto"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "muy alto"},"value": "value-3"},
										{"text": {"type": "plain_text","text": "a machete"},"value": "value-4"}
									]
							}
						},						
						{
							"type": "section",
							"block_id": "input003",
							"text": {"type": "mrkdwn","text": "Tiempo estimado...?"	},
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
							"text": {"type": "mrkdwn","text": "Fecha...?"},
							"accessory": {
											"type": "datepicker",
											"action_id": "action004",
											"placeholder": {
												"type": "plain_text",
												"text": "Seleccione"
											},
											"initial_date": str(yesterdayIs)
							}
						},						
						{
							"type": "section",
							"block_id": "input005",
							"text": {"type": "mrkdwn","text": "Hora...?"	},
							"accessory": {
								"action_id": "action005","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "05:00 hrs"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "05:15 hrs"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "05:30 hrs"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "05:45 hrs"},"value": "value-3"},
										{"text": {"type": "plain_text","text": "06:00 hrs"},"value": "value-4"},
										{"text": {"type": "plain_text","text": "06:15 hrs"},"value": "value-5"},
										{"text": {"type": "plain_text","text": "06:30 hrs"},"value": "value-6"},
										{"text": {"type": "plain_text","text": "06:45 hrs"},"value": "value-7"},
										{"text": {"type": "plain_text","text": "07:00 hrs"},"value": "value-8"},
										{"text": {"type": "plain_text","text": "07:15 hrs"},"value": "value-9"},
										{"text": {"type": "plain_text","text": "07:30 hrs"},"value": "value-10"},
										{"text": {"type": "plain_text","text": "07:45 hrs"},"value": "value-11"},
										{"text": {"type": "plain_text","text": "08:00 hrs"},"value": "value-12"},
										{"text": {"type": "plain_text","text": "08:15 hrs"},"value": "value-13"},
										{"text": {"type": "plain_text","text": "08:30 hrs"},"value": "value-14"},
										{"text": {"type": "plain_text","text": "08:45 hrs"},"value": "value-15"},
										{"text": {"type": "plain_text","text": "09:00 hrs"},"value": "value-16"},
										{"text": {"type": "plain_text","text": "09:15 hrs"},"value": "value-17"},
										{"text": {"type": "plain_text","text": "09:30 hrs"},"value": "value-18"},
										{"text": {"type": "plain_text","text": "09:45 hrs"},"value": "value-19"},
										{"text": {"type": "plain_text","text": "10:00 hrs"},"value": "value-20"},
										{"text": {"type": "plain_text","text": "10:15 hrs"},"value": "value-21"},
										{"text": {"type": "plain_text","text": "10:30 hrs"},"value": "value-22"},
										{"text": {"type": "plain_text","text": "10:45 hrs"},"value": "value-23"},
										{"text": {"type": "plain_text","text": "11:00 hrs"},"value": "value-24"},
										{"text": {"type": "plain_text","text": "10:00 hrs"},"value": "value-25"},
										{"text": {"type": "plain_text","text": "10:15 hrs"},"value": "value-26"},
										{"text": {"type": "plain_text","text": "10:30 hrs"},"value": "value-27"},
										{"text": {"type": "plain_text","text": "10:45 hrs"},"value": "value-28"},
										{"text": {"type": "plain_text","text": "11:00 hrs"},"value": "value-29"},
										{"text": {"type": "plain_text","text": "11:15 hrs"},"value": "value-30"},
										{"text": {"type": "plain_text","text": "11:30 hrs"},"value": "value-31"},
										{"text": {"type": "plain_text","text": "11:45 hrs"},"value": "value-32"},
										{"text": {"type": "plain_text","text": "12:00 hrs"},"value": "value-33"},
										{"text": {"type": "plain_text","text": "12:15 hrs"},"value": "value-34"},
										{"text": {"type": "plain_text","text": "12:30 hrs"},"value": "value-35"},
										{"text": {"type": "plain_text","text": "12:45 hrs"},"value": "value-36"},
										{"text": {"type": "plain_text","text": "13:00 hrs"},"value": "value-37"},
										{"text": {"type": "plain_text","text": "13:15 hrs"},"value": "value-38"},
										{"text": {"type": "plain_text","text": "13:30 hrs"},"value": "value-39"},
										{"text": {"type": "plain_text","text": "13:45 hrs"},"value": "value-40"},
										{"text": {"type": "plain_text","text": "14:00 hrs"},"value": "value-41"},
										{"text": {"type": "plain_text","text": "14:15 hrs"},"value": "value-42"},
										{"text": {"type": "plain_text","text": "14:30 hrs"},"value": "value-43"},
										{"text": {"type": "plain_text","text": "14:45 hrs"},"value": "value-44"},
										{"text": {"type": "plain_text","text": "15:00 hrs"},"value": "value-45"},
										{"text": {"type": "plain_text","text": "15:15 hrs"},"value": "value-46"},
										{"text": {"type": "plain_text","text": "15:30 hrs"},"value": "value-47"},
										{"text": {"type": "plain_text","text": "15:45 hrs"},"value": "value-48"},
										{"text": {"type": "plain_text","text": "16:00 hrs"},"value": "value-49"},
										{"text": {"type": "plain_text","text": "16:15 hrs"},"value": "value-50"},
										{"text": {"type": "plain_text","text": "16:30 hrs"},"value": "value-51"},
										{"text": {"type": "plain_text","text": "16:45 hrs"},"value": "value-52"},
										{"text": {"type": "plain_text","text": "17:00 hrs"},"value": "value-53"},
										{"text": {"type": "plain_text","text": "17:15 hrs"},"value": "value-54"},
										{"text": {"type": "plain_text","text": "17:30 hrs"},"value": "value-55"},
										{"text": {"type": "plain_text","text": "17:45 hrs"},"value": "value-56"},
										{"text": {"type": "plain_text","text": "18:00 hrs"},"value": "value-57"},
										{"text": {"type": "plain_text","text": "18:15 hrs"},"value": "value-58"},
										{"text": {"type": "plain_text","text": "18:30 hrs"},"value": "value-59"},
										{"text": {"type": "plain_text","text": "18:45 hrs"},"value": "value-60"},
										{"text": {"type": "plain_text","text": "19:00 hrs"},"value": "value-61"},
										{"text": {"type": "plain_text","text": "19:15 hrs"},"value": "value-62"},
										{"text": {"type": "plain_text","text": "19:30 hrs"},"value": "value-63"},
										{"text": {"type": "plain_text","text": "19:45 hrs"},"value": "value-64"},
										{"text": {"type": "plain_text","text": "20:00 hrs"},"value": "value-65"},
										{"text": {"type": "plain_text","text": "20:15 hrs"},"value": "value-66"},
										{"text": {"type": "plain_text","text": "20:30 hrs"},"value": "value-67"},
										{"text": {"type": "plain_text","text": "20:45 hrs"},"value": "value-68"},
										{"text": {"type": "plain_text","text": "21:00 hrs"},"value": "value-69"},
										{"text": {"type": "plain_text","text": "21:15 hrs"},"value": "value-70"},
										{"text": {"type": "plain_text","text": "21:30 hrs"},"value": "value-71"},
										{"text": {"type": "plain_text","text": "21:45 hrs"},"value": "value-72"},
										{"text": {"type": "plain_text","text": "22:00 hrs"},"value": "value-73"},
										{"text": {"type": "plain_text","text": "22:15 hrs"},"value": "value-74"},
										{"text": {"type": "plain_text","text": "22:30 hrs"},"value": "value-75"},
										{"text": {"type": "plain_text","text": "22:45 hrs"},"value": "value-76"},
										{"text": {"type": "plain_text","text": "23:00 hrs"},"value": "value-77"},
										{"text": {"type": "plain_text","text": "23:15 hrs"},"value": "value-78"},
										{"text": {"type": "plain_text","text": "23:30 hrs"},"value": "value-79"},
										{"text": {"type": "plain_text","text": "23:45 hrs"},"value": "value-80"},
										{"text": {"type": "plain_text","text": "24:00 hrs"},"value": "value-81"}
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

def noPodemosAyudar(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text":f"Hola <@{user}>!  ¯\_(ツ)_/¯  lo siento , todavía no puedo ayudarte con eso."}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def help(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>! , veo que necesitas ayuda. Este es un listado de las cosas que puedo hacer por ti:")
    web_client.chat_postMessage(channel=channel_id, blocks = [
      {"type": "section", "text": {"type": "mrkdwn","text": "*[/fstbot* noticias] mostrar noticias del mundo del triatlón"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*[/fstbot* quien es juanjo ?] saber mas del personaje"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* horario] conocer horarios actualizados del gimnasio"}},
	  {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* quedar] proponer quedadas"}},
	  {"type": "section", "text": {"type": "mrkdwn","text": "[*/fstbot* foto ] mostrar foto aleatoria del club"}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def helpError(channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>!. Ha ocurrido un error. El formulario anterior no fue rellenado correctamente. Ningún campo puede quedar vacío.")

def randomPic(channel_id,user,web_client,callback_id):
	print('total pics: ', len(FOTOSDRIVE))
	web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
      blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn","text":f"Hola <@{user}>! esta es la foto aleatoria que te ha tocado... !!"}
            },
			{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "foto aleatoria"
			},
			"image_url": "https://drive.google.com/uc?id="+  FOTOSDRIVE[str(randrange(0,len(FOTOSDRIVE),randrange(1,10)))],
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
                "text": {"type": "mrkdwn","text":f"Hola <@{user}>! \n..... *Este es nuestro Juanjo* .... de Colombia para el mundo papa...*juepuuuuu*"}
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
                "text": {"type": "mrkdwn","text":f"Hola <@{user}>! \n <http://fitnessports.eu/wp-content/uploads/pdf/Horarios%20Fitness%20Sports%20actualizado.pdf|Este link te llevará a los horarios del gym ;)>"}
            }
      ]    
    )
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

def triNews(ssl_context,channel_id,user,web_client,callback_id):
    web_client.chat_postMessage(channel=channel_id,text=f"Hola <@{user}>! , a continuación las noticias mas recientes del mundo del triatlon. \n ...luego nos cuentas!! \n\n")
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
                    "text": {"type": "mrkdwn", "text": "*"+title+"*"}
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
	loadPics()
	app.run(debug=True)
