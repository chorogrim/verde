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