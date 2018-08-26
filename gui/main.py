# coding=utf-8
"""..."""
__author__ = 'Tongyan Xu'

import sys
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, QMainWindow, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from config import config
from gui.definitions import SEPARATOR, WidgetType
from gui.utilities import GuiUtils
from main_tool import WechatTools


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
        self._wechat_tool.stop()
        self._wechat_tool = None


class MainWindow(QMainWindow):
    """..."""
    def __init__(self):
        super(MainWindow, self).__init__()
        self._setup_sub_thread()
        self._setup_ui()
        self.show()

    def _setup_ui(self):
        self.setWindowTitle('Wechat Tools')
        self.setGeometry(100, 100, 800, 600)
        self._set_menu_bar()
        self._set_main_window()

    def _set_main_window(self):
        self._sub_window = QWidget()
        _grid = QGridLayout(self._sub_window)
        self._info_window = self._set_info_window()
        self._console_window = GuiUtils.console_window()
        _grid.addWidget(self._info_window, 0, 0, 1, 2)
        _grid.addWidget(self._console_window, 0, 2, 1, 3)
        self._sub_window.setLayout(_grid)
        self.setCentralWidget(self._sub_window)

    def _set_info_window(self):
        _name = 'Info Window'
        _info_window = QWidget()
        _info_window.setObjectName(_name)

        _tool = QGridLayout()
        _tool_label = QLabel('Wechat Tool')
        _tool_type = QComboBox()
        _tool.addWidget(_tool_label, 0, 0, 1, 4)
        _tool.addWidget(_tool_type, 0, 4, 1, 16)

        _tool_enabled_label = QLabel('Enabled')
        _tool_enabled = QCheckBox()
        _tool.addWidget(_tool_enabled_label, 0, 20, 1, 3, Qt.AlignRight)
        _tool.addWidget(_tool_enabled, 0, 23, 1, 1, Qt.AlignRight)

        _friend = QVBoxLayout()
        _friend_label = QLabel('Friend Chat')
        _friend_text = QTextEdit()
        _friend.addWidget(_friend_label)
        _friend.addWidget(_friend_text)
        _friend.setSpacing(0)

        _group = QVBoxLayout()
        _group_label = QLabel('Group Chat')
        _group_text = QTextEdit()
        _group.addWidget(_group_label)
        _group.addWidget(_group_text)
        _group.setSpacing(0)

        _vbox = QVBoxLayout()
        _vbox.addLayout(_tool)
        _vbox.addLayout(_friend)
        _vbox.addLayout(_group)
        _info_window.setLayout(_vbox)
        return _info_window

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
        _menu_group = menu_name_.split(SEPARATOR)
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
            _rest_menu_name = SEPARATOR.join(_menu_group)
            self._add_menu(_rest_menu_name, menu_params_, _sub_menu)

    def _get_menu_wgt(self, menu_name_, menu_=None):
        _menu = menu_ if menu_ else self._menu_bar
        _menu_group = menu_name_.split(SEPARATOR)
        if len(_menu_group) == 1:
            return GuiUtils.get_widget_by_name(_menu, menu_name_)
        else:
            _sub_menu_name = _menu_group.pop(0)
            _sub_menu = GuiUtils.get_widget_by_name(_menu, _sub_menu_name)
            _rest_menu_name = SEPARATOR.join(_menu_group)
            return self._get_menu_wgt(_rest_menu_name, _sub_menu)

    def _test_action(self):
        GuiUtils.info_dialog(self, 'Quit', 'No integrated yet.')

    def _setup_sub_thread(self):
        self._sub_thread = QThread()
        self._wechat_tools = WechatThread(config_=config)
        self._wechat_tools.moveToThread(self._sub_thread)
        self._sub_thread.started.connect(self._wechat_tools.run)

    def _run(self):
        self._sub_thread.start()
        print('Start running wechat tools on tid {}'.format(self._sub_thread.currentThreadId()))
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
    ex = MainWindow()
    sys.exit(app.exec_())
