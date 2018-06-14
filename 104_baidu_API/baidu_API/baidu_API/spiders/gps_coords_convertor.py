#encoding: utf-8

import math
from math import sqrt,atan2,sin,cos

class GPSCoordsConvertor(object):
    def __init__(self):
        pass

    @staticmethod
    def __convertor(lng, lat, cE):
        T = cE[0] + cE[1] * abs(lng)
        cC = abs(lat) / cE[9]
        cF = cE[2] + cE[3] * cC + cE[4] * cC * cC + cE[5] * cC * cC * cC \
          + cE[6] * cC * cC * cC * cC + cE[7] * cC * cC * cC * cC * cC \
          + cE[8] * cC * cC * cC * cC * cC * cC
        T *= -1 if lng < 0 else 1
        cF *= -1 if lat < 0 else 1
        return (T, cF)

    @staticmethod
    def convert_mc_2_gps(lng, lat):
        MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]    
        MC2LL = [
            [
                1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331,
                200.9824383106796, -187.2403703815547, 91.6087516669843,
                -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2
            ],
            [ 
                -7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289,
                96.32687599759846, -1.85204757529826, -59.36935905485877, 47.40033549296737,
                -16.50741931063887, 2.28786674699375, 10260144.86
            ],
            [ 
                - 3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616,
                59.74293618442277, 7.357984074871, -25.38371002664745, 13.45380521110908,
                -3.29883767235584, 0.32710905363475, 6856817.37
            ],
            [ 
                - 1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591,
                40.31678527705744, 0.65659298677277, -4.44255534477492, 0.85341911805263,
                0.12923347998204, -0.04625736007561, 4482777.06
            ],
            [
                3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062,
                23.10934304144901, -0.00023663490511, -0.6321817810242, -0.00663494467273,
                0.03430082397953, -0.00466043876332, 2555164.4
            ],
            [
                2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032,
                -0.00000353937994, -0.02145144861037, -0.00001234426596,
                0.00010322952773, -0.00000323890364, 826088.5
            ]
        ]
        cF = []
        for i in xrange(len(MCBAND)):
            if lat >= MCBAND[i]:
                cF = MC2LL[i]
                break
        return GPSCoordsConvertor.__convertor(lng, lat, cF)

    @staticmethod
    def convert_gps_2_mc(lng, lat):  #gps 转geo
        x = lng *20037508.34/180
        y = math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
        y = y *20037508.34/180
        return (x, y)

    @staticmethod
    def baidu_coord_2_gps(lng, lat):
        bd_x = lng - 0.0065
        bd_y = lat - 0.006
        z = math.sqrt(bd_x * bd_x + bd_y * bd_y) - 0.00002 * math.sin(bd_y * math.pi)
        theta = math.atan2(bd_y, bd_x) - 0.000003 * math.cos(bd_x * math.pi)
        longitude = z * math.cos(theta)
        latitude = z * math.sin(theta)
        return (longitude, latitude)

    @staticmethod
    def gps_2_baidu_coord(lng, lat):
        x = lng
        y = lat
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * math.pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * math.pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return (bd_lng, bd_lat)

    @staticmethod
    def convert_tencent_to_baidu(lat, lng):
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = lng
        y = lat
        z = sqrt(x * x + y * y) + 0.00002 * sin(y * x_pi)
        theta = atan2(y, x) + 0.000003 * cos(x * x_pi)
        lng = z * cos(theta) + 0.0065
        lat = z * sin(theta) + 0.006
        return lng, lat

    @staticmethod
    def convert_baidu_to_tencent(lat, lng):
        x_pi = 3.14159265358979324 * 3000.0 / 180.0
        x = lng - 0.0065
        y = lat - 0.006
        z = sqrt(x * x + y * y) - 0.00002 * sin(y * x_pi)
        theta = atan2(y, x) - 0.000003 * cos(x * x_pi)
        lng = z * cos(theta)
        lat = z * sin(theta)
        return lng, lat

    