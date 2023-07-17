# AIW20A-52
## 개요
바람벡터를 주어진 각도를 가진 단위벡터와 내적한다.
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- ugrd_task: 입력할 u성분 바람의 task 번호
- vgrd_task: 입력할 v성분 바람의 task 번호
- base_degree: 단위벡터의 각도
- output_task: 출력할 task 번호

## 출력
각 좌표마다 단위벡터와 내적한 값을 저장함. 


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2020072712.gb2.nc UGRD_850mb VGRD_850mb 40 task52