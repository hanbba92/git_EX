import numpy as np
import math

class WetBulbCalculator(object):

    def get_wet_bulb_temp(self, tmp, rh):
        mid1 = 0.151977 * (rh + 8.313659)**(1/2)
        mid2 = 0.00391838 * rh**(3/2) * math.atan(0.023101 * rh)
        wet_bulb_temp = tmp * math.atan(mid1) + math.atan(tmp + rh) - math.atan(rh - 1.67633) + mid2 - 4.686035
        return wet_bulb_temp

    def get_wet_bulb_temp_result(self, tmp_1D5maboveground, rh_1D5maboveground):
        wet_bulb_result = []
        ####
        for tmp_1D5maboveground_1d, rh_1D5maboveground_1d in zip(tmp_1D5maboveground, rh_1D5maboveground):
            wet_bulb_result_1d = []
            for tmp, rh in zip(tmp_1D5maboveground_1d, rh_1D5maboveground_1d):
                wet_bulb = self.get_wet_bulb_temp(tmp, rh)
                wet_bulb_result_1d.append(wet_bulb)
                ###
            wet_bulb_result.append(wet_bulb_result_1d)
        return np.array(wet_bulb_result)