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
# deque는 list와 dictionary와 거의 동일

import sys

# 입력 받을 값 n을 선언
n = int(sys.stdin.readline())

# 정수를 저장할 빈 리스트 선언
queue = []

# 반복문을 통해 입력 받는 값을 처리
for i in range(n):
    word = sys.stdin.readline().split()
    order = word[0]

    # order와 push와 같다면
    if order == 'push':
        # queue에 value의 두 번째 값을 append
        queue.append(int(word[1]))
    # order와 pop와 같다면
    elif order == 'pop':
        # queue의 길이가 0보다 작다면 queue의 첫 번째 요소를 제거(제일 앞의 요소 삭제)
        if len(queue) != 0:
            print(queue.pop(0))
        # 그렇지 않다면 -1을 출력
        else:
            print(-1)

    # order와 size가 같다면 queue의 정수의 개수를 출력
    elif order == 'size':
        print(len(queue))
    
    # order와 empty와 같다면
    elif order == 'empty':
        # queue의 길이가 0일 경우 1을 출력, 아니면 0을 출력
        if len(queue) == 0:
            print(1)
        else:
            print(0)
    
    # order와 front와 같다면
    elif order == 'front':
        # queue의 길이가 0일 경우 -1을 출력, 그렇지 않다면 queue의 첫 번째 값을 출력
        if len(queue) == 0:
            print(-1)
        else:
            print(queue[0])

    # order와 back이 같다면
    elif order == 'back':
        # queue의 길이가 0일 경우 -1을 출력, 그렇지 않다면 queue의 마지막 값을 출력
        if len(queue) == 0:
            print(-1)
        else:
            print(queue[-1])

## 맞았음 ! ##