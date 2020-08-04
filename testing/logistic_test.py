"""
This file does unittest for functions in web.logistic

"""
from web.logistic import *
import pytest



def test_region_str_filter():
    """Test the normalization of regions"""
    assert region_str_filter("内蒙古自治区") == "内蒙古"


def test_extract_cities():
    """Test the extract cities for a province"""
    # m = extract_cities("胖胖子")
    # assert len(m) > 0
    m = extract_cities("内蒙古")
    assert len(m) > 0


def test_city_name_transfer():
    """ Test city name normalization
        if
    """
    assert city_name_transfer("安徽省", "安庆府") == "安庆府", "No Transfer Done"
    assert city_name_transfer("安徽省", "安庆") == "安庆市"
    assert city_name_transfer("内蒙古", "呼和浩特") == "呼和浩特市"


def test_get_china_lock_map():
    """Test the returned time index and start index for Timeline"""
    "small time_index test, return 0, abs_time_index - 0"
    map_data = get_china_lock_map(5)
    assert len(map_data[0]) == 21
    assert map_data[1] == 0
    assert map_data[2] == 5

    "Large time_index test, start_index = abs_time_index-15, time_index= abs_time_index- start_index"
    map_data = get_china_lock_map(40)
    assert len(map_data[0]) == 31
    assert map_data[1] == 25
    assert map_data[2] == 15


def test_get_province_lock_map():
    """Get lock condition data for a certain province at a specified time point"""
    m = get_province_lock_map("湖北", 4)
    assert len(m) > 0


def test_get_china_lock_news():
    """Get news at specified time point, return dict"""
    m = get_china_lock_news(20)
    assert 'news' in m and 'date' in m
    assert len(m['news']) > 0 and m['date']




