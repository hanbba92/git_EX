# AIW20A-56
## 개요
강풍 중심을 통과하는 유선이나 제트축을 기준으로 호우 발생 가능 지역(A, B)확인
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (아무거나 넣으면 됨).
- input_file: 입/출력할 netcdf 파일의 경로
- LLJ_axis: 하층 제트축 데이터 경로
- wind_speed: 풍속 데이터 경로
- output_task: 출력할 데이터 경로

## 출력
제트축의 위에있고, 풍속이 15kts, 즉 7.71667m/s이상인 위치를 A 또는 B로 삼고 1로 표시한다.
## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2021070312gb2.nc FLOWDATA/47-1 FLOWDATA/3020 task56
