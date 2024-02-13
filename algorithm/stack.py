# 백준 알고리즘 10828 문제
# 정수를 저장하는 스택을 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.
# push x : 정수 x를 스택에 넣는 연산
# pop : 스택에서 가장 위에 있는 정수를 빼고, 그 수를 출력
# size : 스택에 들어있는 정수의 개수를 출력
# empty : 스택이 비어있으면 1, 아니면 0을 출력
# top : 스택의 가장 위에 있는 정수를 출력


import sys

n = int(sys.stdin.readline())
stack = []

for i in range(n):
    a = input().split()
    if a[0] == 'push':
        stack.append(a[1])
    elif a[0] == 'pop':
        if len(stack):
            print(stack[-1])
            stack.pop()
        else:
            print(-1)
    elif a[0] == 'size':
        print(len(stack))
    elif a[0] == 'empty':
        if len(stack):
            print(0)
        else:
            print(1)
    else:
        if len(stack):
            print(stack[-1])
        else:
            print(-1)