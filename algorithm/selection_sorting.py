# 백준 2750번 문제
# N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.


import sys

data = [] # 빈 리스트 생성

for i in range(int(input())): # 입력받은 정수만큼의 횟수 반복
    data.append(int(input())) # data 리스트에 정수를 추가 

for i in sorted(data): # data 리스트에 저장된 정수들을 오름차순으로 정렬
    print(i) # 각 정수를 한 줄씩 출력
