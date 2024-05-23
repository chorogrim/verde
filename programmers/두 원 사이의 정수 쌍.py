from math import sqrt

def solution(r1, r2): # r1은 작은 원의 반지름, r2는 큰 원의 반지름 
    quar = 0
    for i in range(0, r1): # i를 0부터 r1-1까지 반복. 작은 원의 반지름까지의 x축 좌표를 의미
        # 각 i에 대해 큰 원과 작은 원 사이의 y축 좌표에서 격자점의 수를 계산하여 quar에 더함
        quar += int(sqrt(r2**2 - i**2)) - int(sqrt(r1**2 - i**2 - 1)) # x축 좌표 i에 대해 큰 원의 y축 좌표를 계산, x축 좌표 i에 대해 작은 원의 y축 좌표를 계산
    for i in range(r1, r2): 
        quar += int(sqrt(r2**2 - i**2)) # x축 좌표 i에 대해 큰 원의 y축 좌표를 계산
    return quar * 4 # 첫 번째 사분면에서 계산된 격자점의 수를 4배하여 전체 원에서의 격자점의 수를 반환
