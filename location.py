#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from shapely.geometry import shape, Point

_geojson_data = {}


def coordinate2address(latitude, longitude):
    '''
        经纬度坐标地址解析
        :param latitude: 经度
        :param longitude: 纬度
        :return: 行政区规划地址
    '''

    point = Point(latitude, longitude)
    address = []

    _dfs('china', point, address)

    return address


def _dfs(map_key, point, result=[]):
    level = 'province'
    if len(map_key) == 2:
        level = 'city'
    elif len(map_key) == 4:
        level = 'county'

    map_data = _geojson_data.get(map_key)

    if not map_data:
        if map_key == 'china':  # find in country
            map_file_str = 'mapdata/china.json'
        elif len(map_key) == 2:  # find in province
            map_file_str = 'mapdata/geometryProvince/%s.json' % map_key
        elif len(map_key) == 4:  # find in city
            map_file_str = 'mapdata/geometryCouties/%s00.json' % map_key
        else:
            return

        print(map_file_str)  # debug log

        try:
            with open(map_file_str, encoding='UTF-8-SIG') as f:
                map_data = json.load(f)
        except Exception as e:
            print(e)  # debug log
            return

    for feature in map_data['features']:
        polygon = shape(feature['geometry'])

        if polygon.contains(point):
            name = feature['properties']['name']
            result.append((level, name))

            sub_map_key = feature['properties']['id']
            _dfs(sub_map_key, point, result)

            return


if __name__ == '__main__':
    # 梅县松口车站
    longitude, latitude = 24.5045787219, 116.4040174622
    address = coordinate2address(latitude, longitude)
    print(address)
