def solution(id_list, report, k):
    '''
    id_list: 사용자들의 아이디
    report: 사용자들 간의 신고 이력
    k: 제재 기준이 되는 신고 횟수 
    '''
    answer = [] # 각 사용자가 제재당한 횟수를 저장할 리스트
    report_list = set() # 중복된 신고를 방지하기 위함
    reporter = {} # 각 사용자가 신고한 사용자들의 목록을 저장하는 딕셔너리
    reported = {} # 각 사용자가 받은 신고 횟수를 저장하는 딕셔너리
    
    for id in id_list: # id_list에 있는 각 사용자의 아이디를 순회
        reporter[id] = [] # 해당 사용자가 신고한 사용자들의 목록
        reported[id] = 0 # 해당 사용자가 받은 신고 횟수
        
    for r in report: # 신고 이력 리스트 report에 있는 각각의 신고 이력을 순회
        if r in report_list: # 이미 처리한 신고인지 확인. 신고 이력이 이미 report_list에 있다면 해당 신고는 이미 처리한 것으로 간주하고 다음 신고로 넘어감
            continue
        report_list.add(r) # 처리한 신고 이력을 report_list에 추가
        a, b = r.split() # 현재 신고 이력을 신고한 사용자와 신고 대상자로 분리
        
        reporter[a].append(b) # 신고한 사용자 a의 신고 목록에 신고 대상자 b를 추가
        reported[b] += 1 # 신고 대상자 b의 신고 횟수를 1증가
        
    ban_list = [] # 제재 대상자의 아이디를 저장할 빈 리스트를 초기화
    
    for r in reported: # 딕셔너리에 있는 각 사용자의 신고 횟수
        if reported[r] >= k: # 해당 사용자의 신고 횟수가 k보다 크거나 같으면
            ban_list.append(r) # 제재 대상으로 판단하여 ban_list에 해당 사용자의 아이디를 추가
            
    for r in reporter: # 딕셔너리에 있는 각 사용자의 신고 이력
        cnt = 0 # 해당 사용자가 제재 대상을 신고한 횟수를 저장할 변수를 초기화
        for b in ban_list: # 제재 대상으로 선정된 각 사용자에 대해 확인
            if b in reporter[r]: # 해당 사용자가 제재 대상을 신고한 경우에는 카운트를 증가
                cnt += 1 # 카운트를 증가
        answer.append(cnt) # 해당 사용자가 제재 대상을 신고한 횟수를 answer 리스트에 추가

    return answer # 제재 대상을 신고한 횟수를 계산하여 answer 리스트에 저장하는 과정을 수행
