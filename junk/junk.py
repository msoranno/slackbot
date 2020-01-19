#
#
# un sitio donde meter funciones que nos ayuden en un futuro
#
#
#

# def proponerSalidaBici(channel_id,user,web_client,callback_id,salida_nivel, duracion_salida, texto_ruta):
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
# 				"image_url": "https://drive.google.com/uc?id="+ FOTOSDRIVE[str(randrange(len(FOTOSDRIVE)))],
# 				"alt_text": "Example Image"
# 			},
# 			{
# 				"type": "divider"
# 			}
#       ]    
#     )


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