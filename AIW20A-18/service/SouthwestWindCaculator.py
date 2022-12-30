import numpy as np
import math

class SouthwestWindCalculator(object):

    def get_sw_wind_speed(self, u, v):
        sw_wspd = 0
        if u > 0 and v > 0:
            sw_wspd = math.sqrt(u**2 + v**2)
        return sw_wspd

    def get_sw_wind_speed_result(self, u_wind, v_wind):
        sw_wspd_result = []
        for u_wind_1d, v_wind_1d in zip(u_wind, v_wind):
            sw_wspd_result_1d = []
            for Ucomp, Vcomp in zip(u_wind_1d, v_wind_1d):
                sw_wspd = self.get_sw_wind_speed(Ucomp, Vcomp)
                sw_wspd_result_1d.append(sw_wspd)
            sw_wspd_result.append(sw_wspd_result_1d)
        return np.array(sw_wspd_result)