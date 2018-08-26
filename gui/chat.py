# coding=utf-8
"""..."""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QCheckBox, QGridLayout, QListWidget, QPushButton, QVBoxLayout, QWidget
from gui.utilities import GuiUtils


class ChatSetter(QWidget):
    """..."""
    saved = pyqtSignal(str, bool, list)

    def __init__(self, name_):
        super(ChatSetter, self).__init__()
        self._name = name_
        self._setup_ui()

    def enable(self, enable_):
        """..."""
        self._enable.setChecked(enable_)

    def display_filter(self, filter_list_):
        """..."""
        self._filter.clear()
        self._filter.addItems(filter_list_)

    def _setup_ui(self):
        _vbox = QVBoxLayout()
        self._enable = QCheckBox(self._name)
        self._filter = QListWidget()
        self._filter.setSelectionMode(QAbstractItemView.SingleSelection)
        _vbox.addWidget(self._enable)
        _vbox.addWidget(self._filter)
        _vbox.addLayout(self._gen_filter_btn_group())
        self.setLayout(_vbox)

    def _gen_filter_btn_group(self):
        _add = QPushButton('Add')
        _add.clicked.connect(self._add_filter)
        _edit = QPushButton('Edit')
        _edit.clicked.connect(self._edit_filter)
        _delete = QPushButton('Delete')
        _delete.clicked.connect(self._delete_filter)
        _save = QPushButton('Save')
        _save.clicked.connect(self._save_filter)

        _btn_group = QGridLayout()
        _btn_group.addWidget(_add, 0, 0)
        _btn_group.addWidget(_edit, 0, 1)
        _btn_group.addWidget(_delete, 1, 0)
        _btn_group.addWidget(_save, 1, 1)
        _btn_group.setSpacing(0)
        return _btn_group

    def _add_filter(self):
        _name = GuiUtils.input_dialog(self, 'Filter', 'Add filter:')
        if _name:
            self._filter.addItem(_name)

    def _edit_filter(self):
        try:
            _item = self._filter.currentItem()
            _name = GuiUtils.input_dialog(self, 'Filter', 'Add filter:', _item.text())
            if _name:
                print('!!!')
        except Exception as e:
            _msg = 'Choose one item before editing.'
            print(_msg)

    def _delete_filter(self):
        try:
            _item = self._filter.currentItem()
            if GuiUtils.question_dialog(self, 'Filter', 'Delete filter: ' + _item.text()):
                _item = self._filter.takeItem(self._filter.currentRow())
                del _item
        except Exception as e:
            _msg = 'Choose one item before deleting.'
            print(_msg)

    def _save_filter(self):
        self.saved.emit(self._name, self._enable.isChecked(),
                        [self._filter.item(_index).text() for _index in range(self._filter.count())])
