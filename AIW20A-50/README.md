# AIW20A-50
## 목적
vertical wind shear를 검출한다.
## 개요
각 좌표마다 vertical wind shear를 검출한다. 구한다.
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- DZDT: 수직방향 바람성분 변수이름
- UGRD: 동서방향 바람성분 변수이름
- VGRD: 남북방향 바람성분 변수이름
- output_task: 출력할 task 번호

## 출력
각 좌표마다 convolution으로 주변 바람 벡터와의 차이의 L2 Norm 을 구한다. 필터는 Laplacian filter를 사용함


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2020072712.gb2.nc DZDT_700mb UGRD_700mb VGRD_700mb
