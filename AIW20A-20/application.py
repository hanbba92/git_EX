from kma import KMA
from excel_file_manager import ExcelFileManager


class Application:
    def __init__(self, driver_path, kma_id, kma_pass, download_path):
        self.driver_path = driver_path
        self.kma_id = kma_id
        self.kma_pass = kma_pass
        self.download_path = download_path

    def run(self):
        # 검색 조건
        start_day = '20210101'
        end_day = '20211231'
        weather_type = '강풍'

        # 엑셀 파일 다운로드 방식
        data = self.file_download_method(weather_type, start_day, end_day)

        # 사이트 크롤링 방식
        # data = self.crawling_data_method(weather_type, start_day, end_day)

        header = ['특보 유형', '발표 시각', '지역', '발효 시각', '해당 지역', '구분', '시각 차이']

        excel_file_manager = ExcelFileManager()
        file_name = weather_type + '_' + start_day + '_' + end_day + '.xlsx'
        excel_file_manager.file_write(title=weather_type, file_name=file_name, data_list=data, header=header)

    def file_download_method(self, weather_type, start_day, end_day):
        kma = KMA(driver_path=self.driver_path, download_path=self.download_path)

        kma.setting()
        kma.login_loof(kma_id=self.kma_id, kma_pass=self.kma_pass)

        # 다운로드 받을 경로 비우기
        file_manager = ExcelFileManager()
        file_manager.directory_empty(self.download_path)

        # 파일 다운로드
        kma.file_download(weather_type, start_day, end_day)
        kma.quit()

        # 다운로드 받은 파일 읽기
        full_file_path = file_manager.file_name_read(self.download_path)
        raw_data = file_manager.file_read(full_file_path)

        # 읽은 데이터 가공
        clean_data = kma.clean_up_exel_raw_data(raw_data, weather_type)

        return clean_data

    def crawling_data_method(self, weather_type, start_day, end_day):
        kma = KMA(driver_path=self.driver_path, download_path=self.download_path)

        kma.setting()
        kma.login_loof(kma_id=self.kma_id, kma_pass=self.kma_pass)

        data = kma.crawling_data(weather_type, start_day, end_day)
        kma.quit()

        return data


def main():
    # 개인 설정
    chrome_driver_path = r'c:\Users\~\chromedriver.exe'
    kma_id = 'id'
    kma_pass = 'password'
    download_path = r'C:\Users\~\downloads\strong-wind'

    a = Application(driver_path=chrome_driver_path, kma_id=kma_id, kma_pass=kma_pass, download_path=download_path)
    a.run()


if __name__ == '__main__':
    main()