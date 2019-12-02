# # -*- coding: utf-8 -*-

# # Form implementation generated from reading ui file 'C:\Users\Zoe\Desktop\cv\test.ui'
# #
# # Created by: PyQt5 UI code generator 5.13.0
# #
# # WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import sys
import os
import cv2
import dataset_pyqtgraph 
import numpy as np
from PyQt5.QtCore import Qt
class MainUI(object):
    def __init__(self, MainWindow, data_path):

        MainWindow.setWindowTitle('Tracking demo')
        MainWindow.resize(1000, 700)

        # data path 
        self.gt_path = data_path

        self.path = data_path
     
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

        self.score_box = self.graphicsWindow.addViewBox(0, 0, colspan=100)
        self.ref_box = self.graphicsWindow.addViewBox(0, 100, colspan=50)
        self.groundtruth_box = self.graphicsWindow.addViewBox(3,0, colspan=200)


        self.score_box.invertY(True)  # Images usually have their Y-axis pointing downward
        self.groundtruth_box.invertY(True)
        self.ref_box.invertY(True)

        self.score_box.setAspectLocked(True)
        self.groundtruth_box.setAspectLocked(True)
        self.ref_box.setAspectLocked(True)

        # image stuff 
        self.score_map = pg.ImageItem(axisOrder='row-major')
        self.groundtruth_img = pg.ImageItem(axisOrder='row-major')
        self.ref_img = pg.ImageItem(axisOrder='row-major')

        # Set Image placeholders
        self.score_map.setImage(np.zeros((300,230,3)))
        self.groundtruth_img.setImage(np.zeros((300,230,3)))
        self.ref_img.setImage(np.zeros((300,230,3)))

        self.score_box.addItem(self.score_map)
        self.groundtruth_box.addItem(self.groundtruth_img)
        self.ref_box.addItem(self.ref_img)

        # laybels 
        # Add the Labels to the images
        font = QtGui.QFont()
        font.setPointSize(4)

        # parameter for text display 
        param_dict = {'color':(255,255,255),
                      'anchor':(0,1)}
        label_score = pg.TextItem(text='Score Map', **param_dict)
        label_gt = pg.TextItem(text='Ground Truth', **param_dict)
        label_ref = pg.TextItem(text='Reference Image', **param_dict)
        font.setPointSize(16)
        label_score.setFont(font)
        label_gt.setFont(font)
        label_ref.setFont(font)
        label_score.setParentItem(self.score_map)
        label_gt.setParentItem(self.groundtruth_img)
        label_ref.setParentItem(self.ref_img)
        self.score_box.addItem(label_score)
        self.groundtruth_box.addItem(label_gt)
        self.ref_box.addItem(label_ref)


        # display buttons 
        self.display_Btn.clicked.connect(self.addImages)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)       

        self.i = 0

        self.updateTime = ptime.time()
        self.fps = 0

        MainWindow.show()

    def exit(self):
        sys.exit()

    def setDataset(self):
        if self.panda_radBtn.isChecked():
            self.img_disp_path = self.path["bolt1"]
        if self.tiger_radBtn.isChecked():
            self.img_disp_path  = self.path["bolt2"]

    def addImages(self, MainWindow):
        # self.gt_path = self.path
        self.data_set = self.load_data( )
        self.updateData()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Select Dataset"))
        self.panda_radBtn.setText(_translate("MainWindow", "Bolt"))
        self.tiger_radBtn.setText(_translate("MainWindow", "Plastic"))
        self.display_Btn.setText(_translate("MainWindow", "Display!"))
     
    def load_data(self):
        n_files = len(os.listdir(self.img_disp_path))
        image_set = []
        for i in range(1,n_files - 1):
        
            imagePath = os.path.join(self.img_disp_path+ "%08d.jpg"%i)
            frame = cv2.imread(imagePath) # 1 for colored imaged     
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_set.append(frame)
      
        return image_set

    def read_error(self, path):
        lineList = []
        filePath = os.path.join(self.img_disp_path + ".txt")
        with open(filePath, 'r') as file:
            for line in file :
                lines = [float(number) for number in line.strip().split()]
                lineList.append(lines)
        return lineList 

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

    app = QtWidgets.QApplication(sys.argv)

    win = QtWidgets.QMainWindow()
    path = {"bolt1" : './bolt2_kcf/bolt2/', "bolt2":'./bolt2_kcf/bolt2/', 
            "football":'./bolt2_kcf/bolt2/', "football1":'./bolt2_kcf/bolt2/', 
            "mountainbike":'./bolt2_kcf/bolt2/'}


    ui = MainUI(win, path)

    win.show()
    sys.exit(app.exec_())
