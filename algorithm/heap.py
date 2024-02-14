# 백준 알고리즘 1927번 문제
# 최소 힙을 이용하여 다음과 같은 연산을 지원하는 프로그램을 작성하시오.
# 1. 배열에 자연수 x를 넣는다
# 2. 배열에서 가장 작은 값을 출력하고, 그 값을 배열에서 제거한다.


import heapq
import sys

# heap을 저장하기 위한 리스트
arr = []

# 처음 주어지는 정수 값만큼 반복
for i in range(int(sys.stdin.readline())):
    # 정수 값 받을 x 선언
    x = int(input())
    
    # 받은 x 값이 0인 경우
    if x == 0:
        # 요소가 없을 경우, 길이는 0이며 이때 0을 출력
        if len(arr) == 0:
            print(0)
        # 요소가 있을 경우 최소 힙 출력
        else:
            print(heapq.heappop(arr))
    # 받은 값이 0이 아닌 경우, 최소 힙으로 생성
    else:
        heapq.heappush(arr, x)        
