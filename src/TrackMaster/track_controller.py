#! coding:utf-8
"""
track_controller.py

Created by 0160929 on 2016/09/29 16:38
"""
import os

from TrackMaster.signalfigureview import WaveViewer

__version__ = '0.0'

import sys

from PySide.QtGui import *
from PySide.QtCore import *

import iconsloader


__all__ = ["TrackController"]


class TrackController(QWidget):
    DefaultHeight = 50

    def __init__(self, wave_info, parent=None):
        super().__init__(parent)
        self.loader = iconsloader

        print(wave_info)
        self.wavfilepath = wave_info
        self.track_name = os.path.basename(self.wavfilepath)



        self._setup_ui()
        self._setup_connection()

    def _setup_ui(self):
        self.setObjectName("TrackControllers")
        self.setStyleSheet("#TrackControllers{background-color: rgb(0,0,0);}")
        self.setFixedHeight(self.DefaultHeight)

        # Root Layout
        self.hlayout = QHBoxLayout(self)
        # Wave file icon
        self.wav_icon = QLabel(self)
        self.wav_icon.setMinimumWidth(30)
        self.wav_icon.setStyleSheet("image:url(:/resource/wav.png);")
        self.hlayout.addWidget(self.wav_icon)

        # File name
        self.filename_label = QLabel(self)
        self.filename_label.setObjectName("labelf")
        self.filename_label.setStyleSheet("QLabel#labelf{color: rgb(255, 255, 255);}")
        self.filename_label.setText("01 J Dilla Drum kit No. 12.wav")
        self.filename_label.setText(self.track_name)
        self.filename_label.setAlignment(Qt.AlignVCenter)
        self.hlayout.addWidget(self.filename_label)

        # Spacer
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout.addItem(spacerItem)

        # btns
        self.btn_restart = QPushButton(self)
        self.btn_restart.setObjectName("btn_restart")
        self.btn_restart.setStyleSheet(
            "#btn_restart{border-image:url(:/resource/restart_default.png) 0 0 0 0 stretch stretch;}"
            "#btn_restart:pressed{border-image:url(:/resource/restart_push.png) 0 0 0 0 stretch stretch;}")
        self.btn_restart.setFixedSize(QSize(25, 25))
        self.hlayout.addWidget(self.btn_restart)
        # btn
        self.btn_play = QPushButton(self)
        self.btn_play.setObjectName("btn_play")
        self.btn_play.setFixedSize(QSize(25, 25))
        self.btn_play.setStyleSheet("#btn_play{border-image:url(:/resource/play_default.png) 0 0 0 0 stretch stretch;}"
                                    "#btn_play:pressed{border-image:url(:/resource/play_push.png) 0 0 0 0 stretch stretch;}")
        self.hlayout.addWidget(self.btn_play)

        # btn
        self.btn_stop = QPushButton(self)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setStyleSheet("#btn_stop{border-image:url(:/resource/stop_default.png) 0 0 0 0 stretch stretch;}"
                                    "#btn_stop:pressed{border-image:url(:/resource/stop_push.png) 0 0 0 0 stretch stretch;}")
        self.btn_stop.setFixedSize(QSize(25, 25))
        self.hlayout.addWidget(self.btn_stop)

        # btn
        self.btn_pause = QPushButton(self)
        self.btn_pause.setObjectName("btn_pause")
        self.btn_pause.setStyleSheet(
            "#btn_pause{border-image:url(:/resource/pause_default.png) 0 0 0 0 stretch stretch;}"
            "#btn_pause:pressed{border-image:url(:/resource/pause_push.png) 0 0 0 0 stretch stretch;}")
        self.btn_pause.setFixedSize(QSize(25, 25))
        self.hlayout.addWidget(self.btn_pause)

        # wave figure
        # self.wav_viewer = WaveViewer(self, wavpath="audio3.wav")
        self.wav_viewer = WaveViewer(self, wavpath=self.wavfilepath)
        self.hlayout.addWidget(self.wav_viewer)

    def _setup_connection(self):
        self.btn_play.released.connect(self.on_play)
        self.btn_pause.released.connect(self.on_pause)
        self.btn_stop.released.connect(self.on_stop)
        self.btn_restart.released.connect(self.on_restart)
        pass

    @Slot()
    def on_play(self):
        self.wav_viewer.waveviewer_item.on_play()
        pass
    @Slot()
    def on_restart(self):
        self.wav_viewer.waveviewer_item.on_restart()
    @Slot()
    def on_stop(self):
        self.wav_viewer.waveviewer_item.on_stop()
    @Slot()
    def on_pause(self):
        self.wav_viewer.waveviewer_item.on_pause()


def main():
    app = QApplication(sys.argv)
    # app.setStyle('plastique')
    win = TrackController()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
