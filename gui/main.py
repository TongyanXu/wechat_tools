# coding=utf-8
"""..."""
__author__ = 'Tongyan Xu'

import sys
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QCheckBox, QHBoxLayout, QListWidget
from PyQt5.QtWidgets import QListWidgetItem, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from config import config
from gui.definitions import Separator, WidgetType
from gui.chat import ChatSetter
from gui.utilities import GuiUtils
from main_tool import WechatTools, tools


class WechatThread(QObject):
    """..."""
    signal = pyqtSignal(str)

    def __init__(self, config_):
        super(WechatThread, self).__init__()
        self._wechat_tool = None
        self._config = config_

    def run(self):
        """..."""
        self._wechat_tool = WechatTools(config_=self._config, sub_thread_=True)
        self._wechat_tool.run()

    def stop(self):
        """..."""
        self._wechat_tool.stop()
        self._wechat_tool = None


class MainWindow(QMainWindow):
    """..."""
    def __init__(self, config_, tools_):
        super(MainWindow, self).__init__()
        self._config = config_
        self._tools = tools_
        self._setup_sub_thread()
        self._setup_ui()
        self.show()

    def _setup_ui(self):
        self.setWindowTitle('Wechat Tools')
        self.setGeometry(100, 100, 600, 400)
        self._set_menu_bar()
        self._set_main_window()

    def _set_main_window(self):
        _tab = QTabWidget()
        self._info_window = self._set_tool_window()
        self._console_window = GuiUtils.console_window()
        _tab.addTab(self._info_window, 'Tools Settings')
        _tab.addTab(self._console_window, 'Console Window')
        _tab.currentChanged.connect(self._save_tool)
        self.setCentralWidget(_tab)

    def _set_tool_window(self):
        _window = QWidget()
        _win_layout = QHBoxLayout()

        _tool_list = QWidget()
        _vbox = QVBoxLayout()
        self._all_tools = QCheckBox('Wechat Tools')
        self._all_tools.stateChanged.connect(self._on_check_all)
        self._tool_list = QListWidget()
        self._tool_list.setSelectionMode(QAbstractItemView.SingleSelection)
        for _t in self._tools:
            _enable = self._config[_t['config_key']]['enable']
            _check_state = Qt.Checked if _enable else Qt.Unchecked
            _item = QListWidgetItem()
            _item.setText(_t['type'])
            _item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            _item.setCheckState(_check_state)
            self._tool_list.addItem(_item)
        self._tool_list.itemClicked.connect(self._on_tool_clicked)

        _vbox.addWidget(self._all_tools)
        _vbox.addWidget(self._tool_list)
        _tool_list.setLayout(_vbox)
        _win_layout.addWidget(_tool_list)

        self._friend_filter = ChatSetter('Friend Chat')
        self._friend_filter.saved.connect(self._save_filter)
        _win_layout.addWidget(self._friend_filter)
        self._group_filter = ChatSetter('Group Chat')
        self._group_filter.saved.connect(self._save_filter)
        _win_layout.addWidget(self._group_filter)

        self._default_tool = 0
        self._tool_list.setCurrentRow(self._default_tool)
        self._display_tool_setting(self._default_tool)
        self._tool_list.currentItem().setBackground(QColor(0, 105, 217))
        self._tool_list.currentItem().setForeground(QColor('white'))

        _window.setLayout(_win_layout)
        return _window

    def _on_check_all(self):
        if self._all_tools.isChecked():
            for _index in range(self._tool_list.count()):
                self._tool_list.item(_index).setCheckState(Qt.Checked)
        else:
            for _index in range(self._tool_list.count()):
                self._tool_list.item(_index).setCheckState(Qt.Unchecked)

    def _on_tool_clicked(self, item_):
        self._tool_list.setCurrentItem(item_)
        for _index in range(self._tool_list.count()):
            self._tool_list.item(_index).setBackground(QColor('white'))
            self._tool_list.item(_index).setForeground(QColor('black'))
        item_.setBackground(QColor(0, 105, 217))
        item_.setForeground(QColor('white'))
        _index = self._tool_list.currentRow()
        self._display_tool_setting(_index)

    def _display_tool_setting(self, tool_index_):
        _config = self._config[self._tools[tool_index_]['config_key']]
        _friend_enable = _config['friend_enable']
        _group_enable = _config['group_enable']
        _friend_filter = _config['friend_filter']
        _group_filter = _config['group_filter']
        self._friend_filter.enable(_friend_enable)
        self._group_filter.enable(_group_enable)
        self._friend_filter.display_filter(_friend_filter)
        self._group_filter.display_filter(_group_filter)

    def _save_filter(self, name_, enable_, filter_):
        _index = self._tool_list.currentRow()
        _config = self._config[self._tools[_index]['config_key']]
        if name_ == 'Friend Chat':
            _config['friend_enable'] = enable_
            _config['friend_filter'] = filter_
        elif name_ == 'Group Chat':
            _config['group_enable'] = enable_
            _config['group_filter'] = filter_

    def _save_tool(self):
        for _index in range(self._tool_list.count()):
            self._config[self._tools[_index]['config_key']]['enable'] = \
                self._tool_list.item(_index).checkState() == Qt.Checked

    def _set_menu_bar(self):
        self._menu_bar = self.menuBar()
        self._menu_bar.setNativeMenuBar(False)
        _menu = {
            'Main.Run': (self._run, 'Ctrl+R'),
            'Main.Stop': (self._stop, 'Ctrl+T'),
            'Main.Account': (self._test_action, 'Ctrl+A'),
            'Main.About': (self._test_action, ''),
            'Main.Quit': (self._quit, 'Ctrl+Q'),
            'View.Show Log.Main': (self._test_action, ''),
            'View.Show Log.Recall-Blocker': (self._test_action, ''),
            'View.Show Log.Auto-Replier': (self._test_action, ''),
            'View.Show Log.Auto-Repeater': (self._test_action, ''),
            'View.Show Log.Combined': (self._test_action, ''),
            'View.Clean Log': (self._clean_log, ''),
            'Settings.Edit Settings': (self._test_action, 'Ctrl+Alt+S'),
            'Settings.Import Settings': (self._test_action, 'Ctrl+Alt+I'),
            'Settings.Export Settings': (self._test_action, 'Ctrl+Alt+E'),
            'Help.Help': (self._test_action, '')
        }
        for _menu_name, _menu_params in _menu.items():
            self._add_menu(_menu_name, _menu_params)

        _stop = self._get_menu_wgt('Main.Stop')
        _stop.setDisabled(True)

    def _add_menu(self, menu_name_, menu_params_, menu_=None):
        _menu = menu_ if menu_ else self._menu_bar
        _menu_group = menu_name_.split(Separator.OBJ)
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
            _rest_menu_name = Separator.OBJ.join(_menu_group)
            self._add_menu(_rest_menu_name, menu_params_, _sub_menu)

    def _get_menu_wgt(self, menu_name_, menu_=None):
        _menu = menu_ if menu_ else self._menu_bar
        _menu_group = menu_name_.split(Separator.OBJ)
        if len(_menu_group) == 1:
            return GuiUtils.get_widget_by_name(_menu, menu_name_)
        else:
            _sub_menu_name = _menu_group.pop(0)
            _sub_menu = GuiUtils.get_widget_by_name(_menu, _sub_menu_name)
            _rest_menu_name = Separator.OBJ.join(_menu_group)
            return self._get_menu_wgt(_rest_menu_name, _sub_menu)

    def _test_action(self):
        GuiUtils.info_dialog(self, 'Test', 'No integrated yet.')

    def _setup_sub_thread(self):
        self._sub_thread = QThread()
        self._wechat_tools = WechatThread(config_=self._config)
        self._wechat_tools.moveToThread(self._sub_thread)
        self._sub_thread.started.connect(self._wechat_tools.run)

    def _run(self):
        self._save_tool()
        self._sub_thread.start()
        self._get_menu_wgt('Main.Run').setDisabled(True)
        self._get_menu_wgt('Main.Stop').setDisabled(False)

    def _stop(self):
        self._wechat_tools.stop()
        self._sub_thread.terminate()
        self._sub_thread.wait()
        self._get_menu_wgt('Main.Run').setDisabled(False)
        self._get_menu_wgt('Main.Stop').setDisabled(True)

    def _quit(self):
        self.close()

    def closeEvent(self, event):
        """..."""
        if GuiUtils.question_dialog(self, 'Quit', 'Are you sure to quit wechat tools?'):
            event.accept()
        else:
            event.ignore()

    def _clean_log(self):
        self._console_window.text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(config_=config, tools_=tools)
    sys.exit(app.exec_())
