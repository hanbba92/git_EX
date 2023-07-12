# AIW-TASK-HR-4000
- 이상치 판단 task
## 입력 매개변수
- workflow_id: 워크플로우 아이디 아무거나 넣으면 됨.
- input_file: 입/출력할 netcdf 파일 경로
- task_number: 출력할 task 번호
- input_task: 데이터 경로
- op: 컨디션 ex) >=
- base: 기준 값

## 실행 방법
python3 application.py 202306220000_hr 202306220000.nc 001 FLOWDATA/001 >= 40 

--> FLOWDATA/001 데이터 중 40 이
상인 값만 masking 해서 출력