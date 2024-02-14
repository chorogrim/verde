# 백준 알고리즘 1927 문제
# 최소 힙을 이용하여 다음과 같은 연산을 지원하는 프로그램을 작성하시오.
# 1. 배열에 자연수 x를 넣는다.
# 2. 배열에서 가장 작은 값을 출력하고, 그 값을 배열에서 제거한다.

import sys
import heapq

# heap을 저장하기 위한 리스트
arr = []

# 주어지는 정수 값만큼 반복
for i in range(int(sys.stdin.readline())):
    # 입력받을 값 x를 선언
    x = int(sys.stdin.readline())

    # x의 값이 0일 경우
    if x == 0:
        # 요소가 없을 경우 길이는 0이며 0을 출력
        if len(arr) == 0:
            print(0)
        # 그렇지 않다면, 최소 힙 출력
        else:
            print(heapq.heappop(arr))
    # 받은 값이 0이 아닌 경우, 최소 힙으로 생성
    else:
        heapq.heappush(arr,x)

## 맞았음 ! ##