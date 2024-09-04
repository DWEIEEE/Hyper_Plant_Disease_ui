from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def MBox(txt,mode=None):
    msg = QtWidgets.QMessageBox()
    if mode == 1:
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Hint")
    elif mode == 2:
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Warning")
    elif mode == 3:
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Warning")
    elif mode == 4:
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Hint")
    msg.move(880,500)
    msg.setText(txt)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec_()

'''
def img2pyqt(frame,label, noise_filter):
    temp = np.expand_dims(frame, axis=2)
    temp = np.repeat(temp, 3, axis=2)
    height, width, _ = temp.shape
    img = QtGui.QImage(width, height, QtGui.QImage.Format_RGB888)

    painter = QtGui.QPainter(img)
    for y in range(height):
        for x in range(width):
            if temp[y, x, 0] < noise_filter:
                value = 0
            else:
                value = int(temp[y, x, 0] * 255)
            #print(f"{y}, {x} :{temp[y, x, 0]}")
            color = QtGui.QColor(value, value, value)
            painter.setPen(color)
            painter.drawPoint(x, y)
    painter.end()
    return QtGui.QPixmap.fromImage(img).scaled(label.width(), label.height())
'''

def img2pyqt(frame,label):
    temp = frame.copy()
    temp = QtGui.QImage(temp, temp.shape[1], temp.shape[0], temp.shape[1]*3, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(temp).scaled(label.width(), label.height())

def numpy2pyqt(frame):
    temp = frame.copy()
    frame = frame * 256
    frame = np.round(frame).astype('uint8')
    temp = np.expand_dims(frame, axis=2)
    temp = np.repeat(temp, 3, axis=2)
    temp = QtGui.QImage(temp, temp.shape[1], temp.shape[0], temp.shape[1]*3, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(temp).scaled(80, 80)

def drawBox(img, area_list, padding=0.06):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    plt.xticks(fontsize=9, fontweight='bold')
    plt.yticks(fontsize=9, fontweight='bold')
    for index, (_, x, y, w, h, area) in enumerate(area_list):
        rectangle = plt.Rectangle((x, y), w, h, edgecolor='g', facecolor='none', linewidth=2)
        ax.add_patch(rectangle)
        text_rect = plt.Rectangle((x, y), 18, 18, edgecolor=None, facecolor='g', alpha=0.6)
        ax.add_patch(text_rect)
        ax.text(x+5, y+14, f'{index+1}', color='w', fontsize=12, fontweight='bold')
    plt.subplots_adjust(left=padding, right=1-padding, top=1-padding, bottom=padding)
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
    plt.close(fig)
    return image

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, color="black", Alignment=QtCore.Qt.AlignmentFlag.AlignLeft, transparent=False):
        super().__init__()
        self.transparent = transparent
        self.setWordWrap(True)
        self.setAlignment(Alignment)
        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=600))
        self.set_color(color)
        self.setText(content)

    def set_color(self, color):
        if self.transparent:
            if color == 'red':
                self.setStyleSheet("color: red; background-color: rgba(50,50,50,50);")
            elif color == 'green':
                self.setStyleSheet(f"color: green; background-color: rgba(50,50,50,50);")
            elif color == 'white':
                self.setStyleSheet(f"color: white; background-color: rgba(50,50,50,50);")
            else:
                self.setStyleSheet("color: black; background-color: rgba(50,50,50,50);")
        else:
            if color == 'red':
                self.setStyleSheet("color: red;")
            elif color == 'green':
                self.setStyleSheet(f"color: #00FF00;")
            elif color == 'white':
                self.setStyleSheet(f"color: white;")
            else:
                self.setStyleSheet("color: black;")