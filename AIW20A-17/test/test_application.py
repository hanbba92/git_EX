import unittest

import numpy as np

from service.wind_direction_calculator import WindDirectionCalculator
from file.file_manager import FileManager


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.fm = FileManager()
        self.input_file = 'C:/Users/p/Desktop/aiw-task-hr/netcdf/aiw-task-hr-17-nc/aiw_task_hr_input_20220207.nc'
        self.output_tasks = '1'
        self.base1 = 180
        self.base2 = 230
        self.data = self.fm.read(self.input_file)

    def test_wind_direction_calculator(self):
        wind_direction_cal = WindDirectionCalculator()
        self.assertEqual(wind_direction_cal.get_wind_direction(10.0, 10.0), 225.0)
        self.assertEqual(wind_direction_cal.get_wind_direction(0.0, 10.0), 180.0)
        self.assertEqual(wind_direction_cal.get_wind_direction(0.0, -10.0), 360.0)


if __name__ == '__main__':
    runner = unittest.TextTestRunner



