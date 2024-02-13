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
    word = sys.stdin.readline().split()
    order = word[0]
    
    if order == 'push':
        value = word[0]
        stack.append(value)
    
    elif order == 'pop':
        if not stack:
            print(-1)
        else:
            print(stack.pop())
            
    elif order == 'size':
        print(len(stack))
        
    elif order == 'empty':
        if not stack:
            print(1)
        else:
            print(0)
            
    elif order == 'top':
        if not stack:
            print(-1)
        else:
            print(stack[-1])
            