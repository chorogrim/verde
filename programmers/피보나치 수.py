# 피보나치 수는 F(0)=0, F(1)=1일 때, 1 이상의 n에 대하여 
# F(n) = F(n-2)가 적용되는 수입니다.
# 2 이상의 n이 입력되었을 때, n번째 피보나치 수를 1234567으로 나눈 나머지를 
# 리턴하는 함수, solution을 완성해 주세요.


def solution(n):
    arr = []
    arr.append(0)
    arr.append(1)
    arr.append(1)
    
    for i in range(1, n-1):
        arr.append(arr[i]+ arr[i+1])
    return arr[n] % 1234567