import unittest

import numpy as np

from service.DewPointCalculator import DewPointCalculator
from file.file_manager import FileManager


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.fm = FileManager()
        self.input_file = 'C:/Users/p/Desktop/aiw-hr-task/aiw_task_hr_input_20220207.nc'
        self.output_tasks = '1'
        self.base = 20
        self.data = self.fm.read(self.input_file)

    def test_AbsoluteTmp_to_DegreeCelsius(self):
        tmp_925, rh_925 = self.data['tmp_925'], self.data['rh_925']

        tmp_925 = tmp_925 - 273.15

        print(tmp_925)

        # 섭씨온도 netcdf file
        self.fm.write(self.input_file, [self.data['latitude'], self.data['longitude'], tmp_925], task_number=self.output_tasks)

    def test_tmp_above20(self):
        tmp_925, rh_925 = self.data['tmp_925'], self.data['rh_925']

        tmp_925 = tmp_925 - 273.15

        tmp_925 = np.array(tmp_925)
        tmp_925[tmp_925 < self.base] = self.base -1
        print(tmp_925)

        # 섭씨온도 20도 이상 netcdf file
        self.fm.write(self.input_file, [self.data['latitude'], self.data['longitude'], tmp_925], task_number=self.output_tasks)

    def test_tmp_above20_mask(self):
        tmp_925, rh_925 = self.data['tmp_925'], self.data['rh_925']

        tmp_925 = tmp_925 - 273.15

        tmp_925 = np.array(tmp_925) >= self.base
        print(tmp_925)

        # 섭씨온도 20도 이상 netcdf file
        self.fm.write(self.input_file, [self.data['latitude'], self.data['longitude'], tmp_925], task_number=self.output_tasks)

    def test_rh_above85(self):
        tmp_925, rh_925 = self.data['tmp_925'], self.data['rh_925']

        rh_925 = np.array(rh_925)
        rh_925[rh_925 < 85] = 84

        # 상대습도 85 이상 netcdf file
        self.fm.write(self.input_file, [self.data['latitude'], self.data['longitude'], rh_925], task_number=self.output_tasks)

    def test_rh_above85_mask(self):
        tmp_925, rh_925 = self.data['tmp_925'], self.data['rh_925']

        rh_925 = np.array(rh_925) >= 85

        # 상대습도 85 이상 netcdf file
        self.fm.write(self.input_file, [self.data['latitude'], self.data['longitude'], rh_925], task_number=self.output_tasks)

    def test_dewpointCalculator(self):
        """이슬점 계산 메소드 테스트"""
        dewpoint_cal = DewPointCalculator()
        self.assertEqual(dewpoint_cal.get_dew_point(20, 100), 20)


if __name__ == '__main__':
    runner = unittest.TextTestRunner



