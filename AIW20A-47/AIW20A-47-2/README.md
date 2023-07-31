# AIW20A-47-2
## 목적
극 제트기류축이 위도 X 이상에만 있는지 판단한다.

## 개요
지도상에 1로 표시된 위치가 모두 일정 위도 이상이면 1을, 아니면 0을 표시한다.

## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일 경로
- input_task: 입력할 task 번호
- output_task: 출력할 task 번호
- lat_base: 하한이 될 위도 X

## 출력
극 제트기류축이 위도 X 이상에만 있으면 1을 모든 좌표에 입력하고 아니면 0을 입력한다.


## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2017071600.nc FLOWDATA/47-1 47-2 40
