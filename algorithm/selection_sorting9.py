# 백준 알고리즘 1181번 문제
# 알파벳 소문자로 이루어진 N개의 단어가 들어오면 아래와 같은 조건에 따라 정렬하는 프로그램을 작성하시오.
# 1. 길이가 짧은 것부터 / 2. 길이가 같으면 사전 순으로 / 단, 중복된 단어는 하나만 남기고 제거해야 한다.


import sys
input = sys.stdin.readline

n = int(input())
a = [] # 빈 리스트 생성

for i in range(n): # n번 반복하면서
    a.append(input().rstrip()) # rstrip() 메서드를 호출하여 문자열 끝의 공백을 제거

for i in sorted(set(a), key=lambda x: (len(x), x)): # set(a)를 사용하여 리스트 a의 중복된 요소들을 제거한 집합을 만듦
    print(i) # 정렬된 문자열을 출력                   # key=lambda x: (len(x), x) 이 함수는 문자열의 길이를 먼저 정렬하고, 길이가 같은 경우에는 사전 순서로 정렬