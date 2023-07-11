# AIW20A-50
## 목적
vertical wind shear를 검출한다.
## 개요
각 좌표마다 vertical wind shear를 검출한다. 구한다.
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- input_task_0: 베이스 등압면 레벨
- input_task_1: 비교 드압면 레벨


## 출력
각 좌표마다 convolution으로 주변 바람 벡터와의 차이의 L2 Norm 을 구한다.


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2020072712.gb2.nc 1000 500
