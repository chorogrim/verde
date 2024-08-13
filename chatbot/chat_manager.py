# -*- coding: utf-8 -*-

import multiprocessing
import chatbot2
import time
import datetime


class ChatbotManager:
    """
    chatbot 을 감시하기 위한 class

    기본적으로 chatbot manager 가 실행될 때에 chatbot process 를 생성하도록 하고,
    chatbot process 로부터 'pong' 메세지를 받고 감시 프로세스가 동작하게 된다.

    chatbot process 가 실행되는 시간을 self.PROGRAM_LOADING_TIME(초단위) 으로 정의해 놓았으며,
    chatbot process 와 ping, pong 통신을 할 때 self.PROGRAM_ALIVE_CHECK(초단위) 만큼 통신이 이루어지지 않으면
    chatbot에 이상이 있다고 판단하고 chatbot process 를 kill 시킨 후 다시 실행하도록 한다.
    """
    def __init__(self):
        self.p_pipe, self.c_pipe = None, None
        self.chatbot_process = None
        self.send_flag = False
        self.c_time = datetime.datetime.now()

        self.PROGRAM_LOADING_TIME = 10
        self.PROGRAM_ALIVE_CHECK = 4
        self.wait_second = self.PROGRAM_LOADING_TIME

        # chatbot process 를 실행
        self.make_chatbot_process()

        while True:
            # self.send_flag 가 True 로 되어있을 때에만 ping 을 보내도록 함
            # self.send_flag 는 chatbot 으로부터 'pong' 메세지를 받았을 때에만 True 로 세팅됨
            if self.send_flag:
                self.p_pipe.send('ping')
                self.c_time = datetime.datetime.now()
                self.send_flag = False
                print('manager: ping send')

            if self.p_pipe.poll():
                data = self.p_pipe.recv()
                if data == 'pong':
                    print('manager: pong received')
                    self.c_time = datetime.datetime.now()
                    self.send_flag = True
                    self.wait_second = self.PROGRAM_ALIVE_CHECK

            time.sleep(1)

            n_time = datetime.datetime.now()

            # self.c_time 은 chatbot manager 가 chatbot 에게 'ping'을 보냈을 때의 시간이며, n_time 은 현재의 시간
            # 이 시간 차이가 self.wait_second 만큼이면 문제가 발생한 것으로 판단하고 chatbot 을 재실행함
            if (n_time - self.c_time).seconds >= self.wait_second:
                print('manager: 챗봇이 응답하지 않아서 다시 실행합니다.')
                self.wait_second = self.PROGRAM_LOADING_TIME
                self.chatbot_process.kill()
                self.make_chatbot_process()
                self.c_time = datetime.datetime.now()

    def make_chatbot_process(self):
        # chatbot manager 와 chatbot 간의 연결을 위한 pipe 를 생성
        self.p_pipe, self.c_pipe = multiprocessing.Pipe()

        # chatbot process 를 생성
        self.chatbot_process = multiprocessing.Process(target=self.start_chatbot, args=(self.c_pipe,))

        # chatbot process 를 실행
        self.chatbot_process.start()

    def start_chatbot(self, pipe):
        chatbot2.main(pipe)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = ChatbotManager()