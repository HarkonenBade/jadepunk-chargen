import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from .. import AspectTypes, AttrTypes


class Scribe(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        self.center()
        self.setWindowTitle('Scribe')
        self.setWindowIcon(QIcon('jadepunk/scribe/icons/script_edit.png'))

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.main = QHBoxLayout()

        self.menubar = QMenuBar()
        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.main.setMenuBar(self.menubar)


        self.button_panel = QVBoxLayout()
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.stack = QStackedWidget()

        self.char_tab = self.setup_char_tab()
        self.aspect_tab = self.setup_aspects_tab()
        self.attrs_tab = self.setup_attrs_tab()
        self.assets_tab = self.create_tab("Assets")

        self.button_panel.addStretch(1)

        self.button_group.buttonClicked.connect(lambda button: self.stack.setCurrentIndex(self.button_group.id(button)))

        self.main.addLayout(self.button_panel)
        self.main.addWidget(self.stack)

        self.setLayout(self.main)

        self.show()

    def create_tab(self, name):
        page = QGroupBox(name)
        selecter_button = QPushButton(name)
        selecter_button.setCheckable(True)
        self.button_panel.addWidget(selecter_button)
        self.stack.addWidget(page)
        self.button_group.addButton(selecter_button, self.stack.indexOf(page))
        return page

    def setup_char_tab(self):
        tab = self.create_tab("Character")

        fl = QFormLayout()

        tab.name = QLineEdit()
        tab.background = QTextEdit()

        fl.addRow("Name", tab.name)
        fl.addRow("Background", tab.background)

        tab.setLayout(fl)
        return tab

    def setup_aspects_tab(self):
        tab = self.create_tab("Aspects")

        fl = QFormLayout()

        tab.entries = {}

        for asp in AspectTypes:
            entry = QLineEdit()
            tab.entries[asp] = entry
            fl.addRow(asp.value, entry)

        tab.setLayout(fl)
        return tab

    def setup_attrs_tab(self):
        tab = self.create_tab("Attributes")

        hb = QHBoxLayout()

        fl = QFormLayout()

        tab.entries = {}

        for attr in AttrTypes:
            entry = QSpinBox()
            entry.setRange(0, 5)
            tab.entries[attr] = entry
            fl.addRow(attr.value, entry)

        hb.addLayout(fl)
        hb.addStretch(1)

        tab.setLayout(hb)
        return tab

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def run():
    app = QApplication(sys.argv)
    Scribe()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
