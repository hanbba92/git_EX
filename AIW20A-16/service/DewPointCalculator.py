import math


class DewPointCalculator(object):

    def get_dew_point(self, tmp, rh):
        b = 17.62
        c = 243.12
        gamma = ((b * tmp) / (c + tmp)) + math.log(rh / 100.0)
        dewpoint = (c * gamma) / (b - gamma)
        return dewpoint

    def get_dew_point_result_list(self, tmp_list, rh_list):
        dewpoint_list = []
        for (tmp_1d, rh_1d) in zip(tmp_list, rh_list):
            dewpoint_list_1d = []
            for tmp, rh in zip(tmp_1d, rh_1d):
                dewpoint_list_1d.append(self.get_dew_point(tmp, rh))
            dewpoint_list.append(dewpoint_list_1d)
        return dewpoint_list
