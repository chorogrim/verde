# 입국심사를 기다리는 사람 수n, 각 심사관이 한 명을 심사하는데 걸리는 시간이 
# 담긴 배열 times가 매개변수로 주어질 때, 모든 사람이 심사를 받는데 걸리는
# 시간의 최솟값을 return 하도록 solution 함수를 작성해 주세요.


def solution(n, times):
    start = 1
    end = max(times) * n
    
    while start <= end:
        mid = (start + end) // 2
        people = 0
        
        for t in times:
            people += mid // t
            
        if people >= n:
            answer = mid
            end = mid - 1
        else:
            start = mid + 1
    return answer
