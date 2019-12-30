import os
from flask import Flask, request, Response, jsonify, json
import slack
import certifi
import ssl as ssl_lib

app = Flask(__name__)
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'],ssl=ssl_context)


@app.route('/slack', methods=['POST'])
def inbound():
	message_action = json.loads(request.form["payload"])
	message_type = message_action["type"]
	trigger_id = message_action["trigger_id"]
	user_id = message_action["user"]["name"]
	callback_id = message_action["callback_id"]
	trigger_id = message_action["trigger_id"]
	print(message_type, user_id,callback_id,trigger_id)
	open_dialog = client.views_open(
				trigger_id = trigger_id,
				view={
				    "type": "modal",
				    "callback_id": callback_id,
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

	print(open_dialog)	
	return (message_action)
	#print(data)
	# if request.form.get('token') == SLACK_WEBHOOK_SECRET:
	#     channel = request.form.get('channel_name')
	#     username = request.form.get('user_name')
	#     text = request.form.get('text')
	#     inbound_message = username + " in " + channel + " says: " + text
	#     print(inbound_message)
	#return Response(), 200
	


@app.route('/', methods=['GET'])
def test():
	return Response('It works!')


if __name__ == "__main__":
	app.run(debug=True)