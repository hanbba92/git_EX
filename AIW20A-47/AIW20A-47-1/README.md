# AIW20A-47-1
## 목적
제트기류의 축을 1로 표시한다. 
## 개요
일정 위도 이상의 범위에서 가장 풍속이 빠른 좌표를 1로 표시하고 나머지는 0으로 표시한다.
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- input_task: 입력할 task 번호
- output_task: 출력할 task 번호
- wind_speed_base: 제트기류축으로 볼 최소 풍속

## 출력
제트기류의 축(경도마다 가장 풍속이 강한 위치)에 1을 표시하고 나머지에는 0을 표시함


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2017071600.nc FLOWDATA/3020 47-1 30
