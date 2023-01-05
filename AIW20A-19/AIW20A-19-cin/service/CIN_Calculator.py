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
        # compute parcel temperature. 숫자는 원하는 기층의 인덱스. p[2:],T[2],Td[2]가 되면 925기준으로 계산한 prof나옴
        prof = parcel_profile(p, T[2], Td[2]).to('degC')
        # calculate CAPE/CIN
        cin = cape_cin(p, T, Td, prof)

        return cin



    def get_cin_result(self, tmp_600, tmp_700, tmp_850, tmp_925, tmp_950, tmp_1000, rh_600, rh_700, rh_850, rh_925, rh_950, rh_1000):
        '''
        CIN 계산 함수
        사용하는 기압면 1000, 950, 925, 850, 700, 600
        :param tmp_nnn: nnn(hPa)에서의 기온
        :param rh_nnn: nnn(hPa)에서의 상대습도
        :return: CIN 계산 결과
        '''
        tmp_name_list = [tmp_1000, tmp_950, tmp_925, tmp_850, tmp_700, tmp_600]
        rh_name_list = [rh_1000, rh_950, rh_925, rh_850, rh_700, rh_600]
        p_list = [1000., 950., 925., 850., 700., 600.]

        CIN_result = []
        for i in range(0, 400):
            CIN = []
            for j in range(0, 400):
                T_list = []
                rh_list = []
                #한 좌표에서의 기압별 기온 리스트와 상대습도 리스트 생성
                for t, r in zip(tmp_name_list, rh_name_list):
                    T_list.append(t[i][j] - 273.15)
                    rh_list.append(r[i][j])
                cin = self.get_cin(p_list, T_list, rh_list)
                cin = float(str(cin).split("joule")[0])  #'joule/kilogram'유닛을 그냥 list에 넣으면 np.array로 변환할 수 없음. float로 변환
                CIN.append(cin)
            CIN_result.append(CIN)
        CIN_result = np.array(CIN_result)
        return CIN_result
