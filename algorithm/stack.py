# 백준 알고리즘 10828 문제
# 정수를 저장하는 스택을 구현한 다음, 입력으로 주어지는 명령을 처리하는 프로그램을 작성하시오.
# push x : 정수 x를 스택에 넣는 연산
# pop : 스택에서 가장 위에 있는 정수를 빼고, 그 수를 출력
#       스택에 들어있는 정수가 없을 경우에는 -1을 출력
# size : 스택에 들어있는 정수의 개수를 출력
# empty : 스택이 비어있으면 1, 아니면 0을 출력
# top : 스택의 가장 위에 있는 정수를 출력


import sys

# 입력받을 값을 n에 대입
n = int(sys.stdin.readline())
# stack을 저장하기 위한 리스트 선언
stack = []

# 반복문을 통해 입력 받는 값을 처리
for i in range(n):
    # word라는 변수에 들어온 값을 앞,뒤로 쪼개줌
    # 쪼개준 값을 다시 전달 받고, 값을 반환할 때 index 형태로 돌려줌
    word = sys.stdin.readline().split()
    # order라는 변수에 word의 0을 대입. 명령(push, pop, size, empty, top)이 order에 담김
    order = word[0]
    
    # order가 push일 경우
    if order == 'push':
        # stack에 word 두번째 값을 넣어줌
        stack.append(word[1])
    
    # order가 pop일 경우
    elif order == 'pop':
        # stack의 길이가 0일 경우 stack의 첫 번째 요소를 출력, 그렇지 않다면 -1을 출력
        if len(stack) != 0:
            print(stack.pop())
        else:
            print(-1)     

    # order가 size일 경우        
    elif order == 'size':
        # stack에 들어있는 정수의 개수를 출력
        print(len(stack))
    
    # order가 empty일 경우  
    elif order == 'empty':
        # stack이 없다면 1을 출력, 그렇지 않다면 0을 출력
        if not stack:
            print(1)
        else:
            print(0)
    
    # order가 top일 경우      
    elif order == 'top':
        # stack이 없다면 -1을 출력, 그렇지 않다면 stack의 맨 첫 번째(즉, 가장 마지막 값)을 출력
        if not stack:
            print(-1)
        else:
            print(stack[-1])

## 맞았음! ##