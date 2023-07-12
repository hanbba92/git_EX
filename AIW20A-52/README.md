# AIW20A-52
## 목적
어떤 값이 급격하게 변하는 위치를 검출한다.
## 개요
값이 급격하게 변하는 위치를 convolution 기법으로 구한다.
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- input_task: 입력할 task 번호
- output_task: 출력할 task 번호

## 출력
각 좌표마다 값이 급격히 변하는 위치를 구한다. 필터는 Laplacian filter를 사용함


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2020072712.gb2.nc 700mb 51
