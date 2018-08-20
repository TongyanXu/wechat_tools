# coding=utf-8
"""
Wechat Tools
This script is to setup all available wechat components
By modifying configs, wechat components may perform differently
To see detailed info of each component, please check components repository
"""
__author__ = 'Tongyan Xu'
__version__ = '1.2.0'

from wxpy import Bot, embed
from constants import WechatComponentType, WechatDefaultConfig
from utils import WechatPathManager, WechatLogger
from components import WechatComponents


class WechatTools(object):
    """..."""
    _name = 'wechat_tools_main'
    _tools = [{'type': WechatComponentType.RECALL_BLOCKER,
               'config_key': 'recall_blocker_config',
               'config': WechatDefaultConfig.RECALL_BLOCKER_CONFIG},
              {'type': WechatComponentType.AUTO_REPEATER,
               'config_key': 'auto_repeater_config',
               'config': WechatDefaultConfig.AUTO_REPEATER_CONFIG},
              {'type': WechatComponentType.AUTO_REPLIER,
               'config_key': 'auto_replier_config',
               'config': WechatDefaultConfig.AUTO_REPLIER_CONFIG}]
    _enabled_tools = []
    _working_components = []

    def __init__(self, config_=None):
        self._path = WechatPathManager()
        self._config = config_ if config_ else {}
        self._logging_config = self._config.pop('logging_config', WechatDefaultConfig.LOGGING_CONFIG)
        self._gen_logger()
        self._setup_tools()
        self._setup_bot()

    def _gen_logger(self):
        _logger_creator = WechatLogger(name_=self._name, path_=self._path)
        self._logger = _logger_creator.get_logger(stream_=self._logging_config.get('stream', False),
                                                  file_=self._logging_config.get('file', False))

    def _setup_tools(self):
        for _tool in self._tools:
            _tool['config'] = self._config.pop(_tool['config_key'], _tool['config'])
            _tool['config']['logging_config'] = self._logging_config
            if _tool['config'].get('enable'):
                self._enabled_tools.append(_tool)
                self._logger.info('wechat component <{}> to be activated.'.format(_tool['type']))

    def _setup_bot(self):
        self._bot = Bot(cache_path=self._path.cache_path)
        self._bot.enable_puid(path=self._path.puid_path)

    def run(self):
        """Run wechat components using configs"""
        for _t in self._enabled_tools:
            _comp = WechatComponents.get_wechat_util(
                util_type_=_t['type'], bot_=self._bot, path_=self._path, config_=_t['config'])
            self._working_components.append(_comp)
            _comp.run()
            self._logger.info('wechat component <{}> is activated.'.format(_t['type']))

        self._logger.info('all components activated successfully.')
        embed()


if __name__ == '__main__':
    """
    Modify the config value below
    If any filter is used, please type as specific as you can to avoid mismatching
    
    WORK_ON: Recall-blocker: all types of messages
             Auto-replier: TEXT messages only
             Auto-repeater: all types of messages except VIDEO and ATTACHMENT
             (can check constants.__init__.py)
    
    WARNING: When any main function is enabled and the related filter is empty, NO FRIEND OR GROUP WILL BE FILTERED
             Thus, filters are very important when any function is enabled
             Remember to set filter on all group filters to avoid messy situations
    
    WARNING: Auto-replier and auto-repeater cannot be enabled simultaneously
             Or auto-repeater will be disabled on all TEXT messages
    
    WARNING: Tuling is preferred in auto-replier
             If both Tuling and XiaoI are enabled, XiaoI will be automatically ignored
    """
    config = dict(
        recall_blocker_config=dict(
            enable=True,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here'],
            backup_enable=True,
            sticker=dict(
                send_sticker=True,
                sticker_name=None)),
        auto_replier_config=dict(
            enable=True,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here'],
            auto_replier=dict(
                tuling=True,
                xiaoi=False)),
        auto_repeater_config=dict(
            enable=True,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here']),
        logging_config=dict(
            stream=True,
            file=True))

    main_tool = WechatTools(config_=config)
    main_tool.run()
