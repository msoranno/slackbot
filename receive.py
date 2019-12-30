import os
from flask import Flask, request, Response, jsonify, json


app = Flask(__name__)

#SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/slack', methods=['POST'])
def inbound():
	message_action = json.loads(request.form["payload"])
	message_type = message_action["type"]
	trigger_id = message_action["trigger_id"]
	user_id = message_action["user"]["name"]
	callback_id = message_action["callback_id"]
	trigger_id = message_action["trigger_id"]
	print(message_type, user_id,callback_id,trigger_id)
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