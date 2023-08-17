# AIW-TASK-HR-3020
- 풍속을 계산하는 타스크
## 입력 매개변수
- workflow_id: 워크플로우 아이디 아무거나 넣으면 됨.
- input_file: 입/출력할 netcdf 파일 경로
- task_number: 출력할 task 번호
- input_task: u 바람성분 데이터경로, v 바람 데이터경로

## 실행 방법
python3 application.py 202306220000_hr 202306220000.nc 001 INPUTDATA/UGRD_300mb INPUTDATA/VGRD_300mb