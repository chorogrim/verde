import os
import json
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import pandas as pd

# 키 읽어오기
def read_key(path):
    with open(path, 'r') as r:
        content = json.load(r)
    return content['key']

# 봇 생성
def generate_bot(token):
    return telegram.Bot(token=token)

# 봇 정보
def get_info(bot):
    return bot.getMe()


# 업데이트 된 내용
def get_updates(bot):
    return [eval(str(u)) for u in bot.getUpdates()]

# 최근 채팅한 유저 아이디
def get_recent_user_id(bot):
    return bot.getUpdates()[-1].message.chat.id

# 메시지 보내기
def send_message(bot, target_id, text):
    bot.sendMessage(chat_id=target_id, text=text)


def get_reply(message):
    return f"'{message}'를 보냈습니다."




def message_fn(update, context, save=True, path='./result.csv', botid='5059790606', botname='python7869'):
    m = update.message.text
    reply_message = get_reply(m)

    update.message.reply_text(reply_message)

    if save:
        data = {'id': [update.update_id],
                'name': [update.message.chat.first_name + " " + update.message.chat.last_name],
                'text': [update.message.text],
                }

        data['text'].append(reply_message)
        data['id'].append(botid)
        data['name'].append(botname)


        data = pd.DataFrame(data)
        save_updates(path,data)


def save_updates(path, data):
    df = pd.DataFrame({})
    if os.path.isfile(path):
#        df = pd.read_excel(path)
        df = pd.read_csv(path, encoding='utf-8')
    df = df.append(data, ignore_index=True)
#    df.to_excel(path, encoding='utf-8', index=False)
    df.to_csv(path, encoding='utf-8', index=False)


def update_and_reply(token, message_fn):
    updater = Updater(token, use_context=True)
    # 메시지 처리
    message_handler = MessageHandler(Filters.text, message_fn)
    # 핸들러 생성
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling(timeout=3, drop_pending_updates=True)
    updater.idle()


def main():
    TOKEN = 'token.json'
    token = read_key(TOKEN)
    bot = generate_bot(token)
    update_and_reply(token=token, message_fn=message_fn)


if __name__ == '__main__':
    main()
