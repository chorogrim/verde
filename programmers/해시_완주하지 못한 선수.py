def solution(participant, completion):
    answer = '' # 반환할 값을 초기화
    p_dict = {} # 참가자 이름을 키로 하고, 등장 횟수를 값으로 가지는 p_dict 딕셔너리
    
    for p in participant: # 참가자 리스트를 반복
        if p not in p_dict: # 현재 참가자가 딕셔너리에 없다면
            p_dict[p] = 1 # 딕셔너리에 새로운 키를 추가하고 값을 1로 설정
        else: # 이미 딕셔너리에 존재하는 참가라자면
            p_dict[p] += 1 # 해당 참가자의 값을 1증가
            
    for c in completion: # 완주자 리스트를 반복
        p_dict[c] -= 1 # 완주한 참가자의 등장 횟수를 1감소
        
    for pd in p_dict: # 딕셔너리를 반복
        if p_dict[pd] == 1: # 등장 횟수가 1인 참가자를 찾음
            answer = pd # 해당 참가자를 정답으로 설정
    return answer # 찾은 정답을 반환 
