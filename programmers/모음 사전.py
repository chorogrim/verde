def solution(word):
    answer = 0
    dic = ['A', 'E', 'I', 'O', 'U'] # 문자열 구성하는 문자들을 나타내는 리스트 dic 정의
    li = [5**i for i in range(len(dic))] # 각 자리수에 해당하는 가중치를 저장하는 리스트 li 정의
    
    for i in range(len(word)-1,-1,-1): # 문자열 word의 각 문자를 오른쪽에서 왼쪽으로 반복
        idx = dic.index(word[i]) # 현재 문자 word[i]가 dic 리스트의 몇 번째 위치에 있는지를 찾기
        for j in range(5-i): # 현재 문자의 자리에 따라 해당 문자보다 앞선 자리의 가중치들을 더하기 위해 반복문 시작
            answer += li[j]*idx # 가중치 리스트 li의 각 요소에 idx를 곱하여 answer에 더함
        answer+=1 # 각 문자의 자리가 끝날 때마다 answe에 1 더함
    return answer # 모든 반복이 끝난 후 최종 계산된 answer 값을 반환
