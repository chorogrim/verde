# -*- coding: utf-8 -*-
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
from telegram import InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler,  Updater , MessageHandler , Filters

vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

class Application:
    def __init__(self, pipe=None):
        # 매니저와 연결하기 위한 pipe
        self.pipe = pipe
        self.userCnt=0
        self.money = 0
        self.totalSellMoney = 0
        self.BOTNAME = 'python7869'
        self.isdepoit = False
        self.itemList = {}
        self.productList = {}
        self.CartList = {}
        self.userData =[]
        self.sellList={}
        self.weatherState =''
        self.updater = None
        # ChatbotManager 와 통신하기 위한 thread 생성
        self.watchdog_thread = Thread(target=self.watchdog)
        self.watchdog_thread.start()

    def run(self):
        # manager 에게 메시지를 보냄
        # run 은 watchdog 에 응답하는 부분
        if self.pipe:
            self.pipe.send('pong')
        self.itemSet()
        self.weatherState = self.GongLogic()
        token = self.read_key('./token.json')
        self.updater = Updater(token=token)
        print(self.updater)
        print(self.updater.is_idle)
        print(self.updater.running)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.get_message))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.select_button))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.status_update, self.empty_message))
        # 명령어 받길 기다림
        self.updater.start_polling()
        # 봇 켜진상태로 대기
        self.updater.idle()
    
    # 파이썬 봇 토큰 키
    def read_key(self, path):
        with open(path, 'r') as r:
            content = json.load(r)
        return content['key']
    
    # 공공 데이터 날씨 가져오는 메서드
    def GongLogic(self):
        def Gongread_key(path):
            # 파이썬 봇 토큰 키
            with open(path, 'r') as r:
                content = json.load(r)
            return content['gongongKey']
        service_key = Gongread_key('./token.json')
        now = datetime.now()
        nx = "62"
        ny = "120"

        # 지역의 날씨 데이터 이용 (동네 좌표 값: nx, ny)
        # nx = "62" - 용인 기흥 위도 좌표
        # ny = "120" - 용인 기흥 경도 좌표

        # 오늘
        today = datetime.today()  # 현재 지역 날짜 반환
        today_date = today.strftime("%Y%m%d")  # 오늘의 날짜 (연도/월/일 반환)
        print('오늘의 날짜는', today_date)

        # 어제
        yesterday = date.today() - timedelta(days=1)
        yesterday_date = yesterday.strftime('%Y%m%d')
        print('어제의 날짜는', yesterday_date)

        if now.hour < 2 or (now.hour == 2 and now.minute <= 10):  # 0시~2시 10분 사이
            base_date = yesterday_date  # 구하고자 하는 날짜가 어제의 날짜
            base_time = "2300"
        elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):  # 2시 11분~5시 10분 사이
            base_date = today_date
            base_time = "0200"
        elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):  # 5시 11분~8시 10분 사이
            base_date = today_date
            base_time = "0500"
        elif now.hour <= 11 or now.minute <= 10:  # 8시 11분~11시 10분 사이
            base_date = today_date
            base_time = "0800"
        elif now.hour < 14 or (now.hour == 14 and now.minute <= 10):  # 11시 11분~14시 10분 사이
            base_date = today_date
            base_time = "1100"
        elif now.hour < 17 or (now.hour == 17 and now.minute <= 10):  # 14시 11분~17시 10분 사이
            base_date = today_date
            base_time = "1400"
        elif now.hour < 20 or (now.hour == 20 and now.minute <= 10):  # 17시 11분~20시 10분 사이
            base_date = today_date
            base_time = "1700"
        elif now.hour < 23 or (now.hour == 23 and now.minute <= 10):  # 20시 11분~23시 10분 사이
            base_date = today_date
            base_time = "2000"
        else:  # 23시 11분~23시 59분
            base_date = today_date
            base_time = "2300"

        payload = "serviceKey=" + service_key + "&" + \
                  "dataType=json" + "&" + \
                  "base_date=" + base_date + "&" + \
                  "base_time=" + base_time + "&" + \
                  "nx=" + nx + "&" + \
                  "ny=" + ny

        # 값 요청 (웹 브라우저 서버에서 요청 - url주소 )
        res = requests.get(vilage_weather_url + payload)
        # items 로 요청한 값 받아오는 로직
        print(res.json())
        items = res.json().get('response').get('body').get('items')
        data = dict()
        data['date'] = base_date
        weather_data = dict()

        for item in items['item']:
            if item['category'] == 'T3H':
                weather_data['tmp'] = item['fcstValue']
            if item['category'] == 'PTY':
                weather_code = item['fcstValue']
                if weather_code == '1':  # 비
                    weather_state = 'ra'
                elif weather_code == '2':  # 비,눈
                    weather_state = 'rs'
                elif weather_code == '3':  # 눈
                    weather_state = 'sn'
                elif weather_code == '4':  # 소나기
                    weather_state = 'so'
                else:
                    weather_state = 'su'  # 맑음
                weather_data['code'] = weather_code
                weather_data['state'] = weather_state
        data['weather'] = weather_data
        state = data['weather']['state']
        return state

    # msg.json 에서 상황별 메시지 관련 모음 출력을 위한 메서드
    def Ment_Key(self,ment):
        with open('./msg.json', 'r', encoding='utf-8') as r:
            content = json.load(r)
        return content[ment]

    # user.json 에서 유저 데이터 읽기 메서드
    def User_Read(self):
        with open('./user.json', 'r', encoding='utf-8') as r:
            content = json.load(r)
        return content

    # user.json 에서 유저 데이터 수정 메서드
    def User_Write(self, txt):
        with open('./user.json', 'w', encoding='utf-8') as make_file:
            json.dump(txt, make_file, indent="\t", ensure_ascii = False)

    # token.json 에서 네이버 api 키값 불러오는 메서드
    def Naver_Key(self, path):
        with open(path, 'r') as r:
            content = json.load(r)
        ListAPI=[content['naverKey'],content['naverpass']]
        return ListAPI

    # naver api 호출
    def NaverAPI(self,SearchTxT):
        """
        https://developers.naver.com/docs/common/openapiguide/
        """
        service_key = self.Naver_Key('./token.json')
        client_id = service_key[0]  # Your client_id
        client_secret = service_key[1]  # Your client_secret
        encText = urllib.parse.quote(SearchTxT)
        url = "https://openapi.naver.com/v1/search/encyc?query=" + encText
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
            return head["link"]

    # 메인 메뉴 버튼 생성 및 메인 메뉴 함수
    def menu(self, context, chat_id,userCnt):
        answer_text = f"반가워요😄 오늘 날씨에 따라\n음료를 추천해주는 자판기 봇입니다\n사용 방법을 보려면 도움말 버튼을 눌러주세요"

        # 방문 횟수가 적은 손님용
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('도움말', callback_data='help')],
            [InlineKeyboardButton('돈넣기', callback_data='deposit')],
            [InlineKeyboardButton('메뉴보기', callback_data='List')],
            [InlineKeyboardButton('주문하기', callback_data='Order')],
            [InlineKeyboardButton('평가하기', callback_data='evaluate')],
            [InlineKeyboardButton('종료하기', callback_data='finish')]
        ])

        # 방문 횟수가 10회 넘은 단골 손님용
        reply_markup2 = InlineKeyboardMarkup([
            [InlineKeyboardButton('돈넣기', callback_data='deposit')],
            [InlineKeyboardButton('메뉴보기', callback_data='List')],
            [InlineKeyboardButton('주문하기', callback_data='Order')],
            [InlineKeyboardButton('평가하기', callback_data='evaluate')],
            [InlineKeyboardButton('종료하기', callback_data='finish')]
        ])
        if userCnt <= 9:
            context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup2)

    def menu_link(self, context, chat_id):
        answer_text = self.Ment_Key('menu_link_msg')
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('메뉴보기', callback_data='menu')]
        ])
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

    # 버튼 갯수에 따라 구성을 달리해주는 기능
    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        n_cols = 1
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    # 추천 메뉴   
    def menuProduct_List(self, context, chat_id):
        answer_text = self.Ment_Key('menuProduct_List_msg')
        show_list = []
        # dict -> list 변환 -> for문과 indext 통해 데이터 가져오는 로직
        # 아이템 데이터 전부 show_list dict에 담는 로직
        # 추천 메뉴가 같은 경우 아이템 id 값과 추천 메뉴 값과 일치하는 것만 출력
        values = list(self.itemList.values())
        for keys in values[0]:
            result = str((values[0])[keys])
            weather = str((values[4])[keys])
            if  self.weatherState == weather:
                show_list.append(InlineKeyboardButton(f'{(values[1])[keys]}\n({(values[2])[keys]}원)',
                                                      callback_data=(values[3])[keys]))

        # 마지막 버튼은 이전 단계 버튼 담기 위한 로직
        show_list.append(InlineKeyboardButton("뒤로가기", callback_data="menu"))  # add cancel button
        # 버튼 갯수에따라 구성을 달리해주는 기능
        reply_markup = InlineKeyboardMarkup(self.build_menu(show_list, len(show_list) - 1))  # make markup
        # 버튼 출력시키는 부분
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

    # 장바구니 기능은 들어가있지만, 담기지 않으면 '장바구니가 텅텅비어있네요!' 하고 알려주는 로직
    def addCart(self, index, context, chat_id,json_data,id):
        # 선택한 추천메뉴 버튼 클릭시 클릭한 아이템 cartList 컬렉션에 담기위한 로직
        # totalmoney로 결제해야 할 금액이 더해짐
        values = list(self.itemList.values())
        for keys in values[3]:
            result = str((values[3])[keys])
            if index == result:
                json_data[str(id)]['CartList'][(values[1])[keys]] = (values[2])[keys]
                json_data[str(id)]['totalSellMoney'] += (values[2])[keys]
                self.User_Write(json_data)
        self.menuProduct_List(context, chat_id)

    # 봇이 그룹에 속해있을 때 유저가 그룹에 들어오면 웰컴 메서드 호출
    def welcome(self, update, context, new_member):
        message = update.message
        chat_id = message.chat.id
        answer_text = self.msg['menu_msg']
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('시작', callback_data='menu')],
            [InlineKeyboardButton('도움말', callback_data='help')],
        ])
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

    # 유저 -> 봇으로 메시지 날릴 때 호출
    def get_message(self, update, context):
        chat_id = update.effective_message.chat.id
        text = update.effective_message.text
        id =update.effective_user.id
        json_data = self.User_Read()
        if text == '/start':
            self.sellList.clear()
            self.Usercnt = self.UserSet(id)
            if self.weatherState == 'rs':
                context.bot.send_message(chat_id=chat_id, text='오늘은 비와 눈이 옵니다🌨️')
            elif self.weatherState == 'ra':
                context.bot.send_message(chat_id=chat_id, text='오늘은 비가 옵니다🌧️')
            elif self.weatherState == 'su':
                context.bot.send_message(chat_id=chat_id, text='오늘은 맑습니다☀️')
            elif self.weatherState == 'sn':
                context.bot.send_message(chat_id=chat_id, text='오늘은 눈이 옵니다❄️')
            elif self.weatherState == 'so':
                context.bot.send_message(chat_id=chat_id, text='오늘은 소나기가 옵니다☔')
            self.menu(context, chat_id,self.Usercnt)
        elif self.isdepoit:
            try:
                won = re.sub(r'[^0-9]', '', text)
                json_data[str(id)]['money'] += int(won)
                answer_text = f"{int(won):,}원을 넣었습니다."
                self.User_Write(json_data)
                self.isdepoit = False
                # 돈을 추가하는 기능
                context.bot.send_message(chat_id=chat_id, text=answer_text)
                self.menu(context, chat_id, self.Usercnt)
            except:
                answer_text = self.Ment_Key('order_try')
                context.bot.send_message(chat_id=chat_id, text=answer_text)
        else:
            txtmemo = f'말씀을 이해하지못했습니다. 다시 말씀해주세요.'
            context.bot.send_message(text=txtmemo, chat_id=chat_id)
            self.menu(context, chat_id, self.Usercnt)
        # 돈넣기 활성화 되어있을때만 금액 입력시 작동

    # 메시지 출력하기 위한 함수. 메시지 핸들러에 의해 호출
    def empty_message(self, update, context):
        if update.message.new_chat_members:
            for new_member in update.message.new_chat_members:
                # Bot was added to a group chat
                if new_member.username != self.BOTNAME:
                    return self.welcome(update, context, new_member)

    # 클릭시 함수 호출
    def select_button(self, update, context):
        self.isdepoit = False
        data = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        # 추천메뉴 화면으로 넘어가기위해 아이템 id값 가져오는 로직
        index = self.get_key(data)
        tempUSerCnt = self.UsercntSearch(update.effective_user.id)
        tagindex = self.get_Tagkey(data)
        print("tag_index")
        print(tagindex)
        json_data = self.User_Read()
        id =update.effective_user.id

        # 메인메뉴
        if data == 'menu':
            self.menu(context, chat_id, tempUSerCnt)

        # 도움말
        elif data == 'help':
            answer_text = self.Ment_Key('help')
            context.bot.send_message(text=answer_text, chat_id=chat_id)
            self.menu(context, chat_id, tempUSerCnt)

        # 돈 충전하기
        elif data == 'deposit':
            self.isdepoit = True
            imsiMoney= json_data[str(id)]['money']
            print(imsiMoney)
            answer_text = answer_text = self.Ment_Key('deposit').format(money=f'{imsiMoney:,}')
            context.bot.edit_message_text(text=answer_text, chat_id=chat_id, message_id=message_id)
            self.menu(context, chat_id, tempUSerCnt)
            
        # 주문하기
        elif data == 'Order':
            if len(json_data[str(id)]['CartList']) <= 0:
                answer_text = self.Ment_Key('order_empty')
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.menu(context, chat_id, tempUSerCnt)
            elif json_data[str(id)]['money'] >= json_data[str(id)]['totalSellMoney']:
                # 장바구니 -> 담기, 취소 기능 
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton('담기', callback_data='Order_Cart')],
                    [InlineKeyboardButton('취소', callback_data='Order_Cancel')],
                ])
                context.bot.send_message(chat_id=chat_id , text="장바구니", reply_markup=markup)
            else:
                losemoney = json_data[str(id)]['totalSellMoney'] - json_data[str(id)]['money']
                answer_text = self.Ment_Key('order_fail').format(losemoney=f'{losemoney:,}')
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.User_Write(json_data)
                self.evaulate(context, chat_id, tempUSerCnt)

        # 대분류 메뉴로 넘어가는 로직
        elif data == 'List':
            self.menuProduct_List(context, chat_id)

        # 주문한 리스트를 보여주는 로직
        elif data == "Order_Cart":
            msg = f"주문한 음료 확인해드리겠습니다 \r\n"
            imsiCartList =  json_data[str(id)]['CartList']
            for cart in imsiCartList:
                msg += f"""{cart} - {  imsiCartList[cart]}\r\n"""
            context.bot.send_message(text=msg, chat_id=chat_id)
            if json_data[str(id)]['money'] >= json_data[str(id)]['totalSellMoney']:
                json_data[str(id)]['money'] -= json_data[str(id)]['totalSellMoney']
                answer_text = self.Ment_Key('order_done')
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.sellList = json_data[str(id)]['CartList']
                for x in self.sellList:
                    URL = self.NaverAPI(x)
                    context.bot.send_message(chat_id=chat_id, text=URL)
                self.User_Write(json_data)
                self.menu(context, chat_id, tempUSerCnt)

        # 평가한 다음 거스름돈과 함께 종료되는 로직
        elif data == "evaluate_star":
            answer_text = self.Ment_Key('evaluate_bot')
            context.bot.send_message(text=answer_text, chat_id=chat_id)
            answer_text = self.Ment_Key('order_finish')
            imsimoney=json_data[str(id)]['money']
            txtmoney = f'{imsimoney:,}원 거스름돈입니다.'
            context.bot.send_message(chat_id=chat_id, text=txtmoney)
            chat_user_client = update.effective_user.full_name
            pd.DataFrame({"username": [f"{chat_user_client}"],
                          "message_id": [message_id], "chatid": [chat_id], "Userid": [update.effective_user.id],
                          "exchange": [json_data[str(id)]['money']]}).to_csv(
                f'result00.csv', index=False)
            json_data[str(id)]['money'] = 0
            json_data[str(id)]['totalSellMoney'] = 0
            json_data[str(id)]['CartList'] = {}
            self.User_Write(json_data)
            context.bot.send_message(chat_id=chat_id, text=answer_text)
    
        # 주문하기 - 장바구니 -> 담기, 취소 기능 
        elif data == "Order_Pay":
            if json_data[str(id)]['money'] >= json_data[str(id)]['totalSellMoney']:
                json_data[str(id)]['money'] -= json_data[str(id)]['totalSellMoney']
                answer_text = self.Ment_Key('order_done')
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.sellList = json_data[str(id)]['CartList']
                for x in self.sellList:
                    URL = self.NaverAPI(x)
                    context.bot.send_message(chat_id=chat_id, text=URL)
                self.User_Write(json_data)
                self.menu(context, chat_id, tempUSerCnt)

        # 장바구니 -> 취소 
        elif data == "Order_Cancel":
            answer_text =self.Ment_Key('order_cancel')
            context.bot.send_message(text=answer_text, chat_id=chat_id)
            self.menuProduct_List(context, chat_id)

        # 대분류에서 소분류 넘어가는 로직
        elif data == index:
            self.menuProduct_List(index, context, chat_id)

        # 장바구니 담기위한 로직
        elif data == tagindex:
            print("태그인덱스 ", data, tagindex)
            self.addCart(tagindex, context, chat_id, json_data, id)

        # 평가하기
        elif data == 'evaluate':
            reply_markup5 = InlineKeyboardMarkup([
                [InlineKeyboardButton('★', callback_data='evaluate_star')],
                [InlineKeyboardButton('★★', callback_data='evaluate_star')],
                [InlineKeyboardButton('★★★', callback_data='evaluate_star')],
                [InlineKeyboardButton('★★★★', callback_data='evaluate_star')],
                [InlineKeyboardButton('★★★★★', callback_data='evaluate_star')]
            ])
            context.bot.send_message(chat_id=chat_id, text="평가", reply_markup=reply_markup5)

        # 종료 버튼 클릭시 거스름돈 출력 및 파일 저장(result00.csv)
        elif data == 'finish':
            # 메시지가 종료하기일 때
            answer_text = self.Ment_Key('order_finish')
            imsimoney =json_data[str(id)]['money']
            txtmoney = f'{imsimoney:,}원 거스름돈입니다.'
            context.bot.send_message(chat_id=chat_id, text=txtmoney)
            chat_user_client = update.effective_user.full_name
            pd.DataFrame({"username": [f"{chat_user_client}"],
                          "message_id": [message_id], "chatid": [chat_id], "Userid": [update.effective_user.id],
                          "exchange": [imsimoney]}).to_csv(
                f'result00.csv', index=False)
            json_data[str(id)]['money'] = 0
            json_data[str(id)]['totalSellMoney'] = 0
            json_data[str(id)]['CartList'] ={}
            self.User_Write(json_data)
            context.bot.send_message(chat_id=chat_id, text=answer_text)

    # 해당 소분류 화면으로 넘어가기 위한 로직
    def get_key(self, val):
        values = list(self.productList.values())
        for keys in values[0]:
            result = str((values[0])[keys])
            if val == result:
                return result
        return "There is no such Key"

    # 장바구니를 담기 위해 해당 소분류 아이템 키 가져오는 로직
    def get_Tagkey(self, val):
        values = list(self.itemList.values())
        for keys in values[3]:
            result = str((values[3])[keys])
            if val == result:
                return result
        return "There is no such tag Key"

    # 메뉴 아이템 데이터 엑셀 생성
    # 봇 작동시 엑셀 파일이 없을 때 생성하는 부분이라 필요
    def itemSet(self):
        bigfile = 'bigitem.xlsx'  # 예제 Textfile
        smallfile = 'item.xlsx'  # 예제 Textfile
        if os.path.isfile(bigfile):
            print("file exitst")
        else:
            df = pd.DataFrame({'id': [1, 2], '대분류': ['과자', '음료']})
            df.to_excel("bigitem.xlsx", index=False, encoding='utf-8-sig')
        if os.path.isfile(smallfile):
            print("file exitst")
        else:
            df = pd.DataFrame({'id': [2, 2, 2, 2, 2, 2], 'name': ['아메리카노', '돌체라떼', '생수', '콜라', '자몽티', '망고패션블랜디드'],
                               'price': [4200, 5800, 1000, 1800, 5500, 6200],
                               'tag': ['water1', 'water2', 'water3', 'water4', 'water5', 'water6'],
                               'weather': ['ra', 'ra', 'so', 'sn', 'rs', 'su']})
            df.to_excel("item.xlsx", index=False, encoding='utf-8-sig')
        self.itemList = (pd.read_excel("item.xlsx")).to_dict()
        self.productList = (pd.read_excel("bigitem.xlsx")).to_dict()

    # 유저 리스트(cnt - 방문 횟수, money - 유저가 넣은 금액, totalSellMoney - 잔액, CartList - 장바구니) 엑셀 생성
    def UserSet(self,id):
        Userfile = 'user.json'  # 예제 Textfile
        groupList = dict()
        file_data = dict()
        if os.path.isfile(Userfile):
            json_data =self.User_Read()
            try:
                cnts = json_data[str(id)]['cnt']
                cnts = cnts + 1
                json_data[str(id)]['cnt'] = cnts
                return json_data[str(id)]['cnt']
            except KeyError:
                file_data['cnt'] = 0
                file_data['money'] = 0
                file_data['totalSellMoney'] = 0
                file_data['CartList'] = {}
                groupList[id] = file_data
                json_data.update(groupList)
                self.User_Write(json_data)
                return 0
        else:
            file_data['cnt'] = 0
            groupList[id]=file_data
            self.User_Write(json_data)
            return 0

    # 유저 리스트 생성(cnt - 방문 횟수)
    def UsercntSearch(self, id):
        Userfile = 'user.json'  # 예제 Textfile
        if os.path.isfile(Userfile):
            json_data = self.User_Read()
            cnts = json_data[str(id)]['cnt']
            return cnts

    def watchdog(self):
        """
        ChatbotManager process 와 pipe 통신을 하는 thread method
        chatbot manaer 로부터 'ping'을 받으면 'pong'을 전송하도록 되어있음
        """
        if not self.pipe:
            return
        while True:
            # watchdog thread 는 무한 루프를 돌면서 pipe 를 감시하고 데이터가 들어올 경우에 데이터를 받아서 처리
            if self.pipe.poll():
                data = self.pipe.recv()
                if data == 'ping':
                    self.pipe.send('pong')

def main(pipe):
    """
    ChatbotManager process 에서 Chatbot 을 실행하기 위해 만들어 놓은 function
    """
    app = Application(pipe)
    app.run()

if __name__ == "__main__":
    """
    ChatbotManager 에서 실행하는 것이 아닌, chatbot 단독으로 실행할 때에 진입하는 부분
    """
    app = Application()
    app.run()