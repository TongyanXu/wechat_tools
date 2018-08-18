# coding=utf-8
"""Wechat Chat Manager for chat type management and filter generation"""

from constants import WechatChatType
from wxpy import Bot, Friend, Group
from logging import getLogger


class WechatChatManager(object):
    """
    Wechat chat manager
    Can generate real filter using given vague keywords
    Save partial config
    """

    def __init__(self, chat_type_=WechatChatType.EMPTY, enabled_=False, original_filter_=None, bot_=None, logger_=None):
        self._bot = bot_ if bot_ else Bot()
        self._logger = logger_ if logger_ else getLogger()
        self._name = chat_type_
        self._set_type()
        self._enabled = enabled_
        self._enabled_real = enabled_
        self._original_filter = original_filter_
        self._apply_filter()

    @property
    def is_enabled(self):
        """Return current chat is enabled or not"""
        return self._enabled_real

    @property
    def filter(self):
        """Return filter for current chat"""
        return self._filter

    @property
    def type(self):
        """Return current chat type"""
        return self._type

    @property
    def is_all(self):
        """Return if all chatting objects are enabled"""
        return self._all

    def _set_type(self):
        _mapping_dict = {
            WechatChatType.FRIEND: Friend,
            WechatChatType.GROUP: Group
        }
        self._type = _mapping_dict.get(self._name)

    def _apply_filter(self):
        self._process_filter()
        self._enabled_real = False if not self._filter and self._fail_filter else self._enabled
        self._all = True if not self._filter and self._enabled_real else False
        if self._enabled_real and not self._all:
            self._logger.info('{:6} chats are registered with filter: {}'.format(self._name, self._filter))
        elif self._enabled_real and self._all:
            self._logger.warning('{:6} chats are registered without filter.'.format(self._name))
        else:
            self._logger.info('{:6} chats are disabled.'.format(self._name))
        if self._enabled and self._fail_filter:
            self._logger.error('FAILED to recognize following users in filter: {}'.format(self._fail_filter))

    def _process_filter(self):
        self._filter_temp = list(map(self._search_nick_name, self._original_filter))
        self._check_fail()

    def _check_fail(self):
        self._filter = []
        self._fail_filter = []
        for _element in self._filter_temp:
            if _element:
                self._filter.append(_element)
            else:
                _index = self._filter_temp.index(_element)
                self._fail_filter.append(self._original_filter[_index])

    def _search_nick_name(self, key_word_=None):
        _user = self._bot.search(keywords=key_word_)
        return _user[0].nick_name if _user else None
