from telegram import InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler,  Updater , MessageHandler , Filters
import datetime
import json
import os
import re
import urllib.request
from datetime import date , datetime , timedelta
from threading import Thread
import pandas as pd
import requests
import telegram
import telegram.ext.callbackcontext

class Application:
    def __init__(self, pipe=None):
        self.itemList = {}

    def run(self):
        token = self.read_key('./token.json')
        self.updater = Updater(token=token)
        print(self.updater)
        print(self.updater.is_idle)
        print(self.updater.running)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.get_message))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.select_button))
        'self.updater.dispatcher.add_handler(MessageHandler(Filters.status_update, self.empty_message))'
        # 명령어 받길 기다리는 
        self.updater.start_polling()
        # 봇 켜진상태로 대기
        self.updater.idle()

    # 파이썬 봇 토큰 키
    def read_key(self, path):
        with open(path, 'r') as r:
            content = json.load(r)
        return content['key']

    # token.json 에서 네이버 api 키값 불러오는 메서드
    def Naver_Key(self, path):
        with open(path, 'r') as r:
            content = json.load(r)
        ListAPI = [content['naverKey'], content['naverpass']]
        return ListAPI

    # naver api 호출
    def NaverAPI(self, SearchTxT):
        """
        https://developers.naver.com/docs/common/openapiguide/
        """
        service_key = self.Naver_Key('./token.json')
        client_id = service_key[0]  # Your client_id
        client_secret = service_key[1]  # Your client_secret
        encText = urllib.parse.quote(SearchTxT)
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            res = response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
        data = json.loads(res)
        for head in data["items"]:
            return head
            '''return head["link"]'''

    def get_message(self, update, context):
        chat_id = update.effective_message.chat.id
        text = update.effective_message.text
        id = update.effective_user.id

        if text == '/start':
            context.bot.send_message(chat_id=chat_id, text=f'안녕하세요! 저는 댕댕이와 함께 갈 수 있는 카페를 추천해주는 챗봇입니다. 원하시는 검색 방법을 선택해 주세요')
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('카페검색', callback_data='op')]
               
            ])
            context.bot.send_message(chat_id=chat_id, text='카페검색 리스트',
                                     reply_markup=reply_markup)

        else:
            txtmemo = f'말씀을 이해하지못했습니다. 다시 말씀해주세요.'
            context.bot.send_message(text=txtmemo, chat_id=chat_id)

    def get_Tagkey(self, val):
        values = list(self.itemList.values())
        for keys in values[0]:
            result =(values[0])[keys]
            if val == result:
                return keys
        return "There is no such tag Key"

    def select_button(self, update, context):
        self.itemList = (pd.read_excel("cafelist.xlsx")).to_dict()
        values = list(self.itemList.values())

        self.isdepoit = False
        data = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        tagindex = self.get_Tagkey(data)

        # 추천메뉴 화면으로 넘어가기위해 아이템 id값 가져오는 로직
        # 메인메뉴
        if data == 'op':
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('테마별로 검색', callback_data='op1')],
                [InlineKeyboardButton('소형견/대형견으로 검색', callback_data='op2')],
                [InlineKeyboardButton('실내/실외 테라스로 검색', callback_data='op3')],
            ])
            context.bot.send_message(chat_id=chat_id, text='카페를 찾는 중이신가요? 제가 도와드릴게요! 검색 방법을 선택해주세요',
                                     reply_markup=reply_markup)

        elif data=='op1':
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('분위기 좋은(사진 찍기 좋은)', callback_data='op11')],
                [InlineKeyboardButton('디저트가 맛있는', callback_data='op12')],
                [InlineKeyboardButton('커피가 맛있는', callback_data='op13')],
                [InlineKeyboardButton('이색적인', callback_data='op14')],
                [InlineKeyboardButton('강아지 음료가 있는', callback_data='op15')],
            ])
            context.bot.send_message(chat_id=chat_id, text='원하시는 테마를 입력해주세요',
                                     reply_markup=reply_markup)

        elif data == 'op3':
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('분위기 좋은(사진 찍기 좋은)', callback_data='op11')],
                [InlineKeyboardButton('디저트가 맛있는', callback_data='op12')],
                [InlineKeyboardButton('커피가 맛있는', callback_data='op13')],
                [InlineKeyboardButton('이색적인', callback_data='op14')],
                [InlineKeyboardButton('강아지 음료가 있는', callback_data='op15')],
            ])
            context.bot.send_message(chat_id=chat_id, text='원하시는 테마를 입력해주세요',
                                     reply_markup=reply_markup)

        elif data=='op2':
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('소형견', callback_data='op11')],
                [InlineKeyboardButton('대형견', callback_data='op12')],
            ])
            context.bot.send_message(chat_id=chat_id, text='소형견인지 대형견인지 입력해 주세요',
                                     reply_markup=reply_markup)

        elif data == 'op3':
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('실내', callback_data='op11')],
                [InlineKeyboardButton('실외 테라스', callback_data='op12')],
            ])
            context.bot.send_message(chat_id=chat_id, text='실내/실외 테라스 인지 입력해주세요',
                                     reply_markup=reply_markup)

        elif data == 'op11':
            self.Product_List(context,chat_id,values)

        elif data == 'op12':
            self.Product_List(context,chat_id,values)

        elif data == 'op13':
            self.Product_List(context,chat_id,values)

        elif data == 'op14':
            self.Product_List(context,chat_id,values)

        elif data == 'op15':
            self.Product_List(context,chat_id,values)
        elif data ==(values[0])[tagindex]:
            ments =f"카페명 :{(values[0])[tagindex]} \r\n"
            URL = self.NaverAPI((values[0])[tagindex])
            ments += f"description : {URL['description']} \r\n"
            ments +=f"link : {URL['link']} "
            context.bot.send_message(chat_id=chat_id, text=ments)

            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('네', callback_data='cuyes')],
                [InlineKeyboardButton('아니요', callback_data='cuno')],
            ])
            context.bot.send_message(chat_id=chat_id, text="혹시 추가로 고객님이 가보신 곳 중에서 추천 제의해 주실만한 카페가 있을까요?", reply_markup=reply_markup)

        elif data == 'cuyes':
                  context.bot.send_message(chat_id=chat_id, text='yes')

        elif data == 'cuno':
                 context.bot.send_message(chat_id=chat_id, text='종료')

    def Product_List(self,context, chat_id,itemlist):
        show_list = []
        cnt=0
        ment ='입력하신 테마로 검색된 카페는 다음과 같습니다. \r\n'
        for keys in itemlist[0]:
            cnt += 1
            ment +=f'{cnt}. \r\n {(itemlist[0])[keys]} / {(itemlist[1])[keys]} / {(itemlist[2])[keys]} \r\n'
            show_list.append(InlineKeyboardButton(f'{(itemlist[0])[keys]}',
                                                  callback_data=(itemlist[0])[keys]))

        # 버튼 갯수에따라 구성을 달리해주는 기능
        reply_markup = InlineKeyboardMarkup(self.build_menu(show_list, len(show_list) - 1))  # make markup
        # 버튼 출력시키는 부분
        context.bot.send_message(chat_id=chat_id, text=ment, reply_markup=reply_markup)
        
    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        n_cols = 1
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def empty_message(self, update, context):
        if update.message.new_chat_members:
            for new_member in update.message.new_chat_members:
                # Bot was added to a group chat
                if new_member.username != self.BOTNAME:
                    return self.welcome(update, context, new_member)


