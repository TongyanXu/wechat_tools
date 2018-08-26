# coding=utf-8
"""..."""
__author__ = 'Tongyan Xu'

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor


class EmittingStream(QObject):
    """..."""
    textWritten = pyqtSignal(str)

    def __init__(self, console_window_):
        super(EmittingStream, self).__init__()
        self._console_window = console_window_
        self.textWritten.connect(self._stream_to_wgt)

    def write(self, text):
        """..."""
        self.textWritten.emit(str(text))

    def _stream_to_wgt(self, text):
        cursor = self._console_window.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self._console_window.setTextCursor(cursor)
        self._console_window.ensureCursorVisible()
