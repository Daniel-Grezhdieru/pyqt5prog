import os.path
import sys
# import math
import cmath
# import scipy.integrate as I
import numpy as np
# from numpy import linalg as LA
import matplotlib.pyplot as plt
# from matplotlib import mlab
# from scipy.optimize import fsolve
from mpmath import findroot
from sympy import Float
#PyQT
from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtCore import Qt, QPointF, QRect, QPoint, QObject, pyqtSignal, pyqtSlot, QBasicTimer
# from PyQt5.QtGui import QPainter, QPixmap, QColor, QMouseEvent, QPolygon, QPen, QBrush
from PyQt5.QtWidgets import QMessageBox

# QtDesigner
from form import *

# from ui.ui import *
# ui_path = os.path.dirname(os.path.abspath("C:/Users/grejd/Desktop/pyqt5prog/form.ui"))
# Form, Window = uic.loadUiType(os.path.join(ui_path, "form.ui"))


# app = QtWidgets.QApplication([])
# window = Window()
# form = Form()
# form.setupUi(window)
# window.show()
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
form = Ui_MainWindow()
form.setupUi(window)
window.show()

def on_click1():
    form.textEdit.setText("")
    func_text = form.lineEdit.text().replace('u^', 'u**').replace('e^(','cmath.exp(').replace(',', '.')
    # print(func_text)
    try:
            # проверим и создадим функцию
            func_call = eval('lambda u:' + func_text)
            func_call(1)
    except Exception as ex:
            QMessageBox.warning(window,'Ошибка ввода', 'Некоректная функция')
            print(str(ex))
    # form.lineEdit.setText('')

    n = form.spinBox.value()*10 #2000 200
    x = np.ndarray(form.spinBox.value()*10, dtype=np.complex128)
    roots = []
    # r_real = []
    # r_imag = []
    for i in range(1,n):
        x[i] = complex(0,i*0.1) #0.01 0.1

    for i in x:
        try:
            a = findroot(func_call, i, solver='muller')
            roots.append(complex(Float(a.real,5),Float(a.imag,5)))
            # r_real.append(Float(a.real,5))
            # r_imag.append(Float(a.imag,5))
        except: 
            pass

    roots = set(roots)

    text = " "
    for L in roots:
        s = str(L) + "\n \n"
        text += s

    form.textEdit.setText(text)

def on_click2():
    # form.textEdit.setText("")
    func_text = form.lineEdit.text().replace('u^', 'u**').replace('e^(','cmath.exp(').replace(',', '.')
    # print(func_text)
    try:
        # проверим и создадим функцию
        func_call = eval('lambda u:' + func_text)
        func_call(1)
    except Exception as ex:
        QMessageBox.warning(window,'Ошибка ввода', 'Некоректная функция')
        print(str(ex))
        return
    

    n = form.spinBox.value()*10 #2000 200
    x = np.ndarray(form.spinBox.value()*10, dtype=np.complex128)
    # roots = []
    r_real = []
    r_imag = []
    for i in range(1,n):
        x[i] = complex(0,i*0.1) #0.01 0.1

    for i in x:
        try:
            a = findroot(func_call, i, solver='muller')
            # roots.append(complex(Float(a.real,5),Float(a.imag,5)))
            r_real.append(Float(a.real,5))
            r_imag.append(Float(a.imag,5))
        except: 
            pass
    plt.xlabel("real")
    plt.ylabel("imag")
    plt.plot(r_real,r_imag,".")
    plt.grid()   
    plt.show()




form.pushButton1.clicked.connect(on_click1)
form.pushButton.clicked.connect(on_click2)
sys.exit(app.exec_())
