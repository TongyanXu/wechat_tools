# coding=utf-8
"""Wechat Auto-Replier, to reply user's messages automatically through AI robots"""
__author__ = 'Tongyan Xu'

from wxpy import Tuling, XiaoI
import random
from . import WechatComponents
from constants import WechatMsgType, WechatRobotType, WechatDefaultConfig


class WechatAutoReplier(WechatComponents):
    """
    Wechat auto-replier
    Can work on both friend and group chats
    """
    _name = 'wechat_auto_replier'

    _tuling_api_key = '60d93972232d42f3b7428ae3631b7289'
    _xiaoi_key = 'aIxBk61kStUm'
    _xiaoi_secret = 'rRqWy14gVh7jMG6hGRCP'

    def __init__(self, bot_=None, path_=None, config_=WechatDefaultConfig.AUTO_REPLIER_CONFIG, logger_=None):
        super(WechatAutoReplier, self).__init__(bot_=bot_, path_=path_, config_=config_, logger_=logger_)
        self._tuling = Tuling(api_key=self._tuling_api_key)
        self._xiaoi = XiaoI(key=self._xiaoi_key, secret=self._xiaoi_secret)
        self._set_replier(tuling_=self._config['auto_replier']['tuling'], xiaoi_=self._config['auto_replier']['xiaoi'])

    def _register_auto_func(self, chat_type_=None):
        @self._bot.register(chats=chat_type_.type, enabled=chat_type_.is_enabled, msg_types=WechatMsgType.REPLY_MSG)
        def auto_reply(msg):
            """
            Auto reply
            Using Tuling or XiaoI robot to auto reply received message intelligently
            Cannot deal with non-text message
            Controlled by config
            """
            if chat_type_.is_all or msg.sender.nick_name in chat_type_.filter:
                _msg_reply = self._replier.do_reply(msg)
                self._log(msg_=msg, msg_reply_=_msg_reply)

    def _set_replier(self, tuling_=False, xiaoi_=False):
        self._replier = self._xiaoi if xiaoi_ and not tuling_ else self._tuling

    def _log(self, msg_, msg_reply_):
        self._logger.info(r'收到 {} 的信息：{}'.format(self._gen_log_sender(msg_), msg_.text))
        self._logger.info(r'自动回复内容：{}'.format(msg_reply_))
