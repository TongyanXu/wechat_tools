# coding=utf-8
"""..."""


class MessageLanguage(object):
    """..."""
    @classmethod
    def get_msg(cls, language_):
        """..."""
        if language_ == 'en':
            return MessageEn
        elif language_ == 'zh':
            return MessageZh


class MessageEn(MessageLanguage):
    """..."""
    pass


class MessageZh(MessageLanguage):
    """..."""
    pass
