# coding=utf-8
"""Frequently used constants"""
__author__ = 'Tongyan Xu'

from wxpy import ATTACHMENT, CARD, MAP, NOTE, PICTURE, RECORDING, SHARING, SYSTEM, TEXT, VIDEO


class WechatMsgType(object):
    """Wechat supported message types"""
    TEXT = TEXT
    RECORDING = RECORDING
    PICTURE = PICTURE
    VIDEO = VIDEO
    SHARING = SHARING
    CARD = CARD
    MAP = MAP
    ATTACHMENT = ATTACHMENT
    NOTE = NOTE
    SYSTEM = SYSTEM
    NORMAL_MSG = [TEXT, RECORDING, PICTURE, VIDEO, SHARING, CARD, MAP, ATTACHMENT]
    LARGE_MSG = [VIDEO, ATTACHMENT]
    SPECIAL_MSG = [PICTURE, VIDEO, CARD, ATTACHMENT]
    REPEAT_MSG = [TEXT, RECORDING, PICTURE, SHARING, CARD, MAP]
    REPLY_MSG = [TEXT]


class WechatChatType(object):
    """Wechat supported chat types"""
    FRIEND = 'FRIEND'
    GROUP = 'GROUP'
    EMPTY = ''


class WechatComponentType(object):
    """Wechat component types"""
    RECALL_BLOCKER = 'RECALL-BLOCKER'
    AUTO_REPLIER = 'AUTO-REPLIER'
    AUTO_REPEATER = 'AUTO-REPEATER'
    YOUR_TYPE = ''


class WechatRobotType(object):
    """Wechat auto-reply robot types"""
    TULING = 'TULING'
    XIAOI = 'XIAOI'


class WechatDefaultConfig(object):
    """Wechat default configs"""
    RECALL_BLOCKER_CONFIG = dict(
        enable=False,
        friend_enable=False,
        group_enable=False,
        friend_filter=[],
        group_filter=[],
        backup_enable=False,
        sticker=dict(
            send_sticker=True,
            sticker_name=None))

    AUTO_REPLIER_CONFIG = dict(
        enable=False,
        friend_enable=False,
        group_enable=False,
        friend_filter=[],
        group_filter=[],
        auto_replier=dict(
            tuling=False,
            xiaoi=False))

    AUTO_REPEATER_CONFIG = dict(
        enable=False,
        friend_enable=False,
        group_enable=False,
        friend_filter=[],
        group_filter=[])

    LOGGING_CONFIG = dict(
        stream=False,
        file=False,
        wechat=False)
