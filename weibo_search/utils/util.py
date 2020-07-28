from datetime import datetime, timedelta
from web.region_info.region import region_dict


def get_all_province():
    return list(region_dict.keys())


def convert_weibo_type(weibo_type):
    """Change weibo type into url string"""
    if weibo_type == 0:
        return '&typeall=1'
    elif weibo_type == 1:
        return '&scope=ori'
    elif weibo_type == 2:
        return '&xsort=hot'
    elif weibo_type == 3:
        return '&atten=1'
    elif weibo_type == 4:
        return '&vip=1'
    elif weibo_type == 5:
        return '&category=4'
    elif weibo_type == 6:
        return '&viewpoint=1'
    return '&scope=ori'


def convert_contain_type(contain_type):
    """Change weibo contained type into url string"""
    if contain_type == 0:
        return '&suball=1'
    elif contain_type == 1:
        return '&haspic=1'
    elif contain_type == 2:
        return '&hasvideo=1'
    elif contain_type == 3:
        return '&hasmusic=1'
    elif contain_type == 4:
        return '&haslink=1'
    return '&suball=1'


def standardize_date(created_at):
    """Normalize weibo publication time"""
    if "刚刚" in created_at:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    elif "秒" in created_at:
        second = created_at[:created_at.find(u"秒")]
        second = timedelta(seconds=int(second))
        created_at = (datetime.now() - second).strftime("%Y-%m-%d %H:%M")
    elif "分钟" in created_at:
        minute = created_at[:created_at.find(u"分钟")]
        minute = timedelta(minutes=int(minute))
        created_at = (datetime.now() - minute).strftime("%Y-%m-%d %H:%M")
    elif "小时" in created_at:
        hour = created_at[:created_at.find(u"小时")]
        hour = timedelta(hours=int(hour))
        created_at = (datetime.now() - hour).strftime("%Y-%m-%d %H:%M")
    elif "今天" in created_at:
        today = datetime.now().strftime('%Y-%m-%d')
        created_at = today+' '+created_at[2:]
    elif '年' not in created_at:
        year = datetime.now().strftime("%Y")
        month = created_at[:2]
        day = created_at[3:5]
        time = created_at[6:]
        created_at = year + '-' + month + '-' + day + ' ' + time
    else:
        year = created_at[:4]
        month = created_at[5:7]
        day = created_at[8:10]
        time = created_at[11:]
        created_at = year + '-' + month + '-' + day + ' ' + time
    return created_at
