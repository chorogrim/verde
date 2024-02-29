# 백준 알고리즘 10989번 문제
# N개의 수가 주어졌을 때, 이를 오름차순으로 정렬하는 프로그램을 작성하시오.


import sys

n = int(sys.stdin.readline()) # 사용자로부터 한 줄을 입력받고, 이를 정수형으로 변환하여 n에 저장
count = [0] * 10001 # 길이가 10001인 리스트 count 생성, 모든 요소를 0으로 초기화

for i in range(n): # n번 반복하면서
    count[int(sys.stdin.readline())] += 1 # 정수형으로 변환하여 리스트 count에 해당 숫자 빈도를 1 증가

for i in range(10001): # 0부터 10000까지의 숫자를 반복하면서 
    if count[i] != 0: # count[i]가 0이 아니라면, count[i]의 값만큼 숫자 i를 출력
        print('%s\n'%i * count[i], end='') # 문자열 포맷팅을 사용하여 숫자를 문자열로 변환하고 줄바꿈을 추가
                                           # % count[i]는 해당 숫자가 몇 번 등장했는지에 따라 출력할 횟수를 결정
                                           # end=''는 print() 함수가 줄바꿈을 하지 않도록 설정