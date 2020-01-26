from pprint import pprint

import jwt
import smooch
from flask import Flask, render_template
from flask import request
from smooch.rest import ApiException

# Config
from app.cal_setup import get_calendar_service
from dbOperations import push_db

KEY_ID = 'app_5e2cf154fda5e4000fb5d20d'
SECRET = 'pvqyRcu7WABj9Jo9mcr0xEW6Ck2wwBK0hLVmKeeBedvkb7vn5YwHdPP_3IHm_wCSnVpxhCaBqriMhHJq_Iocdw'

token_bytes = jwt.encode(
    {'scope': 'app'}, SECRET, algorithm='HS256', headers={'kid': KEY_ID})
token = token_bytes.decode('utf-8')

smooch.configuration.api_key['Authorization'] = token
smooch.configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = smooch.ConversationApi()

# Server http://flask.pocoo.org/docs/0.12/quickstart/
app = Flask(__name__)
COMM_INFO = {
    "messenger": ["5e2c892818768b000f696b4b", "faabcb43ffe3dbf868348792"],
    "whatsapp": ["5e2c892818768b000f696b4b", "15391ed89a11661282ef9b26"],
    "telegram": ["5e2c892818768b000f696b4b", "0f226e3cc9b63c1db2a10a3f"]

}


def smooch_send_message(app_id, app_user_id, message):
    try:
        message_post_body = smooch.MessagePost(
            'appMaker', 'text', text=message)
        api_response = api_instance.post_message(
            app_id, app_user_id, message_post_body)
        print('API RESPONSE:')
        pprint(api_response)
    except ApiException as e:
        print('API ERROR: %s\n' % e)


@app.route("/", methods=["GET"])
def hello():
    return "Server is running good!!"


@app.route("/user_form", methods=["POST", "GET"])
def display_form():
    return render_template("user_form.html"), 200


@app.route("/db_update", methods=["POST", "GET"])
def db_update():
    form_data = request.form
    name = form_data.get("name")
    username = form_data.get("username")
    com_preference = form_data.get("communication_preference")
    comm_info = COMM_INFO.get(com_preference.lower())
    answer_1 = form_data.get("ques_1")
    answer_2 = form_data.get("ques_2")
    answer_3 = form_data.get("ques_3")
    answer_4 = form_data.get("ques_4")
    answer_5 = form_data.get("ques_5")
    answer_6 = form_data.get("ques_6")
    quiz_metrics = f"{answer_1},{answer_2},{answer_3},{answer_4},{answer_5},{answer_6}"
    push_db(username=username, name=name, zendesk_app_id=comm_info[0], zendesk_app_uid=comm_info[1],
            quiz_metrics=quiz_metrics, )
    get_calendar_service(username)
    return "Success!!"


# Expose /messages endpoint to capture webhooks
# https://docs.smooch.io/rest/#webhooks-payload
@app.route('/messages', methods=['POST', 'GET'])
def messages():
    req = request.get_json()
    print('webhook PAYLOAD:')
    pprint(req)

    app_id = req.get('app', {}).get('_id')
    app_user_id = req.get('appUser', {}).get('_id')
    # Call REST API to send message https://docs.smooch.io/rest/#post-message
    if req.get('trigger') == 'message:appUser':
        try:
            message_post_body = smooch.MessagePost(
                'appMaker', 'text', text='Live long and prosper')
            api_response = api_instance.post_message(
                app_id, app_user_id, message_post_body)
            print('API RESPONSE:')
            pprint(api_response)
        except ApiException as e:
            print('API ERROR: %s\n' % e)
    return '', 204


@app.route('/send_msg', methods=["POST", "GET"])
def send_msg():
    recieved_msg = request.args["msg"]
    for user in COMM_INFO:
        smooch_send_message(app_id=COMM_INFO[user][0], app_user_id=COMM_INFO[user][1], message=recieved_msg)
    return "Success!!"


@app.route("/ranked_events", methods=["GET", "POST"])
def display_ranked_events():
    ranked_events = request.args["ranked_events"]
    return render_template('testcases.html', cases=ranked_events, title="Test Cases")


@app.route("/info", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        print(request.form)
        test = request.form["checks"]

        return str(test)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
