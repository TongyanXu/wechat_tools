# coding=utf-8
"""Status monitor on wechat, to report progress / status of project on wechat"""

from datetime import datetime
from logging import INFO
from wxpy import get_wechat_logger


wechat_logger = get_wechat_logger(name='status_monitor', level=INFO)
time_format = '%Y-%m-%d %H:%M:%S'


def status_monitor_on_wechat(func_):
    """Decorator to send wechat messages to file helper when the decorated function is called and finished"""
    def inner_func(*args, **kwargs):
        """Decorated function with general input"""
        _name = str(func_).split(' ')[1]
        _begin = datetime.now()
        wechat_logger.info('Start running function <{}> at {}'.format(_name, datetime.strftime(_begin, time_format)))

        try:
            _res = func_(*args, **kwargs)
            _end = datetime.now()
            _last = _end - _begin
            wechat_logger.info('Finish running function <{}> at {}, lasting {} seconds\nResult: {}'.format(
                _name, datetime.strftime(_end, time_format), _last.total_seconds(), str(_res)))
            return _res

        except Exception as e:
            _msg = str(e)
            _end = datetime.now()
            _last = _end - _begin
            wechat_logger.error('Failed to run <{}> at {}, lasting {} seconds\nError msg: {}'.format(
                _name, datetime.strftime(_end, time_format), _last.total_seconds(), _msg))
            raise Exception(_msg)

    return inner_func
