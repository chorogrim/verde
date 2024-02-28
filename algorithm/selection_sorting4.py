# 백준 2751번 문제
# N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.


import sys

n = int(sys.stdin.readline()) # 정수 입력받기

num_list = [] # 빈 리스트 생성

for i in range(n): # n번 반복하면서
    num_list.append(int(sys.stdin.readline())) # 한 줄씩 입력받고, 이를 정수형으로 변환하여 num_list에 추가

for item in sorted(num_list): # num_list를 오름차순으로 정렬
    sys.stdout.write(str(item) + '\n') # 정렬된 숫자들을 하나씩 꺼내어 문자열 형태로 출력. 줄바꿈 문자를 포함하여 출력


