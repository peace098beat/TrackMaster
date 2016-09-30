# -*- coding: utf-8 -*-
"""
wavefigure.py

ステレオ対応

"""
import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *
import numpy as np

from player import Player


class WaveViewItem(QGraphicsItem):
    DefaultViewWidth = 512
    DefaultViewHeight = 30

    def __init__(self, wavpath):
        super().__init__()

        # Color
        self.item_bg_color = QColor(255, 255, 255)
        self.fig_bg_color = QColor(200, 200, 200)
        self.border_color = QColor(0, 0, 0)
        self.series_line_colors = [
            QColor(100, 0, 0), QColor(0, 100, 0), QColor(0, 0, 1)]
        self.cursor_current_color = QColor(30, 30, 30)

        # Size
        self.spacing = 0
        self.bounding = QRectF(
            0, 0, self.DefaultViewWidth, self.DefaultViewHeight)
        self.figure_bound = QRectF(
            self.spacing, self.spacing,
            self.DefaultViewWidth - (self.spacing * 2), self.DefaultViewHeight - (self.spacing * 2))
        self.series = []

        self.set_audio(wavpath)

    def set_audio(self, wavpath):
        """audio plot"""
        import wave
        # audio load
        # wf = wave.open("audio3.wav", 'rb')
        wf = wave.open(wavpath, 'rb')
        rate = wf.getframerate()
        nframes = wf.getnframes()
        nchannels = wf.getnchannels()
        bits = wf.getsampwidth() * 8

        wf.rewind()
        wbuffer = wf.readframes(nframes)

        if bits == 8:
            x = np.frombuffer(wbuffer, dtype=np.int8)
        elif bits == 16:
            x = np.frombuffer(wbuffer, dtype=np.int16)
        elif bits == 32:
            x = np.frombuffer(wbuffer, dtype=np.int32)
        elif bits == 24:
            # 24bitの場合の特別処理 ※24bitのオーディオデータは実装の都合上16bit化
            x = np.frombuffer(wbuffer, 'b').reshape(-1, 3)[:, 1:].flatten().view('i2')
        else:
            raise Warning("SignalFigureView.set_audio(). bits {} is none".format(bits))
        del wbuffer

        # 正規化
        if bits == 24:
            # 24bitの場合の特別処理 ※24bitのオーディオデータは実装の都合上16bit化.
            byte = 2.
            amp = (2. ** 8) ** byte / 2 - 1
        else:
            byte = bits / 8
            amp = (2. ** 8) ** byte / 2 - 1
        x = x / float(amp)

        # モノラル化
        if nchannels > 1:
            x = (x[::2] + x[1::2]) / 2
        assert x.size == nframes

        del wf, bits, byte, amp

        # buffer
        bit = int(np.ceil(np.log2(nframes)))
        self.buffer_size = 2 ** bit
        buffer = np.zeros(self.buffer_size, dtype=np.float32)
        buffer[:nframes] = x
        del x

        # Player Setup
        chunk_size = 128
        self.p = Player(buffer, chunk_size=chunk_size, rate=rate, live=True)
        self.buffer = buffer.copy()
        self.buffer.flags.writeable = False
        del buffer

        self.img_chunk_size = self.DefaultViewWidth
        # Repaint Timer
        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        # fps
        self.fps_oldtime = time.clock()
        self.fps = 0
        # zoom
        self.scale_maxnum = np.log2(self.buffer_size / self.img_chunk_size)
        self.scale_number = self.scale_maxnum
        self.scale_minnum = 1
        self.scale_delta = 1
        # player controller
        self.cursor_current_px = 0
        # frame manage
        self.current_frame = 0

    def on_play(self):
        """(stopping, playing)カレントカーソルから再生開始"""
        self.p.resume(self.current_frame)

    def on_pause(self):
        """ (stopping)カレントカーソルから再生開始 / (playing)再生停止.カレントカーソルをテンポラリカーソルに変更
        """
        if self.p.paused is True:
            self.p.resume(self.current_frame)
        else:
            self.p.pause()
            self.current_frame = self.p.get_nowframe()

    def on_stop(self):
        """ stop: (playing)再生を停止.カレントカーソルはそのまま / (stopping) None"""
        self.p.pause()
        self.p.set_nowframe(self.current_frame)

    def on_restart(self):
        """ (stopping, playing) 先頭から再生"""
        self.p.resume(0)
        self.current_frame = 0

    def on_click(self, x, y):
        frame = self.start + x * self.nstep
        self.current_frame = frame
        self.p.set_nowframe(frame)

    def timeout(self):
        """update timer"""
        frame = self.p.get_nowframe()

        chunk_size = self.img_chunk_size
        harf_chunk = chunk_size / 2
        amp = self.DefaultViewHeight / 2.

        # スケールの最大値調整
        nstep = 2 ** self.scale_number

        # 再生サンプル位置をグラフのx=0に設定
        _start, _end = frame, frame + (chunk_size * nstep)
        # 再生サンプル位置をグラフのx=centerに設定
        start, end = _start - (harf_chunk * nstep), _end - (harf_chunk * nstep)

        # 端部処理
        if start < 0:
            start, end = 0, chunk_size * nstep
        elif self.buffer_size < end:
            start, end = self.buffer_size - (chunk_size * nstep), self.buffer_size

        # 格納
        self.start, self.end, self.nstep = start, end, nstep
        # 描画カーソル位置(px)
        self.cursor_current_px = (frame - start) / nstep

        # 間引き処理
        dreshape = np.asarray(self.buffer[start:end]).reshape((chunk_size, nstep))

        data_max = np.atleast_1d(np.max(dreshape, axis=1))
        data_min = np.atleast_1d(np.min(dreshape, axis=1))
        data = [-1 * d * amp + amp for d in data_max] + \
               [-1 * d * amp + amp for d in data_min[::-1]]
        # x axis
        time = range(chunk_size)
        time = list(time) + list(time[::-1])

        self.set_series(time, data)
        self.update()

    def paint_wave(self, painter):
        # paint series
        painter.setPen(self.series_line_colors[0])
        painter.setBrush(
            QBrush(self.series_line_colors[0], Qt.SolidPattern))
        painter.drawPolygon(QPolygonF(self.series))
        # cursor
        painter.setPen(self.cursor_current_color)
        painter.drawLine(self.cursor_current_px, 0, self.cursor_current_px, self.DefaultViewHeight)

    def paint(self, painter, option, widget):
        self.calc_fps()
        # paint to background
        painter.fillRect(self.bounding, self.item_bg_color)
        painter.fillRect(self.figure_bound, self.fig_bg_color)
        painter.setPen(self.border_color)
        painter.drawRect(self.figure_bound)
        # paint axis line
        painter.drawLine(0, self.DefaultViewHeight / 2,
                         self.DefaultViewWidth, self.DefaultViewHeight / 2)
        # paint wave
        self.paint_wave(painter)

    def set_series(self, t, pcm):
        qpoints = [QPointF(x, y) for x, y in zip(t, pcm)]
        self.series = qpoints

    def calc_fps(self):
        fps_newtime = time.clock()
        self.fps = 1.0 / (fps_newtime - self.fps_oldtime)  # [s]
        self.fps_oldtime = fps_newtime
        # print("FPS :{:0.1f}[fps]".format(self.fps))

    def boundingRect(self):
        return self.bounding

    def wheelEvent(self, event):
        delta = event.delta()
        if 0 < delta:
            if self.scale_minnum < self.scale_number:
                self.scale_number -= self.scale_delta
        else:
            if self.scale_number < self.scale_maxnum:
                self.scale_number += self.scale_delta

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.on_click(event.pos().x(), event.pos().y())


class WaveViewer(QGraphicsView):
    DefaultViewWidth = 512
    DefaultViewHeight = 30

    def __init__(self, *args, wavpath=None, **kw):
        super().__init__(*args, **kw)
        self.setFixedSize(QSize(self.DefaultViewWidth, self.DefaultViewHeight))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene(self)
        # self.scene.setBackgroundBrush(Qt.blue)
        self.scene.setSceneRect(
            0, 0, WaveViewer.DefaultViewWidth, WaveViewer.DefaultViewHeight)
        self.setScene(self.scene)

        self.waveviewer_item = WaveViewItem(wavpath)
        self.scene.addItem(self.waveviewer_item)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.TextAntialiasing
                            )


def testmain():
    app = QApplication(sys.argv)
    wave_figure = WaveViewer()
    wave_figure.show()
    app.exec_()


if __name__ == '__main__':
    testmain()
