# 백준 알고리즘 10816 문제
# 정수 M개가 주어졌을 때, 이 수가 적혀있는 숫자 카드를 상근이가 몇 개 가지고 있는지 구하는 프로그램을 작성하시오.

import sys

# dict을 선언
dict = {}
# 입력 받을 n을 선언
n = int(input())
# 숫자로 된 nl을 split해서 입력 받을 것 -> list로 바꿔줌
nl = list(map(int, sys.stdin.readline().split()))
# 입력 받을 m을 선언
m = int(input())
# 숫자로 된 ml을 split해서 입력 받을 것 -> list로 바꿔줌
ml = list(map(int, sys.stdin.readline().split()))

# 입력 받을 n값에
for i in range(n):
    # nl[i]가 dict에 있으면
    if nl[i] in dict:
        # +1을 해주고
        dict[nl[i]] +=1
    # 아니면 1을 출력
    else:
        dict[nl[i]] = 1

# 입력 받는 m값에      
for i in range(m):
    # ml[i]가 dict에 있다면 몇개가 있는지 출력, 없으면 0을 출력하고 띄어쓰기
    if ml[i] in dict:
        print(dict[ml[i]], end=' ')
    else:
        print(0, end= ' ')
        