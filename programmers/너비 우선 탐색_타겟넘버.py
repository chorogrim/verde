def solution(numbers, target): 
    '''
    numbers: 주어진 숫자들의 리스트
    target: 목표값
    '''
    answer = 0 # 경우의 수를 저장하기 위한 것으로 초기값 0으로 설정
    ansList = [0] # 계산된 가능한 결과값을 저장하기 위한 리스트
    
    for num in numbers: # 주어진 숫자 리스트인 numbers를 순회하면서 각 숫자를 하나씩 꺼내어 처리
        tmpList = [] # 임시로 결과값을 저장하기 위한 리스트

        for a in ansList: # ansList에 저장된 각각의 결과값에 대해 현재 숫자를 더하거나 빼서 나올 수 있는 모든 경우의 수를 tmpList에 저장
            tmpList.append(a+num) # 현재 숫자 num을 이전 결과값 a에 더한 값을 tmpList에 추가
            tmpList.append(a-num) # 현재 숫자 num을 이전 결과값 a에서 뺀 값을 tmpList에 추가
        ansList = tmpList # 모든 계산이 끝나면 tmpList에 저장된 새로운 결과값들로 ansList를 업데이트
        
    for a in ansList: # ansList에 저장된 각각의 값들을 순회하며 처리
        if a == target: # 현재 값 a가 목표 수 target과 같은지 비교
            answer += 1 # 만약 현재 값 a가 목표 수 target과 같다면, answer를 1증가
    return answer # answer를 반환하여 함수의 결과로 출력
    
