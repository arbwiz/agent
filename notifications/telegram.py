import requests
import json
#6480489284
def send_telegram_message(message):
    send_telegram_message_complex(message,
                          "6480489284",
                          "6613908503:AAGLsuazZhBmwHbPCEZzx-tJGQHLOtEcZy0")

def send_telegram_message_complex(message: str,
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