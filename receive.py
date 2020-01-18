import os
import feedparser
import slack
import certifi
import requests
import threading
from flask import Flask, request, Response, jsonify, json, make_response
import ssl as ssl_lib

# Globals
app = Flask(__name__)
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'], ssl=ssl_context)
txtWait = "procesando la petición .... por favor espere"
txtBye = "bye"
SALIDABICI = {}
g_channel_id = "CRB74AX8U" 
user_id = ""
callback_id = ""
FOTOSDRIVE = {}
FOTOSDRIVE['1'] = "1KLGikwvC1QKWlvvImkMOhi0P3BiBt80a"
FOTOSDRIVE['2'] = "1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO"


# -----------------
# This is a working example using slack "event actions"
# -----------------
# @app.route('/slack', methods=['POST'])
# def inbound():
# 	message_action = json.loads(request.form["payload"])
# 	message_type = message_action["type"]
# 	trigger_id = message_action["trigger_id"]
# 	user_id = message_action["user"]["name"]
# 	callback_id = message_action["callback_id"]
# 	trigger_id = message_action["trigger_id"]
# 	print(message_type, user_id,callback_id,trigger_id)
# 	open_dialog = client.views_open(
# 				trigger_id = trigger_id,
# 				view={
# 				    "type": "modal",
# 				    "callback_id": callback_id,
# 				    "title": {
# 				      "type": "plain_text",
# 				      "text": "Just a modal"
# 				    },
# 				    "blocks": [
# 				      {
# 				        "type": "section",
# 				        "block_id": "section-identifier",
# 				        "text": {
# 				          "type": "mrkdwn",
# 				          "text": "*Welcome* to ~my~ Block Kit _modal_!"
# 				        },
# 				        "accessory": {
# 				          "type": "button",
# 				          "text": {
# 				            "type": "plain_text",
# 				            "text": "Just a button"
# 				          },
# 				          "action_id": "button-identifier"
# 				        }
# 				      }
# 				    ]
# 				}
# 			)

# 	print(open_dialog)
# 	return (message_action)

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
	userName = ""
	userID = ""

	#--
	# - view_submission payloads are received when a modal is submitted.
	# - block_actions payloads  are received when a user clicks a Block Kit interactive 
	# --
	if message_type == "view_submission":
		txtRuta = message_action["view"]["state"]["values"]["input001"]["plain_input"]["value"]
		userID = message_action["user"]["id"]
		userName =  message_action["user"]["username"]
		# nos inventamos una key para que en el dict el valor sea unico
		keypart1 = userID+'.'+userName
		keypart2 = keypart1+'.txtRuta'
		SALIDABICI[keypart2] = txtRuta 
		#print(txtRuta)
		print(SALIDABICI)
		# Aqui ahora solo tocaría mandar el mensaje, descomponer del dict los valores 
		# que vayamos a meter en el block del mensaje y pasarlos todo como parametro
		# hay que resolver el problema de como obtener el channel_id de forma dinámica
		# 
		nivelSalida = SALIDABICI[userID + '.' + userName + '.nivelSalida']
		duracionSalida = SALIDABICI[userID + '.' + userName + '.duracionSalida']
		txtRuta = SALIDABICI[userID + '.' + userName + '.txtRuta']
		
		proponerSalidaBici(g_channel_id, user_id, client,callback_id,nivelSalida,duracionSalida, txtRuta )
	
	if message_type == "block_actions":
		print("------------------block_actions-----------------")
		print(request.form)
		
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
		
		#--
		# En caso de querer retomar el tema de las botones de accion
		#--
		# if blockID == "voyNoVoy":
		# 	clickValue = message_action["actions"][0]["value"]
		# 	if clickValue == "click_voy":
		# 		#nivelSalida = SALIDABICI[userID + '.' + userName + '.nivelSalida']
		# 		#duracionSalida = SALIDABICI[userID + '.' + userName + '.duracionSalida']
		# 		#txtRuta = SALIDABICI[userID + '.' + userName + '.txtRuta']
		# 		voy_action_ts = message_action["actions"][0]["action_ts"]
		# 		voy_channel_id = message_action["channel"]["id"]
		# 		voy_channel_name = message_action["channel"]["name"]
		# 		voy_token =  message_action["token"]
		# 		voy_message_ts = message_action["message"]["ts"]
		# 		#UpdateproponerSalidaBici(voy_channel_id, user_id, client,callback_id,nivelSalida,duracionSalida,txtRuta,voy_message_ts,userName )
		# 		UpdateproponerSalidaBici(voy_channel_id, user_id, client,callback_id,voy_message_ts,userName )
			
	
	# Making empty responses to make slack api happy
	return make_response("", 200)

@app.route('/slackcmd', methods=['POST'])
def inbound():
	# -- Print the entire form
	print("------------------raw-----------------")
	print(request.form)
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

	print("-----------------------------------------------------------------")
	print(trigger_id, callback_id, text, channel_id, user_id,user_name)

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


