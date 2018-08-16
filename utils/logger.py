# coding=utf-8
"""Wechat Logger for logging management"""

from logging import getLogger, StreamHandler, FileHandler, Formatter, INFO
from . import WechatPathManager


class WechatLogger(object):
    """
    Wechat logger
    Can show log in both terminal and log file
    Log file path is defined in wechat path manager
    """
    _default_logger_level = INFO
    _default_logger_format = '<%(name)s> [%(levelname)s] %(message)s'
    _default_formatter = Formatter(_default_logger_format)

    def __init__(self, name_, path_=None, level_=None):
        self._name = name_
        self._path = path_ if path_ else WechatPathManager()
        self._level = level_ if level_ else self._default_logger_level

    def get_logger(self, stream_=True, file_=True):
        """Return a default wechat logger"""
        _default_logger = getLogger(self._name)
        _default_logger.setLevel(self._level)
        if stream_:
            _default_logger.addHandler(self._gen_stream_handler())
        if file_:
            _default_logger.addHandler(self._gen_file_handler())
        return _default_logger

    def _gen_stream_handler(self):
        _stream_handler = StreamHandler()
        _stream_handler.setLevel(self._level)
        _stream_handler.setFormatter(self._default_formatter)
        return _stream_handler

    def _gen_file_handler(self):
        _stream_handler = FileHandler(self._path.log_path)
        _stream_handler.setLevel(self._level)
        _stream_handler.setFormatter(self._default_formatter)
        return _stream_handler
