# coding=utf-8
"""
Wechat Tools
This script is to setup all available wechat components
By modifying configs, wechat components may perform differently
To see detailed info of each component, please check components repository
"""
__author__ = 'Tongyan Xu'
__version__ = '1.0.6'

from wxpy import Bot, embed
from constants import WechatComponentType, WechatDefaultConfig
from utils.path import WechatPathManager
from components import WechatComponents


def run_wechat_utils(recall_blocker_config=WechatDefaultConfig.RECALL_BLOCKER_CONFIG,
                     auto_replier_config=WechatDefaultConfig.AUTO_REPLIER_CONFIG,
                     auto_repeater_config=WechatDefaultConfig.AUTO_REPEATER_CONFIG):
    """Run wechat components using configs"""
    path = WechatPathManager()
    bot = Bot(cache_path=path.cache_path)
    bot.enable_puid(path=path.puid_path)

    # if auto_replier_config['enable'] and auto_repeater_config['enable']:
    #     if auto_replier_config['friend_enable'] and auto_repeater_config['friend_enable']:
    #         auto_repeater_config['friend_enable'] = False
    #     if auto_replier_config['group_enable'] and auto_repeater_config['group_enable']:
    #         auto_repeater_config['group_enable'] = False

    if recall_blocker_config['enable']:
        recall_blocker = WechatComponents.get_wechat_util(util_type_=WechatComponentType.RECALL_BLOCKER,
                                                          bot_=bot, path_=path, config_=recall_blocker_config)
        recall_blocker.run()
    if auto_repeater_config['enable']:
        auto_repeater = WechatComponents.get_wechat_util(util_type_=WechatComponentType.AUTO_REPEATER,
                                                         bot_=bot, path_=path, config_=auto_repeater_config)
        auto_repeater.run()
    if auto_replier_config['enable']:
        auto_replier = WechatComponents.get_wechat_util(util_type_=WechatComponentType.AUTO_REPLIER,
                                                        bot_=bot, path_=path, config_=auto_replier_config)
        auto_replier.run()

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
    """
    run_wechat_utils(
        recall_blocker_config=dict(
            enable=True,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here'],
            sticker=dict(
                send_sticker=True,
                sticker_name=None)),
        auto_replier_config=dict(
            enable=False,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here'],
            auto_replier=dict(
                tuling=True,
                xiaoi=False)),
        auto_repeater_config=dict(
            enable=False,
            friend_enable=True,
            group_enable=False,
            friend_filter=['whatever friends here'],
            group_filter=['whatever groups here']))
