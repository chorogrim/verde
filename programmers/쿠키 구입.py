def solution(cookie):
    max_value = 0 # 두 아들이 동일한 개수의 쿠키를 가질 수 있는 최대 쿠키의 개수를 저장
    
    for i in range(len(cookie)-1): # 첫 번째부터 마지막 바로 전까지의 쿠키를 순회
        front_value, front_idx = cookie[i], i # 왼쪽 아들의 쿠키 합계와 현재 인덱스
        end_value, end_idx = cookie[i+1], i+1 # 오른쪽 아들의 쿠키 합계와 현재 인덱스
        
        while True:
            if front_value == end_value and front_value > max_value: # 만약 왼쪽 아들의 쿠키 합계와 오른쪽 아들의 쿠키 합계가 같고
                max_value = front_value # max_value보다 크면 max_value 업데이트

            if front_idx > 0 and front_value <= end_value: # front_idx가 0보다 크고, 왼쪽 아들의 쿠키 합계가 오른쪽 아들의 쿠기 합계보다 작거나 같다면
                front_idx -= 1 # ftont_idx 를 하나 감소
                front_value += cookie[front_idx] # 왼쪽 아들의 쿠키 합계에 cookie[front_idx]를 더함

            elif end_idx < len(cookie) -1 and front_value >= end_value:
                end_idx += 1 # end_idx를 하나 증가
                end_value += cookie[end_idx] # 오른쪽 아들의 쿠키 합계에 cookie[end_idx]를 더함
            else: # 위의 조건을 만족하지 않는다면
                break # 종료
    return max_value # 두 아들이 동일한 개수의 쿠키를 가질 수 있는 최대 쿠키의 개수 반환    

                               