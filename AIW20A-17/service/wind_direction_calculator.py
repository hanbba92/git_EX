import math


class WindDirectionCalculator(object):

    def get_wind_direction(self, u, v):
        r2d = 180 / math.pi
        wind_direction = math.atan2(u, v) * r2d + 180
        return wind_direction

    def get_wind_direction_result_list(self, u_list, v_list):
        wind_direction_list = []
        for (u_1d, v_1d) in zip(u_list, v_list):
            wind_direction_list_1d = []
            for (u, v) in zip(u_1d, v_1d):
                wind_direction_list_1d.append(self.get_wind_direction(u, v))
            wind_direction_list.append(wind_direction_list_1d)
        return wind_direction_list