# n개의 로봇이 각각 주어진 시간 내에 주어진 작업을 끝낼 수 있는지 여부를 판단하는 문제

# 반복 작업에 걸리는 시간을 계산하는 함수
def calculate_time(size, repeat):

    # 만약 반복 횟수가 0인 경우를 처리
    if repeat == 0:

        # 작업을 수행하는데 걸리는 시간 1
        return 1
    
    # 작업의 크기를 주어진 반복 횟수만큼 거듭제곱한 값을 반환
    # (= 작업을 반복하여 수행할 때 걸리는 시간을 계산)
    return size ** repeat

# 각 로봇이 주어진 작업을 완료할 수 있는지 알려주는 함수
# (주어진 작업의 크기, 시간 제한, 그리고 반복 작업 형태를 담기)
def solution(sizes, limits, tasks):

    # 결과를 담을 빈 리스트 선언
    result = []

    # 각 로봇에 대한 작업을 반복 (zip 함수를 사용)
    # sizes, limits, tasks 배열들을 반복하며 각 로봇의 대한 정보를 가져오기
    for size, limit, task in zip(sizes, limits, tasks):

        # 총 total_time = 0 으로 초기화
        # (로봇의 작업을 수행하는데 필요한 시간을 저장)
        total_time = 0

        # 작업 문자열을 한 글자씩 반복
        for char in str(task):

            # 숫자인지 아닌지 확인하는 함수
            if char.isdigit(): 

                # 숫자라면, 글자를 정수로 변환하여 해당 작업을 수행하는데 필요한 시간을 계산하고 total_time에 더함
                total_time += calculate_time(size, int(char))

        # 주어진 시간 내에 작업을 끝낼 수 있는지 확인
        if total_time <= limit:  

            # 작업 완료할 수 있다면 result에 1 추가
            result.append(1) 
        
        # 그렇지 않다면
        else:
            # result에 0을 추가
            result.append(0) 

    # result 리스트를 반환하여 각 로봇의 작업 완료 여부를 나타내는 결과를 얻기
    return result 


# 번호 순서가 빠른대로 1차원 정수 배열에 담아 반환하는 함수
def get_ordered_result(sizes, limits, tasks):
    
    # 주어진 solution() 함수를 사용하여 입력값을 처리하고 결과를 반환
    result = solution(sizes, limits, tasks)
    
    # 반환된 결과를 sorted() 함수를 사용하여 오름차순으로 정렬
    return sorted(result)


# input
sizes = [10, 2, 13, 1]
limits = [300, 31, 100, 5]
tasks = ["3tt", "4ttt", "8t", "4ttttt"]
# output
print(get_ordered_result(sizes, limits, tasks))

# input
sizes = [100, 100, 100]
limits = [1000000000, 100, 3]
tasks = ["9tttt", "1t", "4"]
# output
print(get_ordered_result(sizes, limits, tasks))