# coding=utf-8
"""..."""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAbstractItemView, QCheckBox, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
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
        for _name in filter_list_:
            _item = QListWidgetItem(_name)
            _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self._filter.addItem(_item)

    def _on_clicked(self, item_):
        self._filter.setCurrentItem(item_)
        for _index in range(self._filter.count()):
            self._filter.item(_index).setBackground(QColor('white'))
            self._filter.item(_index).setForeground(QColor('black'))
        item_.setBackground(QColor(0, 105, 217))
        item_.setForeground(QColor('white'))

    def _setup_ui(self):
        _vbox = QVBoxLayout()
        self._enable = QCheckBox(self._name)
        self._filter = QListWidget()
        self._filter.itemClicked.connect(self._on_clicked)
        self._filter.itemChanged.connect(self._save_filter)
        self._filter.setSelectionMode(QAbstractItemView.SingleSelection)
        _vbox.addWidget(self._enable)
        _vbox.addWidget(self._filter)
        _vbox.addLayout(self._gen_filter_btn_group())
        self.setLayout(_vbox)

    def _gen_filter_btn_group(self):
        _add = QPushButton('Add')
        _add.clicked.connect(self._add_filter)
        _delete = QPushButton('Delete')
        _delete.clicked.connect(self._delete_filter)

        _btn_group = QHBoxLayout()
        _btn_group.addWidget(_add)
        _btn_group.addWidget(_delete)
        _btn_group.setSpacing(0)
        return _btn_group

    def _add_filter(self):
        _name = GuiUtils.input_dialog(self, 'Filter', 'Add filter:')
        if _name:
            _item = QListWidgetItem(_name)
            _item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self._filter.addItem(_item)
            self._save_filter()

    def _delete_filter(self):
        try:
            _item = self._filter.currentItem()
            if GuiUtils.question_dialog(self, 'Filter', 'Delete filter: ' + _item.text()):
                _item = self._filter.takeItem(self._filter.currentRow())
                del _item
                self._save_filter()
        except Exception as e:
            _msg = 'Choose one item before deleting.'
            print(_msg)

    def _save_filter(self):
        self.saved.emit(self._name, self._enable.isChecked(),
                        [self._filter.item(_index).text() for _index in range(self._filter.count())])
