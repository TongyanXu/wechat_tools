# coding=utf-8
"""Wechat Auto-Repeater, to simply repeat user's messages"""
__author__ = 'Tongyan Xu'

from . import WechatComponents
from constants import WechatMsgType, WechatDefaultConfig


class WechatAutoRepeater(WechatComponents):
    """
    Wechat auto-repeater
    Can work on both friend and group chats
    """
    _name = 'wechat_auto_repeater'

    def __init__(self, bot_=None, path_=None, config_=WechatDefaultConfig.AUTO_REPEATER_CONFIG, logger_=None):
        super(WechatAutoRepeater, self).__init__(bot_=bot_, path_=path_, config_=config_, logger_=logger_)

    def _register_auto_func(self, chat_type_=None):
        @self._bot.register(chats=chat_type_.type, enabled=chat_type_.is_enabled, msg_types=WechatMsgType.REPEAT_MSG)
        def auto_repeat_friend(msg):
            """
            Auto repeat message
            Controlled by config
            """
            if chat_type_.is_all or msg.sender.nick_name in chat_type_.filter:
                if msg.type in [WechatMsgType.PICTURE] and msg.raw.get('HasProductId'):
                    msg.reply_msg(r'这表情我没下')
                    self._logger.warning(r'无法复读 {} 的信息，系微信官方表情'.format(self._gen_log_sender(msg)))
                msg.forward(msg.sender)
                self._logger.info(r'已自动复读 {} 的信息'.format(self._gen_log_sender(msg)))
