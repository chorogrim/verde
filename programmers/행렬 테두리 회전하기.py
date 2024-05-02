# 행렬의 세로 길이(행 개수) rows, 가로 길이(열 개수) columns, 그리고 회전들의 목록 queries가 주어질 때
# 각 회전들을 배열에 적용한 뒤, 그 회전에 의해 위치가 바뀐 숫자들 중 가장 작은 숫자들을 순서대로 배열에 담아
# return 하도록 solution 함수를 완성해주세요.

def solution(rows, columns, queries):
    answer = [] # 최종적으로 반환할 결과를 저장할 빈 리스트
    arr = [] # 행렬을 저장할 빈 리스트
    cnt = 1 # 시작 숫자를 나타내는 변수 cnt를 1로 초기화
    
    for _ in range(rows):# 주어진 rows 만큼 반복
        arr.append([cnt + x for x in range(columns)]) # 각 행마다 columns 개수만큼 숫자를 생성하여 행렬에 추가
        cnt += columns # 다음 행의 시작 숫자를 업데이트

    for q in queries: # 각 쿼리에 대해 반복
        x1, y1, x2, y2 = q # 쿼리에서 시작점과 끝점의 좌표를 가져옴
        x_len, y_len = x2 - x1, y2 - y1 # x와 y의 길이를 구함
        num_list = [] # 현재 쿼리에서 회전된 숫자들을 저장할 빈 리스트 
        s_x, s_y = x1 - 1, y1 - 1 # 행렬 상에서의 시작점 좌표를 설정

        tmp = arr[s_x][s_y]
        for i in range(1, y_len + 1):
            tmp = arr[s_x][s_y + i]
            num_list.append(tmp)
        s_y += y_len

        for i in range(1, x_len + 1):
            tmp = arr[s_x + i][s_y]
            num_list.append(tmp)
        s_x += x_len

        for i in range(1, y_len + 1):
            tmp = arr[s_x][s_y - i]
            num_list.append(tmp)
        s_y -= y_len

        for i in range(1, x_len + 1):
            tmp = arr[s_x - i][s_y]
            num_list.append(tmp)
        s_x -= x_len

        answer.append(min(num_list))

        cnt = -1
        for i in range(1, y_len + 1):
            arr[s_x][s_y + i] = num_list[cnt]
            cnt += 1
        s_y += y_len

        for i in range(1, x_len + 1):
            arr[s_x + i][s_y] = num_list[cnt]
            cnt += 1
        s_x += x_len

        for i in range(1, y_len + 1):
            arr[s_x][s_y - i] = num_list[cnt]
            cnt += 1
        s_y -= y_len

        for i in range(1, x_len + 1):
            arr[s_x - i][s_y] = num_list[cnt]
            cnt += 1
        s_x -= x_len

    return answer
