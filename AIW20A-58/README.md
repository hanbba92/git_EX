# AIW20A-58
## 개요
강수가능구역이 상층제트축을 기준으로 제트입구(최대풍속지점을 기준으로 남서쪽)에 위치하는지 여부 확인
## 입력 매개변수
- workflow_id: 워크플로우 아이디 (임의로 지정).
- input_file: 입/출력할 netcdf 파일의 경로
- upper_jet_speed: 상층제트의 속도 데이터 경로
- possible_rain_area: 강수가능구역(A 또는 B)의 데이터 경로
- output_task: 출력 경로
## 출력
강수가능구역에서 '상층제트 최대풍속지점'을 기준으로 남서쪽에 존재하는 부분만 남긴다.
## 실행 방법 예시
python3 application.py flow1234 D:/nc_inuse/2021070312gb2.nc FLOWDATA/3020_250 FLOWDATA/task57 task58
