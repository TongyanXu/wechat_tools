# coding=utf-8
"""..."""
__author__ = 'Tongyan Xu'

from PyQt5.QtWidgets import QAction, QMenuBar
from gui.utilities import GuiUtils
from gui.definitions import WidgetType


class MenuBar(QMenuBar):
    """..."""
    def __init__(self, parent_, menu_):
        self._parent = parent_
        super(MenuBar, self).__init__(self._parent)
        self.setNativeMenuBar(False)
        for _menu_name, _menu_params in menu_.items():
            self._add_menu(_menu_name, _menu_params)

    def _add_menu(self, menu_name_, menu_params_, menu_=None):
        _menu = menu_ if menu_ else self
        _menu_group = menu_name_.split('.')
        if len(_menu_group) == 1:
            _menu_btn = QAction(menu_name_, self)
            _menu_btn.triggered.connect(menu_params_[0])
            _menu_btn.setShortcut(menu_params_[1])
            GuiUtils.add_widget(_menu, _menu_btn, menu_name_, WidgetType.BTN)
            _menu.addAction(_menu_btn)
        else:
            _sub_menu_name = _menu_group.pop(0)
            _sub_menu = GuiUtils.get_widget_by_name(_menu, _sub_menu_name) or _menu.addMenu(_sub_menu_name)
            GuiUtils.add_widget(_menu, _sub_menu, _sub_menu_name, WidgetType.MENU)
            _rest_menu_name = '.'.join(_menu_group)
            self._add_menu(_rest_menu_name, menu_params_, _sub_menu)

    def _get_menu_wgt(self, menu_name_, menu_=None):
        _menu = menu_ if menu_ else self
        _menu_group = menu_name_.split('.')
        if len(_menu_group) == 1:
            return GuiUtils.get_widget_by_name(_menu, menu_name_)
        else:
            _sub_menu_name = _menu_group.pop(0)
            _sub_menu = GuiUtils.get_widget_by_name(_menu, _sub_menu_name)
            _rest_menu_name = '.'.join(_menu_group)
            return self._get_menu_wgt(_rest_menu_name, _sub_menu)
