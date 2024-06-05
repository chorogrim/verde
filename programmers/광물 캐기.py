def solution(picks, minerals):
    '''
    piacks, minerals: 최적의 점수를 계산하는 함수
    '''
    answer = 0 # 최종 점수 저장
    mineralSort = [] # 특정 개수만큼 minerals를 다이아몬드, 철, 돌 순으로 정렬한 리스트를 저장하는데 사용

    ableDigAmont = min(sum(picks) * 5, len(minerals)) # 총 파낼 수 있는 광물의 최대 개수
    diaCnt, ironCnt, stoneCnt = 0, 0, 0 # 다이아몬드, 철, 돌의 개수를 세기 위한 변수

    for i in range(ableDigAmont): # ableDigAmont만큼 순회하면서 각 광물의 종류를 확인하고 개수 세어줌
        if minerals[i] == 'diamond':
            diaCnt += 1
        elif minerals[i] == 'iron':
            ironCnt += 1
        elif minerals[i] == 'stone':
            stoneCnt += 1

        if (i + 1) % 5 == 0 or i == ableDigAmont -1: # 매 5개씩 묶거나 마지막 인덱스일 때
            mineralSort.append((diaCnt, ironCnt, stoneCnt)) # 현재까지 센 다이아몬드, 철, 돌의 개수를 mineralSort에 추가하고
            diaCnt, ironCnt, stoneCnt = 0, 0, 0 # 카운터를 초기화

    mineralSort.sort(key = lambda x : (x[0], x[1], x[2]), reverse = True) # mineralSort 리스트를 다이아몬드, 철, 돌의 개수를 기준으로 내림차순 정렬

    i = 0
    for diaCnt, ironCnt, stoneCnt in mineralSort: # picks에서 사용할 수 있는 곡괭이 찾기
        while picks[i] == 0: # picks[i]가 0이면 다음 곡갱이로 넘어감
            i += 1

        if i == 0:
            answer += (diaCnt + ironCnt + stoneCnt) # 첫 번째 다이아몬드는 다이아몬드, 철, 돌의 개수만큼 점수를 더함
        elif i == 1:
            answer += (diaCnt * 5 + ironCnt + stoneCnt) # 두 번째 철은 다이아몬트 개수에 5를 곱한 값, 철, 돌의 개수만큼 점수를 더함
        elif i == 2:
            answer += (diaCnt * 25 + ironCnt * 5 + stoneCnt) # 세 번째 돌은 다이아몬트 개수에 25를 곱한 값, 철 개수에 5를 곱한 값, 돌의 개수만큼 점수를 더함

        picks[i] -= 1 # 사용한 곡괭이의 개수를 하나 줄임

    return answer # 최종적으로 계산된 answer를 반환