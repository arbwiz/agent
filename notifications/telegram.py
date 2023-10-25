import requests
import json
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 6480489284
def send_telegram_message(message):
    send_telegram_message_complex(message,
                                  os.environ['TELEGRAM_CHANNEL_ID'],
                                  "6613908503:AAGLsuazZhBmwHbPCEZzx-tJGQHLOtEcZy0")


def send_telegram_message_complex(message,
                                  chat_id: str,
                                  api_key: str,
                                  proxy_username: str = None,
                                  proxy_password: str = None,
                                  proxy_url: str = None):
    proxies = None
    if proxy_url is not None:
        proxies = {
            'https': f'http://{proxy_username}:{proxy_password}@{proxy_url}',
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_url}'
        }

    for surebet in message['surebets']:
        for outcome in surebet['outcomes']:
            del outcome['otherBookies']

        message = json.dumps(surebet, indent=1)

        headers = {'Content-Type': 'application/json',
                   'Proxy-Authorization': 'Basic base64'}
        data_dict = {'chat_id': chat_id,
                     'text': message,
                     'parse_mode': 'HTML',
                     'disable_notification': True}

        data = json.dumps(data_dict)
        url = f'https://api.telegram.org/bot{api_key}/sendMessage'
        response = requests.post(url,
                                 data=data,
                                 headers=headers,
                                 proxies=proxies,
                                 verify=False)
    return response

