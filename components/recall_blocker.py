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
        self._sticker_config = self._config.get('sticker', {})
        self._sticker_lib = {}

    def _register_auto_func(self, chat_type_=None):
        @self._bot.register(chats=chat_type_.type, enabled=True, msg_types=WechatMsgType.LARGE_MSG)
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
                        if self._sticker_config.get('send_sticker'):
                            self._reply_sticker(msg_=msg, sticker_name_=self._sticker_config.get('sticker_name'))
                        self._send_msg(msg_=msg)

    def _get_msg_by_id(self, msg_id_=None):
        if msg_id_:
            _msg_list = self._bot.messages.search(id=msg_id_)
            if _msg_list:
                _msg = _msg_list[0]
                return _msg
        return None

    def _get_recall_msg(self, note_=None):
        if note_ and re.search(r'<!\[CDATA\[.*撤回了一条消息\]\]>', note_.raw.get('Content')) \
                and re.search(r'<!\[CDATA\[(.*?)撤回了一条消息\]\]>', note_.raw.get('Content')).group(1) != '你':
            _msg_id = int(re.search('<msgid>(.*?)</msgid>', note_.raw.get('Content')).group(1))
            _msg = self._get_msg_by_id(msg_id_=_msg_id)
            return _msg, note_.create_time
        return None, None

    def _backup_msg(self, msg_, recall_time_):
        _prefix = r'{} 于 {} 撤回了 {} 消息: '.format(
            self._gen_log_sender(msg_), recall_time_.strftime(self._default_time_format), msg_.type)
        self._send_msg(msg_=msg_, prefix_=_prefix, send_to_=self._bot.file_helper)
        self._logger.info(_prefix[:-2])

    def _reply_sticker(self, msg_, sticker_name_=None):
        _sticker_path = self._path.get_sticker_path(sticker_name_=sticker_name_)
        if _sticker_path:
            if _sticker_path not in self._sticker_lib:
                _media_id = self._bot.upload_file(_sticker_path)
                self._sticker_lib[_sticker_path] = _media_id
                msg_.reply_image(path=_sticker_path, media_id=self._sticker_lib[_sticker_path])

    def _send_msg(self, msg_, prefix_=None, send_to_=None):
        if not send_to_:
            send_to_ = msg_.sender

        if msg_.type in WechatMsgType.SPECIAL_MSG:
            if msg_.type in [WechatMsgType.PICTURE] and not msg_.raw.get('HasProductId'):
                return self._forward_msg(msg_=msg_, prefix_=prefix_, send_to_=send_to_)
            send_to_.send_msg(
                msg=self._get_name_prefix(msg_=msg_) + self._get_prefix(msg_=msg_) if not prefix_ else prefix_)

        else:
            self._forward_msg(msg_=msg_, prefix_=prefix_, send_to_=send_to_)

    def _forward_msg(self, msg_, prefix_=None, send_to_=None):
        msg_.forward(
            send_to_, prefix=self._get_name_prefix(msg_=msg_) + self._get_prefix(msg_=msg_) if not prefix_ else prefix_)

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
        _prefix = msg_.member.nick_name if msg_.member else r'你'
        return _prefix

    @staticmethod
    def _get_prefix_text(msg_):
        _prefix = r'说：'
        return _prefix

    @staticmethod
    def _get_prefix_recording(msg_):
        _prefix = r'发了条{}秒的语音：'.format(int(round(msg_.voice_length / 1000)))
        return _prefix

    @staticmethod
    def _get_prefix_picture(msg_):
        _img_type = os.path.splitext(msg_.file_name)[1]
        _prefix_1 = r'发了个图片：'
        _prefix_2 = r'发了个表情：'
        _prefix_3 = r'发了个微信商店里的俗表情'
        return _prefix_1 if _img_type != '.gif' else _prefix_3 if msg_.raw.get('HasProductId') else _prefix_2

    @staticmethod
    def _get_prefix_video(msg_):
        _prefix = r'发了个{}秒的视频，不过我已经把它保存到电脑上了'.format(int(round(msg_.play_length)))
        return _prefix

    @staticmethod
    def _get_prefix_sharing(msg_):
        _prefix = r'分享了个链接：'
        return _prefix

    @staticmethod
    def _get_prefix_card(msg_):
        _prefix = r'分享了一张{}的名片'.format(msg_.card.nick_name)
        return _prefix

    @staticmethod
    def _get_prefix_map(msg_):
        _prefix = r'分享了一个位置：'
        return _prefix

    @staticmethod
    def _get_prefix_attachment(msg_):
        _file_type = os.path.splitext(msg_.file_name)[1]
        _prefix = r'发了个{:.2f}KB的{}文件，不过我已经把它保存到电脑上了'.format(msg_.file_size / 1024, _file_type[1:])
        return _prefix
