""" 日期时间相关util函数
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional, List, Union


def now_time(tz:str='Asia/Shanghai') -> datetime:
    """ 当前时间实例 """
    return datetime.now(ZoneInfo(tz))

def now(fmt:str='%Y-%m-%d %H:%M:%S', tz:str='Asia/Shanghai') -> str:
    """ 当前时间字符串 """
    return now_time(tz).strftime(fmt)

def get_date(ndays:int=-1, base_date:Optional[str]=None, base_date_FMT:Optional[str]=None, FMT:str='%Y-%m-%d', tz:str='Asia/Shanghai') -> str:
    """ 获取几天前/后的日期字符串 """
    base_datetime = now_time(tz) if base_date is None else datetime.strptime(base_date, base_date_FMT or FMT)
    return datetime.strftime(base_datetime + timedelta(ndays), FMT)

def date_range(start:str, end:str, end_include:bool=False, step:int=1, FMT:str='%Y-%m-%d') -> List[str]:
    """ 基于开始和结束，生成日期字符串列表 """
    if start > end and step > 0: raise ValueError(f'当日期start > end时, step必须小于0')
    elif start < end and step < 0: raise ValueError(f'当日期start < end时, step必须大于0')
    days = (datetime.strptime(end, FMT) - datetime.strptime(start, FMT)).days
    days = days + int(step/abs(step)) if end_include else days
    return [datetime.strftime(datetime.strptime(start, FMT) + timedelta(i), FMT) for i in range(0, days, step)]

def stamp2str(timestamp: Union[int, float, str], unit:str='s', fmt:str='%Y-%m-%d %H:%M:%S', tz:str='Asia/Shanghai') -> str:
    """ 时间戳 转 时间字符串 """
    assert unit in ('s', 'ms', 'us', 'ns')
    timestamp_seconds = float(timestamp) * {'s':1.0, 'ms':1e-3, 'us':1e-6, 'ns':1e-9}[unit]
    dt = datetime.fromtimestamp(timestamp_seconds, tz=ZoneInfo(tz))
    return dt.strftime(fmt)

def stamp2time(timestamp: Union[int, float, str], unit:str='s', tz:str='Asia/Shanghai') -> datetime:
    """ 时间戳 转 时间实例 """
    assert unit.lower() in ('s', 'ms', 'us', 'ns')
    timestamp_seconds = float(timestamp) * {'s':1.0, 'ms':1e-3, 'us':1e-6, 'ns':1e-9}[unit.lower()]
    dt = datetime.fromtimestamp(timestamp_seconds, tz=ZoneInfo(tz))
    return dt
