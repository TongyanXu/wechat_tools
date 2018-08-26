# coding=utf-8
"""Wechat Path Manager for all kinds of file & path supports"""
__author__ = 'Tongyan Xu'

import json
import os
import random
import time


class WechatPathManager(object):
    """
    Wechat path manager
    Can return file path needed in whole project
    Used for file & path management
    """
    _base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    _static = 'static'
    _cache = 'cache'
    _log = 'log'
    _temp = 'temp'

    _cache_file = 'wxpy.pkl'
    _puid_file = 'wxpy_puid.pkl'
    _log_file = '{}' + '_log_{}.log'.format(time.strftime('%Y%m%d_%H%M%S'))
    _cache_info_file = 'cache_info.json'

    _supported_sticker_type = ['.jpg', '.jpeg', '.png', '.gif']
    _sticker_list = []
    _cache_info = {}

    def __init__(self):
        self._static_dir = os.path.join(self._base_dir, self._static)
        self._cache_dir = os.path.join(self._base_dir, self._cache)
        self._log_dir = os.path.join(self._base_dir, self._log)
        self._temp_dir = os.path.join(self._cache_dir, self._temp)

        self._cache_file_path = os.path.join(self._cache_dir, self._cache_file)
        self._puid_file_path = os.path.join(self._cache_dir, self._puid_file)
        self._log_file_path = os.path.join(self._log_dir, self._log_file)
        self._cache_info_path = os.path.join(self._cache_dir, self._cache_info_file)

        self._check_and_create([self._static_dir, self._cache_dir, self._log_dir, self._temp_dir])
        self._load_default_sticker()
        self._load_cache_info()

    @property
    def cache_path(self):
        """Get cache path for Bot"""
        return self._cache_file_path

    @property
    def log_path(self):
        """Get log path for Bot"""
        return self._log_file_path

    @property
    def puid_path(self):
        """Get puid cache path for Bot"""
        return self._puid_file_path

    def get_sticker_path(self, sticker_name_=None):
        """Get sticker path for recall-blocker"""
        if not self._sticker_list:
            return None
        if not sticker_name_:
            _index = random.randint(0, len(self._sticker_list) - 1)
            sticker_name_ = self._sticker_list[_index]
        return os.path.join(self._static_dir, sticker_name_) if sticker_name_ else None

    def gen_msg_cache_path(self, msg_):
        """Generate message attachment cache path and register to cache info"""
        _original_name = msg_.file_name
        _time_stamp = int(time.time() * 1000000)
        _new_name = '{}{}'.format(_time_stamp, os.path.splitext(_original_name)[-1])
        _file_path = os.path.join(self._temp_dir, _new_name)
        self._cache_info[msg_.id] = _file_path
        self._save_cache_info()
        return _file_path

    def get_msg_cache_path(self, msg_id_):
        """Get message attachment cache path and register to cache info"""
        return self._cache_info.get(msg_id_)

    @staticmethod
    def _check_and_create(path_):
        for _p in path_:
            if not os.path.exists(_p):
                os.mkdir(_p)

    def _load_default_sticker(self):
        for _root, _dirs, _files in os.walk(self._static_dir):
            for _file in _files:
                if os.path.splitext(_file)[1].lower() in self._supported_sticker_type:
                    self._sticker_list.append(_file)

    def _load_cache_info(self):
        if os.path.exists(self._cache_info_path):
            with open(self._cache_info_path) as _f:
                self._cache_info = json.loads(_f.read())

    def _save_cache_info(self):
        with open(self._cache_info_path, 'w') as _f:
            _f.write(json.dumps(self._cache_info))
