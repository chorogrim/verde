# 백준 알고리즘 1427번 문제
# 배열을 정렬하는 것은 쉽다. 수가 주어지면, 그 수의 각 자리수를 내림차순으로 정렬해보자.

import sys

input = sys.stdin.readline # 빠른 입력처리 위해 sys.stdin.readline으로 설정

n = int(input()) # 정수 n을 입력받기
n = sorted(str(n), reverse=True) # n을 문자열로 변환한 후, 각 자리의 숫자를 내림차순으로 정렬
print(''.join(n)) # sorted() 함수는 정렬된 문자열을 리스트 형태로 반환하므로, 이를 다시 문자열로 변환하기 위해 join() 함수를 사용