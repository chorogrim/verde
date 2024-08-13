import os

# 폴더명 src_폴더에서 compare폴더에 이름이 같은 파일을만 남기고 삭제
src_folder = 'C:\\Users\\user\\Desktop\\한글 차트\\차트 해석'
compare_folder = 'C:\\Users\\user\\Desktop\\한글 차트\\차트 이미지'

src_files = os.listdir(src_folder)
compare_files = os.listdir(compare_folder)

# Remove file extensions from chartdata_files and chartanalysis_files
src_files = [os.path.splitext(file)[0] for file in src_files]
compare_files = [os.path.splitext(file)[0] for file in compare_files]


# src폴더에서 compare폴더에 존재하는 파일만 체크
files_to_keep = []
for file in src_files:
    if file in compare_files:
        files_to_keep.append(file)

# 파일명이 중복되는 개수
# print(len(files_to_keep))
# 파일명이 다른 파일 삭제
for file in src_files:
    if file not in files_to_keep:
        file = file + '.xlsx'
        file_path = os.path.join(src_folder, file)        
        try:
            os.remove(file_path)            
        except:
            pass