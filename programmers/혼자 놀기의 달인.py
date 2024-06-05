def solution(cards):
    answer = [] # 각 카드 그룹의 크기를 저장
    
    for i in range(len(cards)): # 각 카드의 인덱스 i에 대해 반복
        tmp = 0 # tmp 변수를 초기화
        while cards[i]: # cards[i]가 0이 아닐 때까지 반복
            next_i = cards[i] - 1 # 현재 카드의 값에서 1을 뺀 값을 저장
            cards[i], i = 0, next_i # cards[i]값을 0으로 설정하여 현재 카드를 방문했음을 표시하고, 
            tmp +=1 # 1 증가시켜 현재 그룹의 크기를 증가
        answer.append(tmp) # 현재 그룹의 크기 tmp를 answer 리스트에 추가
    answer.sort() # answer 리스트를 오름차순으로 정렬
    
    return answer[-1]  * answer[-2] # answer 리스트의 마지막 두 요소의 곱을 반환