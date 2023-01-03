from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import datetime


class KMA:
    def __init__(self, driver_path, download_path, options=Options()):
        self.driver_path = driver_path
        self.down_dir = download_path
        self.options = options
        options.add_experimental_option("prefs", {
            "download.default_directory": self.down_dir})

    def setting(self):
        try:
            self.driver.quit()
        except:
            1
        self.driver = webdriver.Chrome(self.driver_path, options=self.options)
        self.driver.get('https://data.kma.go.kr/cmmn/main.do')

    def login(self, kma_id, kma_pass):
        try:
            self.driver.maximize_window()
            self.driver.find_element_by_css_selector('a#loginBtn').click()
            self.driver.find_element_by_css_selector('input#loginId.inp').send_keys(kma_id)
            self.driver.find_element_by_css_selector('input#passwordNo.inp').send_keys(kma_pass)
            self.driver.find_element_by_css_selector('button#loginbtn.btn_login').click()
            print('Login complete')
            return True
        except:
            print('Already logged in')
            return False

    def logout(self):
        try:
            self.driver.maximize_window()
            self.driver.find_element_by_css_selector('a#logoutBtn').click()
            print('Logout complete')
            return True
        except:
            print('Already logged out')
            return False

    def login_loof(self, kma_id, kma_pass):
        self.logout()
        sleep(0.5)
        self.login(kma_id, kma_pass)
        sleep(0.5)

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def search_data(self, weather_type, start_day, end_day):
        """
        기상자료개방포털에서 검색 조건 설정 후 검색하는 함수
        :return: None
        """
        print('Start crawling...')
        """ 사이트 이동 """
        self.driver.get(f'https://data.kma.go.kr/data/weatherReport/wsrList.do?pgmNo=')

        """ 시작 기간 설정 """
        self.driver.execute_script('document.querySelector("input[id=startDt]").removeAttribute("readonly")')
        self.driver.execute_script(f'document.querySelector("input[id=startDt]").value = "{start_day}"')

        """ 끝 기간 설정 """
        self.driver.execute_script('document.querySelector("input[id=endDt]").removeAttribute("readonly")')
        self.driver.execute_script(f'document.querySelector("input[id=endDt]").value = "{end_day}"')

        """ 전체 지점 선택 """
        if self.driver.find_element_by_css_selector('a#ztree1_1_check').get_attribute('title') == '전체선택 안됨':
            self.driver.find_element_by_css_selector('a#ztree1_1_check').click()

        """ 기상 선택 """
        self.driver.find_element_by_css_selector('a#ztree_2_switch').click()
        if weather_type == '폭염':
            if self.driver.find_element_by_css_selector('a#ztree_6_check').get_attribute('title') == '폭염선택 안됨':
                element = self.driver.find_element_by_css_selector('#ztree_6_check')
                self.driver.execute_script("arguments[0].click();", element)
        elif weather_type == '호우':
            if self.driver.find_element_by_css_selector('a#ztree_9_check').get_attribute('title') == '호우선택 안됨':
                element = self.driver.find_element_by_css_selector('#ztree_9_check')
                self.driver.execute_script("arguments[0].click();", element)

        elif weather_type == '강풍':
            if self.driver.find_element_by_css_selector('a#ztree_13_check').get_attribute('title') == '강풍선택 안됨':
                element = self.driver.find_element_by_css_selector('#ztree_13_check')
                self.driver.execute_script("arguments[0].click();", element)
        else:
            print('기상을 선택해야합니다. (폭염, 호우, 강풍)')

        """ 출력 개수 선택"""
        self.driver.execute_script(
            'document.querySelector("select#selectSchListCnt > option:nth-child(10)").setAttribute("selected", "selected")')

        """ 조회 """
        self.driver.execute_script('searchData();')
        sleep(1)

    def make_one_newsflash_data(self, weather_type, announcement_time, area, fermentation_time_list,
                                concerned_area_list):
        data_list = []
        for i in range(len(fermentation_time_list)):
            if weather_type in fermentation_time_list[i]:
                data = []
                # 발효 시각
                fermentation_time = fermentation_time_list[i].split(':')[1].strip()
                fermentation_time = datetime.strptime(fermentation_time, '%Y년 %m월 %d일 %H시 %M분')
                fermentation_time = datetime.strftime(fermentation_time, '%Y-%m-%d %H:%M')
                # 특보 유형 (주의보/경보)
                newsflash_type = fermentation_time_list[i].split(':')[0].split()[1]
                # 해당 지역
                concerned_area = concerned_area_list[i].split(':')[1].strip()
                # 비고
                note = fermentation_time_list[i].split(':')[0].split()[2].strip()
                # print(newflash_type, announcement_time, area, fermentation_time, concerned_area, note)
                data.append(newsflash_type)
                data.append(announcement_time)
                data.append(area)
                data.append(fermentation_time)
                data.append(concerned_area)
                data.append(note)
                data_list.append(data)
        return data_list

    def file_download(self, weather_type, start_day, end_day):
        """
        크롤링한 엑셀 파일 다운로드 함수
        """

        """ 사이트 데이터 검색 """
        self.search_data(weather_type, start_day, end_day)

        """ 다운로드 및 페이지 이동 """
        # 다운로드 클릭
        self.driver.find_element_by_css_selector(
            '#wrap_content > div.wrap_itm.area_data > div.hd_itm > div > a').click()
        sleep(1)
        # 용도 신청 팝업 및 다운로드 다이얼로그 처리
        if self.driver.find_element_by_css_selector('#wrap-datapop'):
            self.driver.execute_script(
                'document.querySelector("#reqstPurposeCd10").setAttribute("checked", "checked")')
            self.driver.execute_script('fnRltmRequest();')
            sleep(2)
            # pyautogui.press('enter')
        sleep(2)
        print('Download complete.')

    def clean_up_exel_raw_data(self, raw_data, weather_type):
        """
        다운로드 받은 파일 데이터 정리 함수
        :return: 정리된 데이터
        """
        print('Processing data...')
        clean_data = []
        row = 0
        while row < len(raw_data):
            announcement_time = datetime.strftime(raw_data.loc[row+1, 0], '%Y-%m-%d %H:%M')
            area = raw_data.loc[row+1, 1]

            """ 발효 시각 수집 """
            fermentation_time_idx = 0
            fermentation_time_list = []
            while True:
                fermentation_time_list.append(raw_data.loc[row + 3 + fermentation_time_idx, 0])
                if raw_data.loc[row+3+fermentation_time_idx+1, 0] == '해당지역': # 발효 시각 데이터가 끝났는지 확인
                    break
                fermentation_time_idx = fermentation_time_idx + 1

            """ 해당 지역 수집 """
            concerned_area_list = []
            concerned_area_idx = 0
            while True:
                concerned_area_list.append(raw_data.loc[row + 5 + fermentation_time_idx + concerned_area_idx, 0])
                if raw_data.loc[row + 5 + fermentation_time_idx + concerned_area_idx+1, 0] == '내용': # 해당 지역이 끝났는지 확인
                    break
                concerned_area_idx = concerned_area_idx + 1

            """ 내용 개수 수집"""
            contents_idx = 0
            while True:
                concerned_area_list.append(raw_data.loc[row + 7 + fermentation_time_idx + concerned_area_idx + contents_idx, 0])
                # 내용 데이터가 끝났거나 더이상 데이터가 없는지 확인
                if row + 7 + fermentation_time_idx + concerned_area_idx + contents_idx + 1 == len(raw_data) or \
                        raw_data.loc[row + 7 + fermentation_time_idx + concerned_area_idx + contents_idx + 1, 0] == '발표시각':
                    break
                contents_idx = contents_idx + 1

            """ 데이터 수집 """
            data_list = self.make_one_newsflash_data(weather_type, announcement_time, area, fermentation_time_list, concerned_area_list)
            clean_data = clean_data + data_list
            row = row + 8 + fermentation_time_idx + concerned_area_idx + contents_idx
        return clean_data

    def crawling_data(self, weather_type, start_day, end_day):
        """
        데이터 검색 후 크롤링만으로 데이터 수집하는 함수
        :return: 크롤링한 데이터 목록
        """
        """ 사이트 데이터 검색 """
        self.search_data(weather_type, start_day, end_day)

        """ 페이지 이동 및 데이터 추출"""
        newsflash_detailsInfo_list = []
        page_num = 1
        while(True):
            try:
                newsflash_list = self.driver.find_elements_by_css_selector(
                    '#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.wrap_tbl > table > tbody > tr')
                newsflash_detailsInfo_list = newsflash_detailsInfo_list + self.extract_data(weather_type, newsflash_list)
                page_num = page_num + 1
                self.driver.execute_script(f'changePage({page_num});')
                sleep(1)
            except NoSuchElementException:
                break
        print("Data extraction complete")
        return newsflash_detailsInfo_list

    def extract_data(self, weather_type, newsflash_list):
        """
        한 페이지 내의 특보 리스트 세부정보 수집
        """
        newsflash_detailsInfo_list = []
        for idx in range(1, len(newsflash_list)+1):
            detailsInfo = self.open_detailsInfo(idx, weather_type)
            newsflash_detailsInfo_list = newsflash_detailsInfo_list + detailsInfo
        return newsflash_detailsInfo_list

    def open_detailsInfo(self, index, weather_type):
        """
        한개의 특보에 대한 데이터 수집
        """
        # 특보 세부정보 열기
        self.driver.find_element_by_css_selector(f'#wrap_content > div.wrap_itm.area_data > div.cont_itm > div.wrap_tbl > table > tbody > tr:nth-child({index}) > td.col_more > a').click()
        sleep(0.4)

        data_list = []

        # 발표 시각
        announcement_time = self.driver.find_element_by_css_selector('#wrap-datapop > div > div.cont_layer.box > div:nth-child(1) > div').text

        # 지역
        area = self.driver.find_element_by_css_selector('#wrap-datapop > div > div.cont_layer.box > div:nth-child(2) > div').text

        # 발효 시각 여러개
        fermentation_time_series = self.driver.find_element_by_css_selector('#wrap-datapop > div > div.cont_layer.box > div:nth-child(3) > div').text

        # 해당 지역 여러개
        concerned_area_series = self.driver.find_element_by_css_selector('#wrap-datapop > div > div.cont_layer.box > div:nth-child(4) > div').text

        # 특보 분리
        fermentation_time_list = fermentation_time_series.split('\n')
        concerned_area_list = concerned_area_series.split('\n')

        # 하나의 특보에 대한 데이터 리스트
        one_newsflash_data = self.make_one_newsflash_data(weather_type, announcement_time, area, fermentation_time_list, concerned_area_list)

        data_list = data_list + one_newsflash_data

        # 특보 세부정보 닫기
        self.driver.find_element_by_css_selector('#wrap-datapop > div > div.hd_layer > button').click()
        sleep(0.3)

        return data_list