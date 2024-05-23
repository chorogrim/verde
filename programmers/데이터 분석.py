def solution(data, ext, val_ext, sort_by): # data: 필터링 및 정렬할 데이터 리스트, ext: 필터링 되는 열 이름, val_ext: 필터링 기준 값, sort_by: 정렬 기준이 되는 열 이
    answer = []
    dict = {'code':0, 'date':1, 'maximum':2, 'remain':3} # 각 열 이름을 인덱스로 매핑하는 사전을 정의
    for d in data:
        value = d[dict[ext]] # 현재 항목 d에서 필터링 기준 열의 값을 가져옴
        if value <= val_ext: # 필터링 기준 값 value가 주어진 기준 값 val_ext 보다 작거나 같은지 확인
            answer.append(d) # 조건이 참이면 현재 항목 d를 결과 리스트 answer에 추가
    answer.sort(key = lambda x : x[dict[sort_by]]) # 결과 리스트 answer를 정렬
    return answer # 필터링 되고 정렬된 결과 리스트를 반환
