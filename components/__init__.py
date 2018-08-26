# coding=utf-8
"""
This repository is for definitions of all types of wechat components
Each wechat util has its specific decorated function to deal with received messages
Three types of wechat components are available:
    Recall-blocker, to prevent user recalling messages,
    Auto-replier, to reply user's messages automatically through AI robots,
    Auto-repeater, to simply repeat user's messages
All wechat components can be generated or called through WechatComponents
* For different wechat components, it is strongly recommended to assign the same bot and path manager, but different
configs and loggers.
"""
__author__ = 'Tongyan Xu'

from constants import WechatChatType, WechatComponentType
from utils import WechatChatManager, WechatLogger, WechatPathManager
from wxpy import Bot


class WechatComponents(object):
    """
    Wechat base components
    Super class of all types of wechat components with definitions of fundamental methods
    Util types can be found in constants.py - WechatUtilType
    The following code shows a brief example of how to get a wechat util by util type:
        >>> from components import WechatComponents
        >>> from constants import WechatComponentType
        >>> wechat_util = WechatComponents.get_wechat_util(util_type_=WechatComponentType.YOUR_TYPE)
    Then, the instance, wechat_util, is ready to be used for specific purposes
    """
    _name = 'wechat_base_util'

    _default_config = {}
    _default_time_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, bot_=None, path_=None, config_=None, logger_=None):
        self._bot = bot_ if bot_ else Bot()
        self._path = path_ if path_ else WechatPathManager()
        self._config = config_ if config_ else self._default_config
        self._logger = logger_ if logger_ else self._gen_logger()
        self._load_config()

    @classmethod
    def get_wechat_util(cls, util_type_=None, bot_=None, path_=None, config_=None, logger_=None):
        """Get specific wechat util object by type"""
        if util_type_ == WechatComponentType.RECALL_BLOCKER:
            from .recall_blocker import WechatRecallBlocker
            return WechatRecallBlocker(bot_=bot_, path_=path_, config_=config_, logger_=logger_)
        elif util_type_ == WechatComponentType.AUTO_REPLIER:
            from .auto_replier import WechatAutoReplier
            return WechatAutoReplier(bot_=bot_, path_=path_, config_=config_, logger_=logger_)
        elif util_type_ == WechatComponentType.AUTO_REPEATER:
            from .auto_repeater import WechatAutoRepeater
            return WechatAutoRepeater(bot_=bot_, path_=path_, config_=config_, logger_=logger_)

    def run(self):
        """Run wechat util on friend and group chats"""
        self._register_auto_func(chat_type_=self._friend)
        self._register_auto_func(chat_type_=self._group)

    def _register_auto_func(self, chat_type_=None):
        """Definition of wxpy decorated function"""
        raise NotImplementedError

    def _gen_log_sender(self, msg_):
        _sender = '群聊 {} 中 {}'.format(msg_.sender.nick_name, msg_.member.nick_name) if \
            isinstance(msg_.sender, self._group.type) else '{}'.format(msg_.sender.nick_name) if \
            isinstance(msg_.sender, self._friend.type) else '未知'
        return _sender

    def _gen_logger(self):
        self._logging_config = self._config.pop('logging_config', {})
        _logger_creator = WechatLogger(name_=self._name, path_=self._path)
        return _logger_creator.get_logger(stream_=self._logging_config.get('stream', False),
                                          file_=self._logging_config.get('file', False))

    def _load_config(self):
        self._friend = WechatChatManager(chat_type_=WechatChatType.FRIEND,
                                         enabled_=self._config.get('friend_enable', False),
                                         original_filter_=self._config.get('friend_filter', []),
                                         bot_=self._bot,
                                         logger_=self._logger)
        self._group = WechatChatManager(chat_type_=WechatChatType.GROUP,
                                        enabled_=self._config.get('group_enable', False),
                                        original_filter_=self._config.get('group_filter', []),
                                        bot_=self._bot,
                                        logger_=self._logger)
