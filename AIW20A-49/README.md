# AIW20A-49
## 목적
wind shear 값과, 온도가 온도의 중앙값과 가까운 정도를 고려하여 해당 날짜가 전선이 있을 가능성을 점수로 나타낸다.

## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- wind_shear_task: wind shear 값이 있는 태스크 경로
- near_median_task: 온도가 중앙값과 가까운 정도를 가지는 태스크 경로
- output_task: 결과값이 쓰여질 경로
## 출력
해당 날짜에 전선이 있을 가능성을 모든 좌표상에 점수로 나타낸다.


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2020072712.gb2.nc FLOWDATA/900-600 FLOWDATA/51_500 49
