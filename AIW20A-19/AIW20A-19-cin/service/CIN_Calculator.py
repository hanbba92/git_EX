import numpy as np
from metpy.units import units
from metpy.calc import cape_cin, dewpoint_from_relative_humidity, parcel_profile

class CIN_Calculator(object):
    def get_cin(self, p, T, rh):
        p = p * units.hPa
        T = T * units.degC
        rh = rh * units.percent

        # calculate dewpoint
        Td = dewpoint_from_relative_humidity(T, rh)
        # compute parcel temperature. 숫자는 원하는 기층의 인덱스. p[2:],T[2],Td[2]-> 925기준으로 계산한 prof
        prof = parcel_profile(p[2:], T[2], Td[2]).to('degC')
        # calculate CAPE/CIN with index2
        cape, cin = cape_cin(p[2:], T[2:], Td[2:], prof)

        return cin



    def get_cin_result(self, tmp_600, tmp_700, tmp_850, tmp_925, tmp_950, tmp_1000, rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000):
        '''
        CIN 계산 함수
        사용하는 기압면 1000, 950, 925, 850, 700, 600
        :param tmp_nnn: nnn(hPa)에서의 기온
        :param rh_nnn: nnn(hPa)에서의 상대습도
        :return: CIN 계산 결과
        '''
        tmp_name_list = np.stack((tmp_1000, tmp_950, tmp_925, tmp_850, tmp_700, tmp_600))
        rh_name_list = np.stack((rh_1000, rh_950, rh_925, rh_850, rh_700, rh_600))
        p_list = [1000., 950., 925., 850., 700., 600.]

        CIN_result = []
        for i in range(0, tmp_1000.shape[1]):
            CIN = []
            for j in range(0,  tmp_1000.shape[0]):
                #한 좌표에서의 기압별 기온 리스트와 상대습도 리스트 생성
                T_list = tmp_name_list[:, i, j] - 273.15
                rh_list = rh_name_list[:, i, j]
                cin = self.get_cin(p_list, T_list, rh_list).m  # cin.m으로 유닛에서 np.float64값 얻음
                CIN.append(cin)
            CIN_result.append(CIN)
        CIN_result = np.array(CIN_result)
        return CIN_result
