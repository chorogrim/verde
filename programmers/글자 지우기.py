def solution(my_string, indices):
    string_list = list(my_string) # 입력된 문자열을 리스트로 변환
    indices.sort() # 인덱스 리스트 정렬
    indices.reverse() # 정렬된 인덱스 리스트 역순으로 뒤집기
    
    for idx in indices: # 정렬된 역순의 인덱스 리스트를 순회
        del string_list[idx] # 해당 인덱스의 문자 삭제
    
    return ''.join(string_list) # 삭제된 문자가 있는 문자열 리스트를 다시 문자열로 결합하여 반환
