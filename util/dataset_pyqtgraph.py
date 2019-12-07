# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\epyan\Documents\JHU\03-Fall 2019\601.661 Computer Vision\Project\dataset_pyqtgraph.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import sys
import os
import cv2
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(800, 550)
        MainWindow.resize(1000, 700)

        # Dataset Selection
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 120, 100))
        self.groupBox.setObjectName("groupBox")

        self.panda_radBtn = QtWidgets.QRadioButton(self.groupBox)
        self.panda_radBtn.setGeometry(QtCore.QRect(10, 20, 95, 20))
        self.panda_radBtn.setObjectName("panda_radBtn")
        self.panda_radBtn.toggled.connect(self.setDataset)

        self.tiger_radBtn = QtWidgets.QRadioButton(self.groupBox)
        self.tiger_radBtn.setGeometry(QtCore.QRect(10, 40, 95, 20))
        self.tiger_radBtn.setObjectName("tiger_radBtn")
        self.tiger_radBtn.toggled.connect(self.setDataset)

        self.display_Btn = QtWidgets.QPushButton(self.groupBox)
        self.display_Btn.setGeometry(QtCore.QRect(15, 65, 93, 28))
        self.display_Btn.setObjectName("display_Btn")

        # Set up GraphicsLayoutWidget for images
        self.graphicsWindow = GraphicsLayoutWidget(self.centralwidget, border=True)
        self.graphicsWindow.setGeometry(QtCore.QRect(140, 10, 850, 600))
        self.graphicsWindow.setObjectName("graphicsWindow")
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        # Define the Viewboxes for each of the images to be displayed
        self.score_box = self.graphicsWindow.addViewBox(0, 0, colspan=100)
        self.ref_box = self.graphicsWindow.addViewBox(0, 100, colspan=50)
        self.results_box = self.graphicsWindow.addViewBox(3,0, colspan=200)

        self.score_box.invertY(True)
        self.results_box.invertY(True)
        self.ref_box.invertY(True)

        self.score_box.setAspectLocked(True)
        self.results_box.setAspectLocked(True)
        self.ref_box.setAspectLocked(True)

        # Add ImageItems to the ViewBoxes
        self.score_map = pg.ImageItem(axisOrder='row-major')
        self.groundtruth_img = pg.ImageItem(axisOrder='row-major')
        self.ref_img = pg.ImageItem(axisOrder='row-major')

        self.score_box.addItem(self.score_map)
        self.results_box.addItem(self.groundtruth_img)
        self.ref_box.addItem(self.ref_img)

        # Set Image placeholders
        self.score_map.setImage(np.zeros((300,230,3)))
        self.groundtruth_img.setImage(np.zeros((300,230,3)))
        self.ref_img.setImage(np.zeros((300,230,3)))

        # Add the Labels to the images
        font = QtGui.QFont()
        font.setPointSize(4)
        param_dict = {'color':(255,255,255),
                      'anchor':(0,1)}
        label_score = pg.TextItem(text='Score Map', **param_dict)
        label_gt = pg.TextItem(text='Ground Truth', **param_dict)
        label_ref = pg.TextItem(text='Reference Image', **param_dict)
        font.setPointSize(12)
        label_score.setFont(font)
        label_gt.setFont(font)
        label_ref.setFont(font)
        label_score.setParentItem(self.score_map)
        label_gt.setParentItem(self.groundtruth_img)
        label_ref.setParentItem(self.ref_img)
        self.score_box.addItem(label_score)
        self.results_box.addItem(label_gt)
        self.ref_box.addItem(label_ref)

        self.display_Btn.clicked.connect(self.addImages)

        self.i = 0

        self.updateTime = ptime.time()
        self.fps = 0

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.show()

    def setDataset(self):
        if self.panda_radBtn.isChecked():
            self.path = './data/Panda/img/'
        if self.tiger_radBtn.isChecked():
            self.path = './data/Tiger2/img/'

    def addImages(self, MainWindow):
        # self.gt_path = self.path
        self.data_set = self.load_data(self.path)
        self.updateData()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Select Dataset"))
        self.panda_radBtn.setText(_translate("MainWindow", "Panda"))
        self.tiger_radBtn.setText(_translate("MainWindow", "Tiger"))
        self.display_Btn.setText(_translate("MainWindow", "Display!"))

    def load_data(self, path):
        n_files = len(os.listdir(path))
        image_set = []
        for i in range(2,n_files):
        
            imagePath = os.path.join(path+ "%04d.jpg"%i)

            frame = cv2.imread(imagePath)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_set.append(frame)

        return image_set

    def updateData(self):
        self.score_map.setImage(self.data_set[self.i])
        self.groundtruth_img.setImage(self.data_set[self.i])
        self.ref_img.setImage(self.data_set[self.i])

        self.i = (self.i + 1) % len(self.data_set)
       
        QtCore.QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        fps2 = 1.0/(now - self.updateTime)
        self.updateTime = now 
        self.fps = self.fps*0.9 + fps2*0.1



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # ui.updateData()
    MainWindow.show()
    sys.exit(app.exec_())
