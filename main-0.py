import sys
import os.path
from random import randrange
from math import sin, cos
from PyQt5.QtCore import Qt, QPointF, QRect, QPoint, QObject, pyqtSignal, pyqtSlot, QBasicTimer
from PyQt5.QtGui import QPainter, QPixmap, QColor, QMouseEvent, QPolygon, QPen, QBrush
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox, QListWidgetItem
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# import pyqtgraph as pg
# from pyqtgraph import PlotWidget, plot
# import matplotlib.pyplot as plt

# from delay.equation import DifferentialEquationSystem
# from ui.ui import *
from tusa2 import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_func_name = []
        self.init_funcs = []
        self.init_funcs_colors = []
        self.L = 0
        self.d = 0
        self.T = 0
        self.h = 0.001
        self.end_time = 100

        self.ui.graphicsView.setBackground(background=(255, 255, 255))
        self.ui.graphicsView.setRange(xRange=(0, 10), yRange=(0, 10))

        self._init_setup()

    def _init_setup(self):
        self.ui.pb_add_init_func.clicked.connect(self._add_init_func)
        self.ui.pb_del_init_func.clicked.connect(self._del_init_func)
        self.ui.pb_draw.clicked.connect(self.draw)
        self.ui.pb_draw_matplotlib.clicked.connect(self.draw_matplotlib)
        # -----------------/L/-----------------
        self.ui.le_param_L_from.textChanged.connect(self._change_range_L)
        self.ui.le_param_L_to.textChanged.connect(self._change_range_L)
        self.ui.hs_param_L_val.valueChanged.connect(self._set_value_L)
        # -----------------/d/-----------------
        self.ui.le_param_d_from.textChanged.connect(self._change_range_d)
        self.ui.le_param_d_to.textChanged.connect(self._change_range_d)
        self.ui.hs_param_d_val.valueChanged.connect(self._set_value_d)
        # -----------------/T/-----------------
        self.ui.le_param_T_from.textChanged.connect(self._change_range_T)
        self.ui.le_param_T_to.textChanged.connect(self._change_range_T)
        self.ui.hs_param_T_val.valueChanged.connect(self._set_value_T)
        # -----------------//-----------------
        self.ui.le_set_L.textChanged.connect(lambda: setattr(self, 'L', float(self.ui.le_set_L.text().strip().replace(',', '.') or 0)))
        self.ui.le_set_d.textChanged.connect(lambda: setattr(self, 'd', float(self.ui.le_set_d.text().strip().replace(',', '.') or 0)))
        self.ui.le_set_T.textChanged.connect(lambda: setattr(self, 'T', float(self.ui.le_set_T.text().strip().replace(',', '.') or 0)))
        self.ui.le_set_end_time.textChanged.connect(lambda: setattr(self, 'end_time', float(self.ui.le_set_end_time.text() or 0)))
        # -----------------//-----------------
        self.ui.le_set_L.setVisible(False)
        self.ui.le_set_d.setVisible(False)
        self.ui.le_set_T.setVisible(False)
        self.ui.le_set_end_time.setVisible(False)
        self.ui.le_param_h.setVisible(False)
        # -----------------//-----------------
        self.ui.hs_param_k_val.valueChanged.connect(self._set_value_k)

    def _del_init_func(self):
        try:
            idx = self.ui.input_area.selectedIndexes()[0].row()
            del self.init_funcs[idx]
            del self.init_funcs_colors[idx]
            self.ui.input_area.takeItem(idx)
        except Exception as ex:
            print(str(ex))
            QMessageBox.critical(self, 'Ошибка', 'Не удалось удалить элемент!')
        count = self.ui.input_area.count() - 1
        self.ui.le_param_k_to.setText(str(count))
        self.ui.hs_param_k_val.setRange(0, count)

    def _set_value_k(self, val):
        self.k = val
        self.ui.lbl_cur_val_k.setText('Текущее значение параметра k: ' + str(self.k))

    def _set_value_L(self, val):
        self.L = val
        self.ui.lbl_cur_val_L.setText('Текущее значение параметра L: ' + str(self.L))

    def _set_value_d(self, val):
        self.d = val / 100
        self.ui.lbl_cur_val_d.setText('Текущее значение параметра d: ' + str(self.d))

    def _set_value_T(self, val):
        self.T = val
        self.ui.lbl_cur_val_T.setText('Текущее значение параметра T: ' + str(self.T))

    def _change_range_L(self):
        try:
            val_from = float(self.ui.le_param_L_from.text().strip() or 0)
        except Exception:
            val_from = 0
        try:
            val_to = float(self.ui.le_param_L_to.text().strip() or 0)
        except Exception:
            val_to = 100
        self.ui.hs_param_L_val.setRange(val_from, val_to)

    def _change_range_d(self):
        try:
            val_from = float(self.ui.le_param_d_from.text().strip() or 0)
        except Exception:
            val_from = 0
        try:
            val_to = float(self.ui.le_param_d_to.text().strip() or 0)
        except Exception:
            val_to = 100
        self.ui.hs_param_d_val.setRange(val_from, val_to)

    def _change_range_T(self):
        try:
            val_from = float(self.ui.le_param_T_from.text().strip() or 0)
        except Exception:
            val_from = 0
        try:
            val_to = float(self.ui.le_param_T_to.text().strip() or 0)
        except Exception:
            val_from = 10
        self.ui.hs_param_T_val.setRange(val_from, val_to)

    def _add_init_func(self):
        func_text = self.ui.le_input_init_func.text().replace('^', '**').replace(',', '.')
        try:
            # проверим и создадим функцию
            func_call = eval('lambda t:' + func_text)
            func_call(1)
            # создадим цвет
            color = (
                (256 - randrange(256)) % 256,
                randrange(256),
                (256 + randrange(256)) % 256
            )
            # для каждой функции будет ее цвет
            self.init_funcs.append(func_call)
            self.init_funcs_colors.append(color)
            self.init_func_name.append(func_text)
            item = QListWidgetItem('f(t) = ' + func_text.strip())
            item.setBackground(QBrush(QColor(*color)))
            self.ui.input_area.addItem(item)
        except Exception as ex:
            QMessageBox.warning(self, 'Ошибка ввода', 'Некоректная функция')
            print(str(ex))
        self.ui.le_input_init_func.setText('')
        count = self.ui.input_area.count() - 1  # -1 так как свзяй на 1 меньше чем ур-ий
        self.ui.le_param_k_to.setText(str(count))
        self.ui.hs_param_k_val.setRange(0, count)

    def draw(self):
        if not self.init_funcs:
            QMessageBox.warning(self, 'Ошибка данных', 'Не указано ни одной начальной функции!')
            return
        if self.T <= 0:
            QMessageBox.warning(self, 'Ошибка данных', 'Не указано время запаздывания!')
            return
        h = self.ui.sb_h.value()
        end_time = self.ui.sb_t.value()
        k = self.ui.hs_param_k_val.value()
        n = self.ui.sp_n.value()
        self.ui.progress_bar.setValue(0)
        ds = DifferentialEquationSystem(self.init_funcs, h, self.T, self.L, self.d, k, n)
        for state in ds.solve_yield(end_time):
            self.ui.progress_bar.setValue(state * 90)
        self.ui.graphicsView.clear()
        self.plot = ds.get_data()
        for i, plot in enumerate(self.plot):
            self.ui.graphicsView.plot(plot[0], plot[1], pen=self.init_funcs_colors[i])
        self.ui.progress_bar.setValue(100)
        if ds.sync():
            self.ui.lbl_status.setText('Синхронизация произошла')
            self.ui.lbl_status.setStyleSheet('background-color: green')
        else:
            self.ui.lbl_status.setText('Синхронизация не произошла')
            self.ui.lbl_status.setStyleSheet('background-color: red')

    def draw_matplotlib(self):
        if not getattr(self, 'plot', None):
            QMessageBox.critical(self, 'Ошибка', 'Ур-ия не были решены!')
            return
        plt.xlabel('t')
        plt.ylabel('$x_i(t)$')
        for i, plot in enumerate(self.plot):
            plt.plot(plot[0], plot[1], label=f'$x_{i + 1}(t)$')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
