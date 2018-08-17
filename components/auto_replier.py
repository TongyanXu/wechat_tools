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
    _name = 'wechat_autp_replier'

    _tuling_api_key = '60d93972232d42f3b7428ae3631b7289'
    _xiaoi_key = 'aIxBk61kStUm'
    _xiaoi_secret = 'rRqWy14gVh7jMG6hGRCP'

    def __init__(self, bot_=None, path_=None, config_=WechatDefaultConfig.AUTO_REPLIER_CONFIG, logger_=None):
        super(WechatAutoReplier, self).__init__(bot_=bot_, path_=path_, config_=config_, logger_=logger_)
        self._tuling = Tuling(api_key=self._tuling_api_key)
        self._xiaoi = XiaoI(key=self._xiaoi_key, secret=self._xiaoi_secret)

    def _register_auto_func(self, chat_type_=None):
        @self._bot.register(chats=chat_type_.type, enabled=chat_type_.is_enabled, msg_types=WechatMsgType.REPLY_MSG)
        def auto_reply(msg):
            """
            Auto reply
            Using Tuling or XiaoI robot to auto reply received message intelligently
            If non-text message received, just repeat it, working as an auto-repeater
            Controlled by config
            """
            if chat_type_.is_all or msg.sender.nick_name in chat_type_.filter:
                if msg.type in WechatMsgType.TEXT:
                    self._auto_reply(msg_=msg,
                                     tuling_=self._config['auto_replier']['tuling'],
                                     xiaoi_=self._config['auto_replier']['xiaoi'])
                else:
                    msg.forward(msg.sender)

    def _auto_reply(self, msg_, tuling_=False, xiaoi_=False):
        msg_reply = None
        if tuling_ and not xiaoi_:
            msg_reply = self._tuling.do_reply(msg_)
        elif not tuling_ and xiaoi_:
            msg_reply = self._xiaoi.do_reply(msg_)
        elif tuling_ and xiaoi_:
            robot = self._random_robot()
            if robot == WechatRobotType.TULING:
                msg_reply = self._tuling.do_reply(msg_)
            elif robot == WechatRobotType.XIAOI:
                msg_reply = self._xiaoi.do_reply(msg_)
        self._log(msg_=msg_, msg_reply_=msg_reply)

    def _log(self, msg_, msg_reply_):
        if isinstance(msg_.sender, self._friend.type):
            self._logger.info(
                r'收到群聊 {} 中 {} 的信息：{}'.format(msg_.sender.nick_name, msg_.member.nick_name, msg_.text))
        elif isinstance(msg_.sender, self._group.type):
            self._logger.info(r'收到 {} 的信息：{}'.format(msg_.sender.nick_name, msg_.text))
        self._logger.info(r'自动回复内容：'.format(msg_reply_))

    @staticmethod
    def _random_robot():
        index = random.randint(0, 1)
        return WechatRobotType.TULING if index else WechatRobotType.XIAOI
