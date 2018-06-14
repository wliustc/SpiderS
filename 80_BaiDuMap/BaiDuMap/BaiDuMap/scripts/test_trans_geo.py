# encoding: utf-8
from gps_coords_convertor import GPSCoordsConvertor

def trans_geo(x,y):
    return GPSCoordsConvertor.convert_mc_2_gps(x, y)
    # return GPSCoordsConvertor.convert_gps_2_mc(x,y)
    # return GPSCoordsConvertor.baidu_coord_2_gps(x,y)

# print trans_geo(11622073.81, 3578638.97)