def solution(k, tangerine):
    '''
    k: 목표 개수, 얼마나 많은 귤을 선택해야 하는지 나타냄
    tangerine: 귤의 크기를 나타내는 리스트
    '''
    answer = 0
    a={} # 각 크기별 귤의 개수를 저장할 딕셔너리 a를 초기화

    for i in tangerine: # tangerine 리스트를 반복하여 각 귤의 크기 i를 순회
        if i in a: # 현재 귤의 크기 i가 딕셔너리 a에 있다면
            a[i]+=1 # 해당 크기의 귤 개수를 1 증가

        else: # 현재 귤의 크기 i가 딕셔너리 a에 없다면
            a[i]=1 # 새로운 키로 추가하고 그 값을 1로 설정

    for i in a: # 딕셔너리 a의 각 키 i를 반복
        if k<=0: # 목표 개수 k가 0 이하가 되면
            return answer # 귤 종류 수 answer를 반환
        
        if a[i]>1: # 현재 크기의 귤 개수 a[i]가 1보다 크면
            k-=a[i] # k에서 해당 귤 개수를 뺌
            answer+=1 # 선택한 귤 종류 수 answer를 1 증가

    return answer # 모든 귤의 크기를 다 확인한 후, 최종적으로 선택한 귤 종류수 answer를 반환
