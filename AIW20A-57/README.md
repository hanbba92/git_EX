# AIW20A-57
## 개요
A, B 지역 상공 200hPa 혹은 300hPa에 제트기류 위치 여부 확인
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (임의로 지정).
- input_file: 입/출력할 netcdf 파일의 경로
- A_or_B_area: A 또는 B 지역의 위치가 1로 표시된 데이터 경로
- wind_speed: 풍속 데이터 경로
- output_task: 출력할 데이터 경로
- upper_jet_base: 하층제트라고 볼 최소 풍속. 보통 40m/s를 적용함

## 출력
A_or_B_area 에 표시된 위치에서 제트기류의 위치가 존재하는 지역을 1로 표시한다.
## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2021070312gb2.nc FLOWDATA/task56 FLOWDATA/3020 task57 40
