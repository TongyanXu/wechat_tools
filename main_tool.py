# coding=utf-8
"""
Wechat Toolkit
This script is to setup all available wechat components
By modifying configs, wechat components may perform differently
To see detailed info of each component, please check components repository
"""
__author__ = 'Tongyan Xu'
__version__ = '1.2.6'

from components import WechatComponents
from constants import WechatComponentType, WechatDefaultConfig
from time import sleep
from utils import WechatLogger, WechatPathManager
from wxpy import Bot, embed

tools = [{'type': WechatComponentType.RECALL_BLOCKER,
          'config_key': 'recall_blocker_config',
          'config': WechatDefaultConfig.RECALL_BLOCKER_CONFIG},
         {'type': WechatComponentType.AUTO_REPEATER,
          'config_key': 'auto_repeater_config',
          'config': WechatDefaultConfig.AUTO_REPEATER_CONFIG},
         {'type': WechatComponentType.AUTO_REPLIER,
          'config_key': 'auto_replier_config',
          'config': WechatDefaultConfig.AUTO_REPLIER_CONFIG}]


class WechatToolkit(object):
    """..."""
    _name = 'wechat_toolkit'

    def __init__(self, config_=None, tools_=tools, sub_thread_=False):
        self._path = WechatPathManager()
        self._tools = tools_
        self._config = config_ if config_ else {}
        self._logging_config = self._config.pop('logging_config', WechatDefaultConfig.LOGGING_CONFIG)
        self._gen_logger()
        self._sub_thread = sub_thread_
        self._terminated = False
        self._enabled_tools = []
        self._working_components = []

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

    def stop(self):
        """..."""
        self._terminated = True

    def run(self):
        """Run wechat components using configs"""
        self._enabled_tools = []
        self._working_components = []
        self._setup_tools()
        self._setup_bot()

        for _t in self._enabled_tools:
            _comp = WechatComponents.get_wechat_util(
                util_type_=_t['type'], bot_=self._bot, path_=self._path, config_=_t['config'])
            self._working_components.append(_comp)
            _comp.run()
            self._logger.info('wechat component <{}> is activated.'.format(_t['type']))

        self._logger.info('all components activated successfully.')

        if self._sub_thread:
            while not self._terminated:
                sleep(1)
        else:
            embed()

        self._logger.info('all components are stopped.')
