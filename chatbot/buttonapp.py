# -*- coding: utf-8 -*-

import os
import requests
from flask import Flask, request, Response

API_KEY = '5025918465:AAEik4LzCoJlvVO4UaKfEIy6L5mdP_7CQSA'

app = Flask(__name__)

    
def parse_message(data):
    chat_id = data['message']['chat']['id']
    msg = data['message']['text']
    
    return chat_id, msg


def send_message(chat_id, text='bla-bla-bla'):
    """
    Chat-id 와 text를 변수로 받아 메세지를 보내주는데
    params 안에 키보드를 설정해서 같이 보내주는 방법
    
    https://core.telegram.org/bots/api#keyboardbutton
    """
    # sendMessage URL
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    keyboard = {                                        # Keyboard 형식
            'keyboard': [[{
                    'text': '버튼1'
                        },
                    {'text': '버튼2'
                        }],
                [{'text': '버튼3'},
                 {'text': '버튼4'}]
                    ],
            'one_time_keyboard': True
            }
        
    if text == '버튼1':                            # 사용자가 button_1 이라고 응답하면 ~
        keyboard = {
            'keyboard':[[{'text': '버튼1을 누르셨습니다.'}]],
            'one_time_keyboard' : True
            }
        params = {'chat_id':chat_id, 'text': text, 'reply_markup': keyboard}
        requests.post(url, json=params)
        return 0 
    
    # 변수들을 딕셔너리 형식으로 묶음
    params = {'chat_id': chat_id, 'text': text, 'reply_markup': keyboard}
    
    # Url 에 params 를 json 형식으로 변환하여 전송
    # 메세지를 전송하는 부분
    requests.post(url, json=params)
    
    return 0


# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()

        chat_id, msg = parse_message(message)
        send_message(chat_id, msg)
        
        return Response('ok', status=200)
    else:
        return 'Hello World!'


# Python 에서는 실행시킬때 __name__ 이라는 변수에
# __main__ 이라는 값이 할당
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
