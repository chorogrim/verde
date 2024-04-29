# 신입사원 무지는 게시판 불량 이용자를 신고하고 처리 결과를 메일로 발송하는
# 시스템을 개발하려 합니다. 무지가 개발하려는 시스템은 다음과 같습니다.


def solution(id_list, report, k):
    answer = []
    report_list = set()
    reporter = {}
    reported = {}
    
    for id in id_list:
        reporter[id] = []
        reported[id] = 0
        
    for r in report:
        if r in report_list:
            continue
        report_list.add(r)
        a, b = r.split()
        
        reporter[a].append(b)
        reported[b] += 1
        
    ban_list = []
    
    for r in reported:
        if reported[r] >= k:
            ban_list.append(r)
            
    for r in reporter:
        cnt = 0
        for b in ban_list:
            if b in reporter[r]:
                cnt += 1
        answer.append(cnt)

    return answer