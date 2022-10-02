
import time

from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import config
from handler import send_alert, send_message_alert
import logging


app = Flask(__name__)

cond_a = False
cond_b = False

def get_timestamp():
    timestamp = time.strftime("%Y-%m-%d %X")
    return timestamp

@app.route("/webhook1", methods=["POST"])
def webhook1():
    try:
        global cond_a , cond_b
        if request.method == "POST":
            data = request.get_json()
            key = data["key"]
            if key == config.sec_key:
                if data['alert_key'] == 'a':
                    cond_a = True
                    print(get_timestamp() ,"Alert Received For A")

                    if(cond_b) :
                        send_message_alert(data)
                        print(get_timestamp() ,"Alert Received & both conditions met! alert sent because of a")
                elif data['alert_key'] == 'b':
                    cond_b = True
                    logging.info( "Alert Received For B")
                    print(get_timestamp() ,"Alert Received For B")
                    if(cond_a) :
                        send_message_alert(data)
                        print(get_timestamp(), "Alert Received & both conditions met! alert sent because of b")

                elif data['alert_key'] == 'untrigger_a':
                    cond_a = False
                    print( "Alert Received For Untriggering A")

                elif data['alert_key'] == 'untrigger_b':
                    cond_b = False
                    print( "Alert Received For Untriggering B")
                else:
                    logging.info( "Not valid alert_key")
                    print(get_timestamp(), 'not a valid alert_key')
                    return "Bad alert" , 401

                return "Sent alert", 200

            else:
                print("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Master Key)")
                return "Refused alert", 400

    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        if request.method == "POST":
            data = request.get_json()
            key = data["key"]
            if key == config.sec_key:
                print(get_timestamp(), "Alert Received & Sent!")
                send_alert(data)
                return "Sent alert", 200

            else:
                print("[X]", get_timestamp(), "Alert Received & Refused! (Wrong Key)")
                return "Refused alert", 400

    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400
@app.route("/")
def hello():
    return '<h1>Your Bot Is alive</h1>'

@app.route("/whatsapp_bot",methods =["POST"])
def whatsapp_bot():
    try:
        user_msg = request.values.get('Body', '').lower()

        # creating object of MessagingResponse
        response = MessagingResponse()
        if user_msg in ['hello','hi']:
            response.message(f"Hi this is ilyes's BOT !\nHow can I help You ?")
        else:
            response.message(f"Sorry I didn't understand that !")



        data = {"key": "","telegram": "-768784032","msg": f"This message is sent: {user_msg}"}
        send_alert(data)
        return str(response) ,200

    except Exception as e:
        print("[X]", get_timestamp(), "Error:\n>", e)
        return "Error", 400



if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5050)
