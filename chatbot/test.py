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
        self.apiKey = {
            "key": "5067718126:AAFdqW_LnaJX5bUYWANt6-x699AfGQW15wk" ,
            "gongongKey": "%2FjEMJvdXRrLVtFtwr%2BU8UCwlaDibJ70XI3tSO1WAiv2aNo%2BJgK7wpWlQOc7J4zh70e41x%2FQREMkSqHIJDzq9nw%3D%3D" ,
            "naverKey": "RD3zHR8A8ILjNgmwKuz_" ,
            "naverpass": "MjusBHLvzp"
        }

        self.text = ({
            "menual_msg": "봇 사용 메뉴얼"
                          "이 봇은 현재 날씨 기준으로 날씨에 맞는 음료를 추천해줍니다.\n"
                          "사용 방법을 보려면 도움말 버튼을 눌러주시고,\n ",
                          "순서대로 주문해주시면 됩니다."
            "menu_List_msg": "아이템" ,
            "menuProduct_List_msg": "추천메뉴" ,
            "welcome_msg": "안녕하세요 탄산음료자판기봇입니다."
                           "사용하시려면 사용시작 버튼을 눌러주시고"
                           "사용방법을 보시려면 도움말 버튼을 눌러주세요." ,
            "select_button": {
                "deposit": '1000원 또는 1000을 입력해주세요. 금액대는 상관없습니다. (잔액: {money}원)' ,
                "order_empty": f'장바구니가 텅텅비어있네요!' ,
                "order_done": f'결제완료 하였습니다.' ,
                "order_fail": '결제 실패했습니다 {losemoney}원이 부족합니다.'
            }
        })

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

    def read_key(self, path):
        # 파이썬 봇 토큰 키

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
        nx ="62"
        ny ="120"

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

        # items 로 요청한 값 받아옴
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

                if weather_code == '1':# 비
                    weather_state = 'ra'
                elif weather_code == '2':# 비,눈
                    weather_state = 'rs'
                elif weather_code == '3':# 눈
                    weather_state = 'sn'
                elif weather_code == '4':# 소나기
                    weather_state = 'so'
                else:
                    weather_state = 'su'# 맑음

                weather_data['code'] = weather_code
                weather_data['state'] = weather_state

        data['weather'] = weather_data

        state = data['weather']['state']
        return state


    def Naver_Key(self, path):
        # 파이썬 봇 토큰 키
        with open(path, 'r') as r:
            content = json.load(r)
        ListAPI=[content['naverKey'],content['naverpass']]
        return ListAPI

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

    def menu(self, context, chat_id,userCnt):
        # 메인 메뉴 버튼 생성 및 메인 메뉴 함수

        answer_text = f'안녕하세요 저는 자판기 봇입니다. 먼저 사용방법을 보시려면 도움말 버튼을 눌러주세요. (현재 잔액: {self.money:,}원)입니다.'

        ## 방문 횟수가 적은 손님용
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('도움말', callback_data='help')],
            [InlineKeyboardButton('돈넣기', callback_data='deposit')],
            [InlineKeyboardButton('메뉴보기', callback_data='List')],
            [InlineKeyboardButton('주문하기', callback_data='Order')],
            [InlineKeyboardButton('평가하기', callback_data='evaluate')],
            #[InlineKeyboardButton('사진전송', callback_data='SendPhoto')],
            [InlineKeyboardButton('종료하기', callback_data='finish')]
        ])

        ## 방문 횟수가 10회 넘은 단골 손님용
        reply_markup2 = InlineKeyboardMarkup([
            [InlineKeyboardButton('돈넣기', callback_data='deposit')],
            [InlineKeyboardButton('메뉴보기', callback_data='List')],
            #[InlineKeyboardButton('사진전송', callback_data='SendPhoto')],
            [InlineKeyboardButton('주문하기', callback_data='Order')],
            [InlineKeyboardButton('평가하기', callback_data='evaluate')],
            [InlineKeyboardButton('종료하기', callback_data='finish')]
        ])
        if userCnt <= 10:
            context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup2)


    def menu_link(self, context, chat_id):

        answer_text = self.text['menu_link_msg']
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

    # 아이템 메뉴
    def menu_List(self, context, chat_id):
        answer_text = '아이템'
        show_list = []
        # dict -> list로 변환 -> for문과 index 통해 데이터 가져옴
        values = list(self.productList.values())

        # 아이템 데이터 전부 show_list dict 담음
        for keys in values[0]:
            show_list.append(InlineKeyboardButton((values[1])[keys], callback_data=(values[0])[keys]))

        # 마지막 버튼은 뒤로가기 버튼을 담음
        show_list.append(InlineKeyboardButton("뒤로가기", callback_data="menu"))  # add cancel button
        # 버튼 갯수에따라 구성을 달리해주는 기능
        reply_markup = InlineKeyboardMarkup(self.build_menu(show_list, len(show_list) - 1))  # make markup
        # 버튼 출력시키는 부분
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

    # def sendPhoto(self, context: telegram.ext.callbackcontext.CallbackContext, chat_id):
        # 여기서 원하는 사진 url을 변경할 수 있음 
        # context.bot.send_photo(chat_id=chat_id, photo="https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210727_70%2F1627366672518eC0pG_JPEG%2FwYj2YLSl66dBPHZ-flLqoIIk.jpeg.jpg&type=f&size=680x360")

    # 추천 메뉴
    def menuProduct_List(self, context, chat_id):
        answer_text = self.text['menuProduct_List_msg']
        show_list = []
        # dict -> list 변환 -> for문과 indext 통해 데이터 가져옴
        # 아이템 데이터 전부 show_list dict에 담음
        # 추천메뉴 같은 경우 아이템 id값과 추천메뉴 값과 일치하는것만 출력
        values = list(self.itemList.values())

        for keys in values[0]:
            result = str((values[0])[keys])
            weather = str((values[4])[keys])
            if  self.weatherState == weather:
                show_list.append(InlineKeyboardButton(f'{(values[1])[keys]}\n({(values[2])[keys]}원)',
                                                      callback_data=(values[3])[keys]))

        # 마지막 버튼은 뒤로가기 버튼 담음
        show_list.append(InlineKeyboardButton("뒤로가기", callback_data="menu"))  # add cancel button
        # 버튼 갯수에따라 구성을 달리해주는 기능
        reply_markup = InlineKeyboardMarkup(self.build_menu(show_list, len(show_list) - 1))  # make markup
        # 버튼 출력시키는 부분
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

    # 장바구니 기능은 들어가있지만, 담기지 않으면 사용하지 않음
    def addCart(self, index, context, chat_id):
        # 선택한 추천메뉴 버튼 클릭시 클릭한 아이템 cartList 컬렉션에 담음
        # totalmoney로 결제해야 할 금액이 더해짐
        values = list(self.itemList.values())

        for keys in values[3]:
            result = str((values[3])[keys])
            if index == result:
                self.CartList[(values[1])[keys]] = (values[2])[keys]
                self.totalSellMoney += (values[2])[keys]

        self.menuProduct_List(context, chat_id)

    # 봇이 그룹에 속해있을 때 유저가 그룹에 들어오면 웰컴 메서드 호출
    def welcome(self, update, context, new_member):
        """ Welcomes a user to the chat """

        message = update.message
        chat_id = message.chat.id

        answer_text = self.msg['menu_msg']

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('사용시작', callback_data='menu')],
            [InlineKeyboardButton('도움말', callback_data='help')],
        ])
        context.bot.send_message(chat_id=chat_id, text=answer_text, reply_markup=reply_markup)

        # Replace placeholders and send message

    # 유저 -> 봇으로 메세지 날릴 때 호출
    def get_message(self, update, context):
        chat_id = update.effective_message.chat.id
        text = update.effective_message.text
        self.Usercnt= self.UserSet(update.effective_user.id)

        if text == '/start':
            self.sellList.clear()

            if self.weatherState == 'rs':
                context.bot.send_message(chat_id=chat_id, text='금일은 비와 눈이 옵니다')
            elif self.weatherState == 'ra':
                context.bot.send_message(chat_id=chat_id, text='금일은 비가 옵니다.')
            elif self.weatherState == 'su':
                context.bot.send_message(chat_id=chat_id, text='금일은 맑습니다.')
            elif self.weatherState == 'sn':
                context.bot.send_message(chat_id=chat_id, text='금일은 눈이 옵니다')
            elif self.weatherState == 'so':
                context.bot.send_message(chat_id=chat_id, text='금일은 소나기가 옵니다')

            self.menu(context, chat_id,self.Usercnt)
        elif self.isdepoit:
            try:
                won = re.sub(r'[^0-9]', '', text)
                self.money += int(won)
                answer_text = f"{int(won):,}원을 넣었습니다."
                self.isdepoit = False
                context.bot.send_message(chat_id=chat_id, text=answer_text) # 돈을 추가하는 기능
                self.menu(context, chat_id, self.Usercnt)
            except:
                answer_text = '입력을 잘못했습니다. 다시 입력해주세요.'
                context.bot.send_message(chat_id=chat_id, text=answer_text)
        else:
            txtmemo = f'말씀을 이해하지못했습니다. 다시 말씀해주세요.'
            context.bot.send_message(text=txtmemo, chat_id=chat_id)
            self.menu(context, chat_id, self.Usercnt)
        # 돈넣기 활성화 되어있을때만 금액 입력시 작동

    # 메시지 출력하기 위한 함수. 메시지 핸들러에 의해 호출
    def empty_message(self, update, context):
        """
        Empty messages could be status messages, so we check them if there is a new
        group member, someone left the chat or if the bot has been added somewhere.
        """

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
        # 추천메뉴 화면으로 넘어가기위해 아이템 id값 가져옴
        index = self.get_key(data)
        tempUSerCnt = self.UsercntSearch(update.effective_user.id)
        tagindex = self.get_Tagkey(data)
        print("tag_index")
        print(tagindex)

        # 메인메뉴
        if data == 'menu':
            self.menu(context, chat_id, tempUSerCnt)

        # 도움말
        elif data == 'help':
            context.bot.send_message(text=self.Help_text, chat_id=chat_id)
            self.menu(context, chat_id, tempUSerCnt)

        # elif data == 'TEST':
        #    context.bot.send_photo(photo='https://m.epicbox.co.kr/web/product/big/201908/df72550a87a40147f8366f3e51b1aa8c.jpg', chat_id=chat_id)
        #   self.menu(context, chat_id, tempUSerCnt)

        # 돈 충전
        elif data == 'deposit':
            self.isdepoit = True
            answer_text = answer_text = self.text['select_button']['deposit'].format(money=f'{self.money:,}')
            context.bot.edit_message_text(text=answer_text, chat_id=chat_id, message_id=message_id)

        # 주문하기
        elif data == 'Order':
            if len(self.CartList) <= 0:
                answer_text = f'장바구니가 텅텅비어있네요!'
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.menu(context, chat_id, tempUSerCnt)

            elif self.money >= self.totalSellMoney:
                # 주문하기 이전 장바구니, 취소기능 추가
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton('장바구니', callback_data='Order_Cart')],
                    [InlineKeyboardButton('주문하기', callback_data='Order_Pay')],
                    [InlineKeyboardButton('취소하기', callback_data='Order_Cancel')],
                ])
                context.bot.send_message(chat_id=chat_id , text="주문하기 전 메뉴", reply_markup=markup)

            else:
                losemoney = self.totalSellMoney - self.money
                answer_text = self.text['select_button']['order_fail'].format(losemoney=f'{losemoney:,}')
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.menu(context, chat_id, tempUSerCnt)

        # 대분류 메뉴로 넘어감
        elif data == 'List':
            self.menuProduct_List(context, chat_id)

        # 사진 전송 기능 추가
        # elif data == "SendPhoto":
        #    self.sendPhoto(context, chat_id)

        elif data == "Order_Cart":
            # 장바구니를 보여줌
            msg = f"장바구니리스트\r\n"

            for cart in self.CartList:
                msg += f"""{cart} - {self.CartList[cart]}\r\n"""

            context.bot.send_message(text=msg, chat_id=chat_id)

        elif data == "Order_Pay":
            if self.money >= self.totalSellMoney:
                # 주문하기 이전 장바구니, 취소 기능 추가
                self.money -= self.totalSellMoney
                answer_text = f'결제를 완료 하였습니다.'
                context.bot.send_message(text=answer_text, chat_id=chat_id)
                self.sellList = self.CartList
                for x in self.sellList:
                    URL = self.NaverAPI(x)
                    context.bot.send_message(chat_id=chat_id, text=URL)
                self.menu(context, chat_id, tempUSerCnt)

        elif data == "Order_Cancel":
            answer_text = f"주문을 취소했습니다."
            context.bot.send_message(text=answer_text, chat_id=chat_id)
            self.menu(context, chat_id, tempUSerCnt)

        elif data == index:
            self.menuProduct_List(index, context, chat_id)

        # 장바구니 담기위함
        elif data == tagindex:
            print("태그인덱스 ", data, tagindex)
            self.addCart(tagindex, context, chat_id)

        # 평가하기
        # elif data == 'evaluate'
        # answer_text = f'평가해주셔서 감사합니다.!'
        # context.bot.send_message(text=answer_text, chat_id=chat_id)
        # self.evaluate(context, chat_id)

        # 종료버튼 클릭시 거스름돈 출력 및 파일저장(result00.csv)
        elif data == 'finish':
            # 메시지가 종료하기일 때
            answer_text = '판매를 종료합니다.'
            txtmoney = f'{self.money:,}원 거스름돈입니다.'
            context.bot.send_message(chat_id=chat_id, text=txtmoney)
            chat_user_client = update.effective_user.full_name
            pd.DataFrame({"username": [f"{chat_user_client}"],
                          "message_id": [message_id], "chatid": [chat_id], "Userid": [update.effective_user.id],
                          "exchange": [self.money]}).to_csv(
                f'result00.csv', index=False)
            self.money = 0


    # 해당 소분류 화면으로 넘어가기 위함
    def get_key(self, val):

        values = list(self.productList.values())
        for keys in values[0]:
            result = str((values[0])[keys])
            if val == result:
                return result
        return "There is no such Key"

    # 장바구니를 담기 위해 해당 소분류 아이템 키 가져옴
    def get_Tagkey(self, val):

        values = list(self.itemList.values())
        for keys in values[3]:
            result = str((values[3])[keys])
            if val == result:
                return result
        return "There is no such tag Key"

    # 메뉴 아이템 데이터 엑셀 생성하기위함
    def itemSet(self):
        # df = pd.DataFrame({'id': [1, 2], '대분류': ['과자', '음료']})
        # df.to_csv("bigitem.csv", index=False)

        # df = pd.DataFrame({'id': [1,1, 2, 2,2,2], 'name': ['허니버터칩','초코하임', '생수', '콜라','사이다','환타'], 'price': [3000, 2800, 800, 1500, 1300, 1100],'tag':['food1','food2','water1','water2','water3','water4']})
        # df.to_csv("item.csv", index=False)
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
            df = pd.DataFrame({'id': [1, 1, 2, 2, 2, 2], 'name': ['허니버터칩', '초코하임', '생수', '콜라', '사이다', '환타'],
                               'price': [3000, 2800, 800, 1500, 1300, 1100],
                               'tag': ['food1', 'food2', 'water1', 'water2', 'water3', 'water4'],
                               'weather': ['ra', 'ra', 'so', 'sn', 'rs', 'su']})
            df.to_excel("item.xlsx", index=False, encoding='utf-8-sig')

        self.itemList = (pd.read_excel("item.xlsx")).to_dict()
        self.productList = (pd.read_excel("bigitem.xlsx")).to_dict()

    # 유저 리스트 엑셀 생성
    def UserSet(self,id):

        Userfile = 'user.json'  # 예제 Textfile
        groupList = dict()
        file_data = dict()
        if os.path.isfile(Userfile):

            with open(Userfile, 'r') as f:
                json_data = json.load(f)
            try:
                cnts = json_data[str(id)]['cnt']
                cnts = cnts + 1
                json_data[str(id)]['cnt'] = cnts
                with open(Userfile, 'w', encoding='utf-8') as make_file:
                    json.dump(json_data, make_file, indent="\t")
                return json_data[str(id)]['cnt']
            except KeyError:
                file_data['cnt'] = 1
                groupList[id] = file_data
                json_data.update(groupList)

                with open(Userfile, 'w', encoding='utf-8') as make_file:
                    json.dump(json_data, make_file, indent="\t")

                return 1
        else:

            file_data['cnt'] = 1
            groupList[id]=file_data

            with open(Userfile, 'w', encoding='utf-8') as make_file:
                json.dump(groupList, make_file, indent="\t")

            return 1

    def UsercntSearch(self, id):

        Userfile = 'user.json'  # 예제 Textfile

        if os.path.isfile(Userfile):

            with open(Userfile, 'r') as f:
                json_data = json.load(f)

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