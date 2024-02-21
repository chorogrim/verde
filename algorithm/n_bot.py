# 주어진 작업 형태, 작업 크기를 이용해 해당 작업을 수행하는데 걸리는 시간 계산 함수 정의
def calculate_time(task, size):
    
    # 문자열 task에서 문자 't'의 개수를 세어 이어 붙인 작업의 개수를 구함
    t_count = task.count('t')
    
    # 문자열 task에서 't'를 모두 제거한 후, 남은 문자열을 정수로 변환하여 반복 횟수 k를 구함
    k = int(task.replace('t', ''))
    
    # 반복 횟수 k와 작업 크기를 이용하여 작업에 걸리는 시간을 계산
    return k * (size ** t_count)

# 각 로봇이 주어진 시간 내에 작업을 완료할 수 있는지를 판단하는 함수 정의
def solution(sizes, limits, tasks):
    
    # 결과를 담을 빈 리스트 선언
    results = []
    
    # 각 로봇에 대해 작업에 걸리는 총 시간을 계산
    for i in range(len(sizes)):
        
        time_limit = limits[i]  # 주어진 시간 제한
        task = tasks[i]         # 반복 작업 형태
        size = sizes[i]         # 작업 크기
        
        # 작업에 걸리는 총 시간 계산
        total_time = calculate_time(task, size)  
        
        # 작업에 걸리는 총 시간이 주어진 시간 제한 이내에 있는지 확인
        if total_time <= time_limit:
            
             # 끝낼 수 있다면 result에 1 추가
            results.append(1) 
        else:
            # 그렇지 않다면 result에 0 추가
            results.append(0) 
            
    # 결과 리스트 반환
    return results

# input
sizes = [10, 2, 13, 1]
limits = [300, 31, 100, 5]
tasks = ["3tt", "4ttt", "8t", "4ttttt"]
# output
print(solution(sizes, limits, tasks)) 

# input
sizes = [100, 100, 100]
limits = [1000000000, 100, 3]
tasks = ["9tttt", "1t", "4"]
# output
print(solution(sizes, limits, tasks)) 