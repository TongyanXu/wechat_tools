# coding=utf-8
"""..."""
__author__ = 'Tongyan Xu'

import sys
from PyQt5.QtWidgets import QInputDialog, QLabel, QLineEdit, QMessageBox, QTextEdit, QVBoxLayout, QWidget
from gui.custom import EmittingStream
from gui.definitions import Separator


class GuiUtils(object):
    """..."""

    @classmethod
    def get_widget_by_name(cls, parent_, name_):
        """..."""
        try:
            if name_ not in parent_.child_map:
                return None
            return parent_.__getattribute__(parent_.child_map[name_])
        except AttributeError:
            return None
        except Exception as e:
            raise str(e)

    @classmethod
    def get_widget_by_obj_name(cls, parent_, obj_name_):
        """..."""
        try:
            return parent_.__getattribute__(obj_name_)
        except AttributeError:
            return None
        except Exception as e:
            raise str(e)

    @classmethod
    def add_widget(cls, parent_, wgt_, wgt_name_, wgt_type_):
        """..."""
        map_ = 'child_map'
        if not hasattr(parent_, map_):
            parent_.__setattr__(map_, {})
        _wgt_obj_name = cls.combine_name([wgt_type_, wgt_name_])
        parent_.__getattribute__(map_)[wgt_name_] = _wgt_obj_name
        parent_.__setattr__(_wgt_obj_name, wgt_)

    @classmethod
    def combine_name(cls, list_of_name_):
        """..."""
        return Separator.OBJ.join(list_of_name_)

    @classmethod
    def info_dialog(cls, parent_, title_, info_):
        """..."""
        _reply = QMessageBox.information(parent_, title_, info_, QMessageBox.Yes, QMessageBox.Yes)
        return _reply == QMessageBox.Yes

    @classmethod
    def question_dialog(cls, parent_, title_, info_):
        """..."""
        _reply = QMessageBox.question(parent_, title_, info_, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return _reply == QMessageBox.Yes

    @classmethod
    def input_dialog(cls, parent_, title_, info_, default_=''):
        """..."""
        _input, _reply = QInputDialog.getText(parent_, title_, info_, QLineEdit.Normal, default_)
        return _input if _reply and (len(_input) != 0) else None

    @classmethod
    def console_window(cls):
        """..."""
        _name = 'Console Window'
        _console_window = QWidget()
        _console_window.setObjectName(_name)

        _console_label = QLabel(_name)
        _console_text = QTextEdit()
        _console_text.setReadOnly(True)

        sys.stdout = EmittingStream(_console_text)
        sys.stderr = EmittingStream(_console_text)

        _vbox = QVBoxLayout()
        _vbox.addWidget(_console_label)
        _vbox.addWidget(_console_text)
        _vbox.setSpacing(0)
        _console_window.setLayout(_vbox)
        _console_window.text = _console_text
        return _console_window
