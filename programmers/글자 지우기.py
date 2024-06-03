def solution(my_string, indices):
    '''
    my_string: 문자열
    indices: 삭제할 문자의 인덱스
    '''
    string_list = list(my_string) # 입력된 문자열을 리스트로 변환
    indices.sort() # 인덱스 리스트 정렬
    indices.reverse() # 정렬된 인덱스 리스트 역순으로 뒤집기
    
    for idx in indices: # 정렬된 역순의 인덱스 리스트를 순회
        del string_list[idx] # 해당 인덱스의 문자 삭제
