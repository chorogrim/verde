def solution(stones, k):
    '''
    stones: 징검다리의 각 돌의 내구도를 나타내는 리스트
    k: 연속으로 건너뛸 수 있는 최대 거리
    '''
    answer = 0
    s = 1 # 이진 탐색의 시작 값
    e = max(stones) # e를 stones 리스트의 최대 값으로 초기화
    
    while s <= e:
        # mid 명이 건넌 후 다음 사람이 건널 수 있는가?
        mid = (s+e)//2 
        # 몇칸씩 건너는지
        l = []
        cnt = 1
        for i in range(len(stones)):
            # mid 명이 건넜으니
            # 밟을 수 없는 돌 -> 건너뛰기
            if mid >= stones[i]:
                cnt += 1
            else:
                l.append(cnt)
                cnt = 1
        # 마지막 건너뛰기
        l.append(cnt)
        # 건너뛸 수 있는 최대보다 크면 다 못 건넌다... -> 사람 줄이자
        if max(l) > k:
            e = mid - 1
        # 다 건널 수 있다 -> 사람 늘려보자 + (mid+1)값 저장
        else:
            s = mid + 1
            answer = mid+1
    return answer
