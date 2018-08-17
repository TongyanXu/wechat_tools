# coding=utf-8
"""Wechat Recall-Blocker, to prevent user recalling messages"""
__author__ = 'Tongyan Xu'

import re
import os
from . import WechatComponents
from constants import WechatMsgType, WechatDefaultConfig


class WechatRecallBlocker(WechatComponents):
    """
    Wechat recall-blocker
    Can work on both friend and group chats
    """
    _name = 'wechat_recall_blocker'

    def __init__(self, bot_=None, path_=None, config_=WechatDefaultConfig.RECALL_BLOCKER_CONFIG, logger_=None):
        super(WechatRecallBlocker, self).__init__(bot_=bot_, path_=path_, config_=config_, logger_=logger_)

    def _register_auto_func(self, chat_type_=None):
        @self._bot.register(chats=chat_type_.type, enabled=True, msg_types=WechatMsgType.ATTACH_MSG)
        def msg_backup(msg):
            """
            Message attachment cache maker
            To cache all recordings, pictures, videos, and attachments in all other types
            Since auto cache is not reliable enough under recalling situations
            All cache files will be save at cache/temp
            Videos and attachments are not considered to send whole files while replying
            """
            msg.get_file(save_path=self._path.gen_msg_cache_path(msg))

        @self._bot.register(chats=chat_type_.type, enabled=True, msg_types=WechatMsgType.NOTE)
        def recall_backup(note):
            """
            Recall blocker - backup & reply message
            Backup is to send the info of recalled message to file helper
            Reply is to forward the recalled message to the sender with a sticker
            Backup is always enabled
            Reply is controlled by config
            """
            msg, recall_time = self._get_recall_msg(note_=note)
            if msg:
                self._backup_msg(msg, recall_time)
                if chat_type_.is_enabled:
                    if chat_type_.is_all or msg.sender.nick_name in chat_type_.filter:
                        if self._config['sticker']['send_sticker']:
                            self._reply_sticker(msg_=msg,
                                                sticker_name_=self._config['sticker']['sticker_name'],
                                                random_sticker_=self._config['sticker']['random_sticker'])
                        self._send_msg(msg_=msg)

    def _get_msg_by_id(self, msg_id_=None):
        if msg_id_:
            msg_list = self._bot.messages.search(id=msg_id_)
            if msg_list:
                msg = msg_list[0]
                return msg
        return None

    def _get_recall_msg(self, note_=None):
        if note_ and re.search(r'<!\[CDATA\[.*撤回了一条消息\]\]>', note_.raw.get('Content')) \
                and re.search(r'<!\[CDATA\[(.*?)撤回了一条消息\]\]>', note_.raw.get('Content')).group(1) != '你':
            msg_id = int(re.search('<msgid>(.*?)</msgid>', note_.raw.get('Content')).group(1))
            msg = self._get_msg_by_id(msg_id_=msg_id)
            return msg, note_.create_time
        return None, None

    def _backup_msg(self, msg_, recall_time_):
        if isinstance(msg_.sender, self._friend.type):
            prefix = r'{} 于 {} 撤回了 {} 消息: '.format(
                msg_.sender.nick_name, recall_time_.strftime(self._default_time_format), msg_.type)
        elif isinstance(msg_.sender, self._group.type):
            prefix = r'{} 于 {} 在群聊 {} 撤回了 {} 消息: '.format(
                msg_.member.nick_name, recall_time_.strftime(self._default_time_format), msg_.sender.nick_name,
                msg_.type)
        else:
            prefix = str(msg_)
        self._send_msg(msg_=msg_, prefix_=prefix, send_to_=self._bot.file_helper)
        self._logger.info(prefix[:-2])

    def _reply_sticker(self, msg_, sticker_name_=None, random_sticker_=True):
        sticker_path = self._path.get_sticker_path(sticker_name_=sticker_name_, random_sticker_=random_sticker_)
        msg_.reply_image(path=sticker_path)

    def _send_msg(self, msg_, prefix_=None, send_to_=None):
        if not send_to_:
            send_to_ = msg_.sender

        if msg_.type in [WechatMsgType.CARD] + WechatMsgType.ATTACH_MSG:
            send_to_.send_msg(msg=self._get_name_prefix(msg_=msg_) + self._get_prefix(
                msg_=msg_) if not prefix_ else prefix_)

            if msg_.type in [WechatMsgType.PICTURE]:
                send_to_.send_image(path=self._path.get_msg_cache_path(msg_.id))

            # elif msg.type in [WechatMsgType.VIDEO]:
            #     send_to.send_video(path=self._path.msg_cache_path(msg.id))
            #
            # elif msg.type in WechatMsgType.ATTACH_MSG:
            #     send_to.send_file(path=self._path.msg_cache_path(msg.id))

        else:
            msg_.forward(send_to_,
                         prefix=self._get_name_prefix(msg_=msg_) + self._get_prefix(
                             msg_=msg_) if not prefix_ else prefix_)

    def _get_prefix(self, msg_):
        if msg_.type == WechatMsgType.TEXT:
            _get_prefix_func = self._get_prefix_text
        elif msg_.type == WechatMsgType.RECORDING:
            _get_prefix_func = self._get_prefix_recording
        elif msg_.type == WechatMsgType.PICTURE:
            _get_prefix_func = self._get_prefix_picture
        elif msg_.type == WechatMsgType.VIDEO:
            _get_prefix_func = self._get_prefix_video
        elif msg_.type == WechatMsgType.SHARING:
            _get_prefix_func = self._get_prefix_sharing
        elif msg_.type == WechatMsgType.CARD:
            _get_prefix_func = self._get_prefix_card
        elif msg_.type == WechatMsgType.MAP:
            _get_prefix_func = self._get_prefix_map
        elif msg_.type == WechatMsgType.ATTACHMENT:
            _get_prefix_func = self._get_prefix_attachment
        else:
            _get_prefix_func = None

        if _get_prefix_func:
            return _get_prefix_func(msg_)
        else:
            return ''

    @staticmethod
    def _get_name_prefix(msg_):
        prefix = msg_.member.nick_name if msg_.member else r'你'
        return prefix

    @staticmethod
    def _get_prefix_text(msg_):
        prefix = r'说：'
        return prefix

    @staticmethod
    def _get_prefix_recording(msg_):
        prefix = r'发了条{}秒的语音：'.format(int(round(msg_.voice_length / 1000)))
        return prefix

    def _get_prefix_picture(self, msg_):
        img_type = os.path.splitext(msg_.file_name)[1]
        prefix_1 = r'发了个图片：'
        prefix_2 = r'发了个表情：'
        prefix_3 = r'发了个微信商店里的俗表情'
        return prefix_1 if img_type != '.gif' else \
            prefix_2 if os.path.getsize(self._path.get_msg_cache_path(msg_id_=msg_.id)) else prefix_3

    @staticmethod
    def _get_prefix_video(msg_):
        prefix = r'发了个{}秒的视频，不过我已经把它保存到电脑上了'.format(int(round(msg_.play_length)))
        return prefix

    @staticmethod
    def _get_prefix_sharing(msg_):
        prefix = r'分享了个链接：'
        return prefix

    @staticmethod
    def _get_prefix_card(msg_):
        prefix = r'分享了一张{}的名片'.format(msg_.card.nick_name)
        return prefix

    @staticmethod
    def _get_prefix_map(msg_):
        prefix = r'分享了一个位置：'
        return prefix

    @staticmethod
    def _get_prefix_attachment(msg_):
        file_type = os.path.splitext(msg_.file_name)[1]
        prefix = r'发了个{:.2f}KB的{}文件，不过我已经把它保存到电脑上了'.format(msg_.file_size / 1024, file_type[1:])
        return prefix
