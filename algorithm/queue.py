# 백준 알고리즘 10845 문제
# 정수를 저장하는 큐를 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.
# push x : 정수 x를 큐에 넣는 연산
# pop : 큐에서 가장 앞에 있는 정수를 빼고, 그 수를 출력
#       만약 큐에 들어있는 정수가 없을 경우에는 -1을 출력
# size : 큐에 들어있는 정수의 개수를 출력
# empty : 큐가 비어있으면 1, 아니면 0을 출력
# front : 큐의 가장 앞에 있는 정수를 출력
#         만약 큐에 들어있는 정수가 없을 경우에는 -1을 출력
# back : 큐의 가장 뒤에 있는 정수를 출력
#        만약 큐에 들어있는 정수가 없을 경우에는 -1을 출력


import sys

# 입력 받을 값 n을 선언
n = int(sys.stdin.readline())

# 정수르 저장할 큐를 빈 리스트로 선언
queue = []

for i in range(n):
    word = sys.stdin.readline().split()
    order = word[0]

    if order == 'push':
        value = word[0]
        queue.append(value)

    elif order == 'pop':
        if not queue:
            print(-1)
        else:
            print(queue[-1])

    elif order == 'size':
        print(len(queue))

    elif order == 'empty':
        if not queue:
            print(1)
        else:
            print(0)

    elif order == 'front':
        if not queue:
            print(-1)
        else:
            print(queue[-1])
    
    elif order == 'back':
        if not queue:
            print(-1)
        else:
            print(queue[-1])