# coding=utf-8
"""
Run wechat toolkit with configs in config.py
"""
__author__ = 'Tongyan Xu'

from config import config
from main_tool import WechatToolkit


def main():
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
    toolkit = WechatToolkit(config_=config)
    toolkit.run()


if __name__ == '__main__':
    main()
