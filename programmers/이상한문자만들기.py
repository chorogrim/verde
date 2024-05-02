# 문자열 s는 한 개 이상의 단어로 구성되어 있습니다.
# 각 단어는 하나 이상의 공백문자로 구분되어 있습니다.
# 각 단어의 짝수번째 알파벳은 대문자로, 홀수번째 알파벳은
# 소문자로 바꾼 문자열을 리턴하는 함수, solution을 완성하세요.

def solution(s): 
    answer = '' # 결과를 저장할 빈 문자열 answer를 초기화
    words = s.split(' ') # 입력 문자열 s를 공백을 기준으로 분리하여 단어들이 리스트인 word로 만듦
    
    for word in words: # 각 단어에 대해 반복
        for i in range(len(word)): # 현재 단어에서 각 문자에 대해 반복
            if i % 2 == 0: # 현재 문자의 인덱스가 짝수인지 확인
                answer += word[i].upper() # 대문자로 변환하여 answer에 추가
            else: # 홀수번째 문자는 소문자로 변환
                answer += word[i].lower() # 소문자로 변환하여 answer에 추가
        answer += ' ' # 각 단어의 처리가 끝나면 공백 문자를 추가하여 단어를 구분
    return answer[:-1] # 마지막 공백 문자를 제외하고 answer를 반환
