# 백준 10814번 문제
# 온라인 저지에 가입한 사람들의 나이와 이름이 가입한 순서대로 주어진다. 이때, 회원들을 나이가 증가하는 순으로, 나이가 같으면 먼저 가입한 사람이 앞에 오는 순서로 정렬하는 프로그램을 작성하시오.


import sys

n = int(input()) # 입력받을 정수 n 선언
result = [] # 결과를 담을 빈 리스트 생성

for i in range(n): # n번 반복하면서
    age, name = sys.stdin.readline().split() # 분리된 문자열을 각각 age와 name의 변수에 할당
    result.append([age, name]) # 변수 result에 [age, name] 형태의 리스트를 추가

result = sorted(result, key = lambda x : x[0]) # sorted() 함수를 사용하여 리스트 result를 정렬
                                               # key = lambda x : x[0] 함수는 각 요소의 첫 번째 값을 기준으로 정렬. 즉, 나이 기준으로 정렬
for j in result: # result를 순회하면서
    print(*j) # 각 요소를 출력. 리스트의 각 요소를 공백으로 구분하여 출력