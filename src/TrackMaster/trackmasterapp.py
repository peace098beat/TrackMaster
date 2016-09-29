#! coding:utf-8
"""
trackmasterapp.py

Created by 0160929 on 2016/09/29 16:36
"""
import os

__version__ = '0.1'

import sys

from PySide.QtGui import *
from PySide.QtCore import *

from track_controller import TrackController

class TrackMasterApp(QWidget):
    def __init__(self, parent=None):
        # QMainWindow.__init__(self)
        super().__init__(parent)
        self.setWindowTitle("Track Master")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAcceptDrops(True) # D&D Flag

        # init
        self._setupUi()

    def _setupUi(self):
        # self
        self.setObjectName("TrackMasterApp")
        self.resize(1024, 480)
        self.setStyleSheet("#TrackMasterApp{background-color: rgb(0,0,0);}")
        # top layout
        self.vlayout = QVBoxLayout(self)
        # Header QLabel
        self.header_label = QLabel(self)
        self.header_label.setObjectName("header_label")
        self.header_label.setMinimumSize(QSize(0, 40))
        font = QFont()
        font.setFamily("Myriad Arabic")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setStyleSheet("#header_label{background-color: rgb(149, 0, 2);\n" "color: rgb(255, 255, 255);}")
        self.header_label.setText("  TRACK MASTER")
        self.vlayout.addWidget(self.header_label)
        # Scroll Area
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("#scrollArea{background-color: rgb(0, 0, 0);}")
        self.scrollArea.setWidgetResizable(True)
        self.vlayout.addWidget(self.scrollArea)
        # Scroll Area Widget Contents (Important)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 720,480))
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents{background-color: rgb(0, 255, 0);}")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # ScrollAreaWidgetContents Layout
        self.scrl_contents_vlayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrl_contents_vlayout.setSpacing(0)

        # Track Controllers
        self.track_controller1 = TrackController()
        self.scrl_contents_vlayout.addWidget(self.track_controller1)

        self.track_controller_s = []
        for i in range(10):
            tc = TrackController()
            self.scrl_contents_vlayout.addWidget(tc)
            self.track_controller_s.append(tc)

        # Spacer
        spacerItem = QSpacerItem(20,40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scrl_contents_vlayout.addItem(spacerItem)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        objs = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        for u in objs:
            ext = os.path.splitext(u)[1]
            if ext in (".wav",".WAV"):
                print(u)


def main():
    app = QApplication(sys.argv)
    # app.setStyle('plastique')
    win = TrackMasterApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
