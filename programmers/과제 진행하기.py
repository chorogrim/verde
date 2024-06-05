def solution(plans):
    '''
    plans: 각 작업의 이름, 시작 시간, 소요 시간
    '''
    stack = [] # 현재 진행 중인 작업
    answer = [] # 최종적으로 처리된 작업들의 순서
    
    for i in range(len(plans)): # 리스트의 각 요소를 반복하면서 시작 시간을 분 단위로 변환
        h, m = map(int, plans[i][1].split(':')) # 
        plans[i][1] = h*60 + m # 시작 시간을 분 단위로 변환하여 plans[i][1]에 저장
        plans[i][2] = int(plans[i][2]) # plans[i][2]를 정수형으로 변환하여 소요 시간을 저장
        
    plans.sort(key = lambda x: x[1]) # plans[i][1]을 기준으로 정렬
    
    for i in range(len(plans)-1):
        stack.append([plans[i][0], plans[i][2]]) # 작업의 이름과 소요 시간을 stack에 추가
        gap = plans[i+1][1] - plans[i][1] # 현재 작업과 다음 작업의 시작 시간 차이를 계산하여 gap에 저장
        
        while stack and gap: # stack이 비어 있지 않고, gap이 0보다 큰 동안 반복
            nowTime = stack[-1][1]  # stack의 마지막 요소('stack[-1][1]')의 소요 시간을 nowTime에 저장
            
            if nowTime <= gap: # nowTime이 gap보다 작거나 같으면
                name, time = stack.pop() # stack의 마지막 작업을 꺼내 그 이름과 소요 시간을 가져옴
                gap -= time # gap에서 소요 시간을 빼고
                answer.append(name) # 작업 이름을 answer에 추가
    return answer # 최종적으로 처리된 작업들의 순서가 저장된 answer 리스트를 반환