# encoding: utf-8
from gps_coords_convertor import GPSCoordsConvertor

def trans_geo(x,y):
    # return GPSCoordsConvertor.baidu_coord_2_gps(x,y)
    # return GPSCoordsConvertor.gps_2_baidu_coord(x,y)
    # return GPSCoordsConvertor.convert_mc_2_gps(x,y)
    return GPSCoordsConvertor.convert_gps_2_mc(x,y)

# print trans_geo(12959676.7462,4853967.22241)


