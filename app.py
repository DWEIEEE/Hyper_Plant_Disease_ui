import os
import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from GUI import Ui_MainWindow
import qtawesome as qta
from tool import MBox, img2pyqt, drawBox, numpy2pyqt
import scipy.io
import numpy as np
import h5py as h5
from Segment import Segmentation
from treeview import TreeView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Application")
        self.setIcon()

        ### Setting ###
        ########################
        self.default_band = 22
        self.default_img_width = [17, 387]
        self.leaf_seg_size = 300
        self.seg_threshold = 40
        self.img_size = 224
        ########################
        self.seg = Segmentation(self.leaf_seg_size, self.seg_threshold, self.img_size)
        self.tree = TreeView(self.ui.treeView)

        self.ui.pushButton_3.clicked.connect(self.add_folder)
        self.ui.pushButton_2.clicked.connect(self.cancel)
        self.ui.pushButton_4.clicked.connect(self.left)
        self.ui.pushButton_5.clicked.connect(self.right)
        self.ui.comboBox.activated.connect(self.bandChange)

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.addButton(self.ui.checkBox)
        self.button_group.addButton(self.ui.checkBox_2)
        self.button_group.setExclusive(True)
        self.ui.checkBox.setChecked(True)

        self.button_group_2 = QtWidgets.QButtonGroup(self)
        self.button_group_2.addButton(self.ui.checkBox_3)
        self.button_group_2.addButton(self.ui.checkBox_4)
        self.button_group_2.setExclusive(True)
        self.ui.checkBox_3.setChecked(True)

        self.button_group_3 = QtWidgets.QButtonGroup(self)
        self.button_group_3.addButton(self.ui.checkBox_5)
        self.button_group_3.addButton(self.ui.checkBox_6)
        self.button_group_3.setExclusive(True)
        self.ui.checkBox_5.setChecked(True)

        self.ui.pushButton_6.setStyleSheet(f"""
        QPushButton {{
            background-color: green;
            border-radius: 3px;
        }}
        """)

    def bandChange(self):
        self.bandNum = int(self.ui.comboBox.currentText())
        self.setSec()

    def left(self):
        try:
            if self.inNum == 1:
                return
            self.inNum -= 1
            self.setSec()
        except:
            pass

    def right(self):
        try:
            if self.inNum == self.file_count:
                return
            self.inNum += 1
            self.setSec()
        except:
            pass

    def cancel(self):
        print("Application Exit ...")
        sys.exit()

    def add_folder(self):
        self.checkin = False
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if self.folder_path == "":
            return
        self.ui.lineEdit.setText(self.folder_path)
        self.checkfolder()

    def checkfolder(self):
        notice = False
        self.filenames = os.listdir(self.folder_path)
        self.file_count = len(self.filenames)
        if self.file_count == 0:
            MBox('No .mat files found in the folder.',3)
            return
        for index, file in enumerate(self.filenames):
            _, extension = os.path.splitext(file)
            extension = extension.lower()
            if extension != ".mat":
                self.file_count -= 1
                del self.filenames[index]
                notice = True
        if self.file_count == 0:
            MBox('No .mat files found in the folder.',3)
            return
        if notice == True:
            MBox('Notice, Only .mat files supported in folder,\nNon-.mat files filtered out from the folder',1)
        self.checkin = True
        self.inNum = 1
        self.bandNum = self.default_band
        self.setSec()

    def setSec(self):
        self.ui.label_5.setText(f"( {self.inNum} / {self.file_count} )")
        self.ui.label_4.setText(f"{self.filenames[self.inNum-1]}")
        self.load_file()

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems([str(x) for x in range(1, (self.band+1))])
        self.ui.comboBox.setCurrentIndex(self.bandNum-1)

        self.ui.comboBox.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_5.setEnabled(True)
        self.ui.pushButton_6.setEnabled(True)

    def load_file(self):
        self.tree.clear()
        try:
            temp = scipy.io.loadmat(os.path.join(self.folder_path,self.filenames[self.inNum-1]))
            #print("use Scipy success")
        except:
            temp = h5.File(os.path.join(self.folder_path,self.filenames[self.inNum-1]),'r')
            self.img = np.array(temp[list(temp.keys())[0]])
            #print("use h5 success")
        self.img = np.array(temp["cube"])
        self.img = np.transpose(self.img, (2, 1, 0))
        self.img = self.img[:, self.default_img_width[0]:self.default_img_width[1], :]
        self.band = self.img.shape[2]
        #### self.stack_image_list shape : (n, 224, 224, 24)
        self.area_list, self.stack_image_list = self.seg.process(self.img)
        box_img = drawBox(self.img[:, :, self.bandNum-1], self.area_list)
        self.ui.label.setPixmap(img2pyqt(box_img, self.ui.label))
        self.ui.label_16.setText("Found : {:2d} pcs".format(len(self.area_list)))
        for idx, (index, x, y, w, h, area) in enumerate(self.area_list):
            temp = self.stack_image_list[idx]
            self.tree.add(numpy2pyqt(temp[:,:,(self.default_band-1)]), str(idx+1), f'{str(area)} pixel', '-')

    def setIcon(self):
        folder_icon = qta.icon('mdi.folder-outline', color='black')
        left_icon = qta.icon('mdi.arrow-left-thick', color='black')
        right_icon = qta.icon('mdi.arrow-right-thick', color='black')

        self.ui.pushButton_3.setIcon(QtGui.QIcon(folder_icon))
        self.ui.pushButton_3.setIconSize(QtCore.QSize(25,25))
        self.ui.pushButton_4.setIcon(QtGui.QIcon(left_icon))
        self.ui.pushButton_4.setIconSize(QtCore.QSize(25,25))
        self.ui.pushButton_5.setIcon(QtGui.QIcon(right_icon))
        self.ui.pushButton_5.setIconSize(QtCore.QSize(25,25))

        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)

        self.ui.comboBox.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())