# def UpdateproponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta,message_ts,userName):
#-- 
# Método para actualizar un mensaje previo, no está bien logrado, hay que darle mas vueltas... probablemente usar un backend
# para guardar datos.
# En la actualización debe ir el bloque completo para actualice exactamente el mismo mensaje.
#--
#     web_client.chat_update(
#       channel=channel_id,
#       ts=message_ts,
# 	  text=":white_check_mark: " + userName,
#       blocks = [
# 	        {
# 				"type": "divider"
# 			},
# 			{
# 				"type": "section",
# 				"text": {
# 					"type": "mrkdwn",
# 					"text": "*La ruta:*\n" + texto_ruta
# 				}
# 			},
# 			{
# 				"type": "section",
# 				"fields": [
# 					{
# 						"type": "mrkdwn",
# 						"text": "*Nivel:*\n" + salida_nivel
# 					},
# 					{
# 						"type": "mrkdwn",
# 						"text": "*Duración:*\n" + duracion_salida
# 					}
# 				]
# 			},
# 			{
# 				"type": "image",
# 				"title": {
# 					"type": "plain_text",
# 					"text": "foto aleatoria.... Esto ha cambiado"
# 				},
# 				"image_url": "https://drive.google.com/uc?id=1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO",
# 				"alt_text": "Example Image"
# 			},
# 			{
# 				"type": "divider"
# 			},
# 			{
# 				"type": "actions",
# 				"block_id": "voyNoVoy",
# 				"elements": [
# 					{
# 						"type": "button",
# 						"text": {
# 							"type": "plain_text",
# 							"text": "VOY\n" + userName + ' '
# 						},
# 						"style": "primary",
# 						"value": "click_voy"
# 					},
# 					{
# 						"type": "button",
# 						"text": {
# 							"type": "plain_text",
# 							"text": "NO ES SEGURO"
# 						},
# 						"style": "danger",
# 						"value": "click_noSeguro"
# 					}
# 				]
# 			},
# 			{
# 				"type": "divider"
# 			}
#       ]    


#     )

def proponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta):

   

    web_client.chat_postMessage(
      channel=channel_id,
      # thread_ts=thread_ts,
      blocks = [
	        {
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*La ruta:*\n" + texto_ruta
				}
			},
			{
				"type": "section",
				"fields": [
					{
						"type": "mrkdwn",
						"text": "*Nivel:*\n" + salida_nivel
					},
					{
						"type": "mrkdwn",
						"text": "*Duración:*\n" + duracion_salida
					}
				]
			},
			{
				"type": "image",
				"title": {
					"type": "plain_text",
					"text": "foto aleatoria...."
				},
				"image_url": "https://drive.google.com/uc?id="+ FOTOSDRIVE['1'],
				"alt_text": "Example Image"
			},
			{
				"type": "divider"
			}
      ]    
    )

# def proponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta):
# --
# Dejaré este codigo aqui solo para tener una referencia de como crear botones de accion.
# -- 
#     web_client.chat_postMessage(
#       channel=channel_id,
#       # thread_ts=thread_ts,
#       blocks = [
# 	        {
# 				"type": "divider"
# 			},
# 			{
# 				"type": "section",
# 				"text": {
# 					"type": "mrkdwn",
# 					"text": "*La ruta:*\n" + texto_ruta
# 				}
# 			},
# 			{
# 				"type": "section",
# 				"fields": [
# 					{
# 						"type": "mrkdwn",
# 						"text": "*Nivel:*\n" + salida_nivel
# 					},
# 					{
# 						"type": "mrkdwn",
# 						"text": "*Duración:*\n" + duracion_salida
# 					}
# 				]
# 			},
# 			{
# 				"type": "image",
# 				"title": {
# 					"type": "plain_text",
# 					"text": "foto aleatoria...."
# 				},
# 				"image_url": "https://drive.google.com/uc?id=1BS6VL5onsxbfHNQWMqEBsqKHuHTmiAAO",
# 				"alt_text": "Example Image"
# 			},
# 			{
# 				"type": "divider"
# 			},
# 			{
# 				"type": "actions",
# 				"block_id": "voyNoVoy",
# 				"elements": [
# 					{
# 						"type": "button",
# 						"text": {
# 							"type": "plain_text",
# 							"text": "VOY"
# 						},
# 						"style": "primary",
# 						"value": "click_voy"
# 					},
# 					{
# 						"type": "button",
# 						"text": {
# 							"type": "plain_text",
# 							"text": "NO ES SEGURO"
# 						},
# 						"style": "danger",
# 						"value": "click_noSeguro"
# 					}
# 				]
# 			},
# 			{
# 				"type": "divider"
# 			}
#       ]    
#     )

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
							"label": {"type": "plain_text","text": "La ruta"},
							"element": {
								"type": "plain_text_input",
								"action_id": "plain_input",
								"placeholder": {"type": "plain_text","text": "Describa la ruta en terminos generales"}
							}
						},
						{
							"type": "section",
							"block_id": "input002",
							"text": {"type": "mrkdwn","text": "Nivel"},
							"accessory": {
								"action_id": "action002","type": "static_select",
								"placeholder": {"type": "plain_text","text": "Seleccione"},
									"options": [
										{"text": {"type": "plain_text","text": "nivel bajo"},"value": "value-0"},
										{"text": {"type": "plain_text","text": "nivel medio"},"value": "value-1"},
										{"text": {"type": "plain_text","text": "nivel alto"},"value": "value-2"},
										{"text": {"type": "plain_text","text": "nivel muy alto"},"value": "value-3"},
										{"text": {"type": "plain_text","text": "nivel Chema Camacho!!"},"value": "value-4"}
									]
							}
						},						
						{
							"type": "section",
							"block_id": "input003",
							"text": {"type": "mrkdwn","text": "Tiempo estimado"	},
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
      {"type": "section", "text": {"type": "mrkdwn","text": "*/fstbot* tri noticias"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*/fstbot* quien es juanjo ?"}},
      {"type": "section", "text": {"type": "mrkdwn","text": "*/fstbot* horario gym"}},
	  {"type": "section", "text": {"type": "mrkdwn","text": "*/fstbot* salida bici"}}
      ])
    # response to Slack after processing is finished
    message = {"text": txtBye}
    res = requests.post(callback_id, json=message)
    print('respuesta:',res)

# def quienesjuano(channel_id,user,web_client,thread_ts):
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

# def horariosFitness(channel_id,user,web_client,thread_ts):
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

# def triNews(ssl_context,channel_id,user,web_client,thread_ts):
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
