import re
import re
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import traceback
 
def run():    
    pkl_f = file_text.get()
    new_pkl_f= file_text.get().split(':')
    new_pkl_f = ':'.join(new_pkl_f[1:])
    pkl_f = new_pkl_f.strip()
    print(pkl_f)
    
    if pkl_f == '':
        messagebox.showwarning("경고", "파일이 선택되지 않았습니다.")
        return        

    v.set('변환 진행중..')
    root.update()

    file_nm = pkl_f.split('/')[-1].split('.')[0]
    file = open(pkl_f, "r", encoding='utf-8')
    lines = file.readlines()
    file.close()
    
    questions = []
    answers = []
    lines2 = []
    texts = []
    
    for idx, line in enumerate(lines):
        if idx != 0 and re.search('^[0-9]+$', line):
            text = ' '.join(texts)
            lines2.append(text)
            texts = []
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            temp_text = re.sub(r'<.*?>','', line.strip().replace('- ',''))
            texts.append(temp_text)
        if idx == len(lines) -1 :
            text = ' '.join(texts)
            lines2.append(text)
    for idx, line in enumerate(lines2):
        if '?' in line:
            questions.append(line)
            if idx + 1 >= len(lines2):
                answers.append('')
                continue
            answers.append(lines2[idx+1])
    result = pd.DataFrame({
        '질문' : questions,
        '답변' : answers
    })
    
    #저장할 폴더 경로
    save_path = pkl_f.split('/')[:-1]
    save_path = '/'.join(save_path)
    print(save_path)

    #저장할 파일의 전체 경로
    file_path = save_path + '/{}.xlsx'.format(file_nm)
    print(file_path)
    result.to_excel(file_path, index=False)    
    v.set('변환 및 저장 완료.')
    root.update()

def c_file():
    pkl_f = filedialog.askopenfilename(title="텍스트 파일을 선택하세요", filetypes=(("텍스트 파일", "*.txt*"), ("모든 파일", "*.*")))
    file_text.set(f'선택된 파일: {pkl_f}')
    return pkl_f

if __name__ == "__main__":
    root = Tk()

    root.title("자막txt파일 변환")
    root.geometry("400x130+810+340")
    root.resizable(False, False)

    #안내
    main_frame = Frame(root)
    main_frame.pack(fill="x", padx=5, pady=5)

    v = StringVar()
    v.set('파일을 선택 후 "변환실행" 버튼을 클릭하세요.')
    date_label = Label(main_frame, textvariable=v)
    date_label.pack(side="left", padx=5)

    btn_close = Button(main_frame, text="닫기", width=8, command=root.quit)
    btn_close.pack(side="right", padx=5)

    #변환
    foot_frame = LabelFrame(root, text="파일 정보")
    foot_frame.pack(fill="x", padx=5, pady=5, ipady=5)

    footer_frame1 = Frame(foot_frame)
    footer_frame1.pack(fill="x", padx=5)

    footer_frame2 = Frame(foot_frame)
    footer_frame2.pack(fill="x", padx=5)

    file_text = StringVar()
    file_text.set('선택된 파일: ')
    file_label = Label(footer_frame1, textvariable=file_text)
    file_label.pack(padx=5, pady=5)

    change_btn = Button(footer_frame2, text="파일 선택", command=c_file)
    change_btn.grid(row=0, column=0, padx= 80)

    run_btn = Button(footer_frame2, text="변환 실행", command=run)
    run_btn.grid(row=0, column=1, padx= 20)

    root.mainloop()
