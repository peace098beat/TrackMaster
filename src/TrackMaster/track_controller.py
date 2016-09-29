#! coding:utf-8
"""
track_controller.py

Created by 0160929 on 2016/09/29 16:38
"""
from PySide.QtCore import QSize, Qt
from TrackMaster.signalfigureview import WaveViewer

__version__ = '0.0'

import sys

from PySide.QtGui import *

__all__ = ["TrackController"]


class TrackController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TrackControllers")
        self.setStyleSheet("#TrackControllers{background-color: rgb(0,0,0);}")
        self.setFixedHeight(50)
        self.hlayout = QHBoxLayout(self)
        # Wave file icon
        self.wav_icon = QLabel(self)
        self.wav_icon.setPixmap(QPixmap("./resource/wav.png"))
        self.wav_icon.resize(20,20)
        self.wav_icon.setFixedSize(QSize(25,25))
        self.hlayout.addWidget(self.wav_icon)

        # File name
        self.filename_label = QLabel(self)
        self.filename_label.setObjectName("labelf")
        self.filename_label.setStyleSheet("QLabel#labelf{"
                                          "color: rgb(255, 255, 255);}")
        self.filename_label.setText("01 J Dilla Drum kit No. 12.wav")
        self.filename_label.setAlignment(Qt.AlignVCenter)
        self.hlayout.addWidget(self.filename_label)

        # Spacer
        spacerItem = QSpacerItem(20,40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout.addItem(spacerItem)

        # icons
        # self.icon_play = QIcon("./resource/wav.png")
        # self.icon_play.set(QSize(25,25))
        # btns
        self.btn_play = QPushButton(self)
        self.btn_play.setIcon(QIcon(QPixmap("./resource/wav.png")))
        self.btn_play.setFixedSize(QSize(25,25))
        self.hlayout.addWidget(self.btn_play)

        self.btn_stop = QPushButton(self)
        self.btn_stop.setIcon(QIcon(QPixmap("./resource/wav.png")))
        self.btn_stop.setFixedSize(QSize(25,25))
        self.hlayout.addWidget(self.btn_stop)

        self.btn_pause = QPushButton(self)
        self.btn_pause.setIcon(QIcon(QPixmap("./resource/wav.png")))
        self.btn_pause.setFixedSize(QSize(25,25))
        self.hlayout.addWidget(self.btn_pause)


        self.btn_allplay = QPushButton(self)
        self.btn_allplay.setIcon(QIcon(QPixmap("./resource/wav.png")))
        self.btn_allplay.setFixedSize(QSize(25,25))
        self.hlayout.addWidget(self.btn_allplay)
        # wave figure
        self.wav_viewer = WaveViewer(self)
        self.hlayout.addWidget(self.wav_viewer)


def main():
    app = QApplication(sys.argv)
    # app.setStyle('plastique')
    win = TrackController()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
