def solution(targets): # targets라는 2차원 리스트를 매개변수로 받음. 각 요소는 '시작 시간, 종료 시간'을 나타냄
    answer = 0 # 선택된 타켓의 개수를 저장할 변수 answer를 0으로 초기화
    targets.sort(key = lambda x: [x[1], x[0]]) # targets 리스트를 종료 시간('x[0]')을 기준으로 오름차순으로 정렬
    
    s = e = 0 # 현재 선택된 타겟의 시작 시간 s와 e를 0으로 초기화 
    for target in targets: # 정렬된 targets 리스트를 순회
        if target[0] >= e: # 현재 타겟의 시작시간 target[0]이 이전 타켓의 종료시간 e보다 크거나 같다면,
            answer += 1 # 타겟을 선택. 선택된 타겟의 개수를 증가
            e = target[1] # 현재 타겟의 종료 시간 target[1]을 e에 저장하여 사용
    return answer # 모든 타겟을 순회한 후 선택된 타겟의 총 개수를 반환 
