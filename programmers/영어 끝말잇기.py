def solution(n, words):
    '''
    n: 참여자 수
    words: 단어 리스트
    '''
    checked = [words[0]] # 이미 사용된 단어들 저장
    
    for i in range(1, len(words)): # 첫 번째 단어 이후의 단어들 순회
        if words[i][0] == words[i-1][-1] and words[i] not in checked: # 현재 단어의 첫 글자가 이전 단어의 마지막 글자와 같고, 현재 단어가 checked 리스트에 없다면
            checked.append(words[i]) # checked 리스트에 현재 단어 추가
        else: # 위의 조건을 만족하지 않으면
            return [(i%n)+1, (i//n)+1] # (i%n)+1은 규칙을 어긴 사람이 몇 번째 사람인지를 나타냄, (i//n)+1은 몇 번째 차례인지를 나타냄
    return [0,0] # 모든 단어가 규칙을 잘 지켰다면 [0,0]을 반환