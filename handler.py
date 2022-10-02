
from telegram import Bot
import config
import urllib3


def send_alert(data):
    msg = data["msg"]#.encode("latin-1", "backslashreplace").decode("unicode_escape")
    if config.send_telegram_alerts:
        tg_bot = Bot(token=config.tg_token)

        try:
            tg_bot.sendMessage(
                data["telegram"],
                msg,
                parse_mode="MARKDOWN",
            )
        except KeyError:
            tg_bot.sendMessage(
                config.channel,
                msg,
                parse_mode="MARKDOWN",
            )
        except Exception as e:
            print("[X] Telegram Error:\n>", e)

#the data format would be : data = {'key': '' , 'alert_key':'a or b or untrigger_a or untrigger_b' , 'alertid': 'c8232f58-dea2-4c33-8305-3591b80d9120'}
def send_message_alert(data):
    url = 'http://ilyeshaddad337.pythonanywhere.com/webhook'
    payload= {"key": "",
          "telegram": "-768784032",
          "msg": str(data['alertid'])}

    try:
        http = urllib3.PoolManager()
        r = http.request('POST',url,fields=payload)
        #r = requests.post(url,json=payload)
        print('sent')
    except Exception as e:
        print(e, ' not sent')



