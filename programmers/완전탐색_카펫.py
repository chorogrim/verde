def solution(brown, yellow):
    '''
    brown: 갈색 타일의 개수
    yellow: 노란색 타일의 개수
    '''
    answer = []
    
    sum = brown + yellow # 갈색 타일과 노란색 타일의 수를 합하여 타일의 수를 구함
    divisors = [] # 약수를 저장할 리스트 divisors 초기화

    for i in range(1, sum + 1): # 1부터 총 타일의 수까지의 숫자에 대해 반복
        if sum % i == 0: # 현재 숫자 i가 총 타일의 수의 약수인지 확인
            divisors.append(i) # i가 총 타일의 약수라면 divisors 리스트에 추가
            
    for divisor in divisors: # 약수 리스트에 있는 각각의 숫자에 대해 반복
        across_divisor = sum / divisor # 총 타일의 수를 현재 약수로 나눈 값을 구함
        
        if (across_divisor - 2) * (divisor - 2) == yellow: # 현재 가로와 세로를 고려하여 노란색 타일의 수를 계산
            answer.append(across_divisor) # 만약 조건을 만족한다면, 가로를 결과 리스트에 추가
            answer.append(divisor) # 세로를 결과 리스트에 추가
            break # 가장 작은 조건을 만족하는 가로와 세로를 찾았으므로 반복문을 종료
    return answer # 최종적으로 찾은 가로와 세로를 담고 있는 answer 리스트를 반환
