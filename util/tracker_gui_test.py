# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Zoe\Desktop\cv\test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import GraphicsLayoutWidget
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import time
import sys
import os

class MainUI(object):
    def __init__(self, MainWindow, data_path):

        MainWindow.setWindowTitle('Tracking demo')
        MainWindow.resize(1050, 690)
        # data path 
        self.gt_path = data_path
        self.path = data_path
     
        # Dataset Selection
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 150, 200))
        self.groupBox.setObjectName("groupBox")

        self.groupBox_legend = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_legend.setGeometry(QtCore.QRect(10, 220, 150, 70))
        self.groupBox_legend.setObjectName("groupBox_legend")
         
        # self.legend_label = QtWidgets.QLabel()
        self.legend_label = QtWidgets.QLabel(self.groupBox_legend)
        self.legend_label.setGeometry(QtCore.QRect(10, 10, 150, 50))
        self.legend_label.setText("Ground Truth")
        self.legend_label.setStyleSheet(" color: rgba(255, 0, 0, 1); font-size: 10pt; font-weight: 300;")
        
        self.legend_label2 = QtWidgets.QLabel(self.groupBox_legend)
        self.legend_label2.setGeometry(QtCore.QRect(10, 30, 150, 50))
        self.legend_label2.setText("Tracking Result")
        self.legend_label2.setStyleSheet(" color: rgba(0,255, 0, 1); font-size: 10pt; font-weight: 300;")

        self.radBtn_1 = QtWidgets.QRadioButton(self.groupBox)
        self.radBtn_1.setGeometry(QtCore.QRect(10, 20, 95, 20))
        self.radBtn_1.setObjectName("panda_radBtn")
        self.radBtn_1.toggled.connect(self.setDataset)

        self.radBtn_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radBtn_2.setGeometry(QtCore.QRect(10, 40, 95, 20))
        self.radBtn_2.setObjectName("tiger_radBtn")
        self.radBtn_2.toggled.connect(self.setDataset)

        self.radBtn_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radBtn_3.setGeometry(QtCore.QRect(10, 60, 95, 20))
        self.radBtn_3.setObjectName("panda_radBtn")
        self.radBtn_3.toggled.connect(self.setDataset)

        self.radBtn_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radBtn_4.setGeometry(QtCore.QRect(10, 80, 95, 20))
        self.radBtn_4.setObjectName("tiger_radBtn")
        self.radBtn_4.toggled.connect(self.setDataset)

        self.radBtn_5 = QtWidgets.QRadioButton(self.groupBox)
        self.radBtn_5.setGeometry(QtCore.QRect(10, 100, 95, 20))
        self.radBtn_5.setObjectName("panda_radBtn")
        self.radBtn_5.toggled.connect(self.setDataset)

        self.model_pulldown = QtGui.QComboBox(self.groupBox)
        self.model_pulldown.setGeometry(QtCore.QRect(15,125, 93, 28))
        self.model_pulldown.setObjectName("model_pulldown")
        # self.model_pulldown.addItem("Select")
        self.model_pulldown.addItem("KCF")
        self.model_pulldown.addItem("MDNet")
        self.model_pulldown.addItem("SiamFC")
        self.img_root = self.path["KCF"]
        self.model_pulldown.activated.connect(self.setModel)

        self.display_Btn = QtWidgets.QPushButton(self.groupBox)
        self.display_Btn.setGeometry(QtCore.QRect(15, 155, 93, 28))
        self.display_Btn.setObjectName("display_Btn")

        # Set up GraphicsLayoutWidget for images
        self.graphicsWindow = GraphicsLayoutWidget(self.centralwidget, border=True)
        self.graphicsWindow.setGeometry(QtCore.QRect(170, 10, 850, 600))
        self.graphicsWindow.setObjectName("graphicsWindow")
        MainWindow.setCentralWidget(self.centralwidget)

        self.score_box = self.graphicsWindow.addViewBox(0, 0, colspan=100)
        self.ref_box = self.graphicsWindow.addViewBox(0, 100, colspan=50)
      
        self.score_box.invertY(True)  # Images usually have their Y-axis pointing downward

        self.ref_box.invertY(True)

        self.score_box.setAspectLocked(True)
 
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

        self.ref_box.addItem(self.ref_img)

        # laybels 
        # Add the Labels to the images
        font = QtGui.QFont()
        font.setPointSize(4)

        # parameter for text display 
        param_dict = {'color':(255,255,255),
                      'anchor':(0,1)}
        label_score = pg.TextItem(text='Tracking Result', **param_dict)
        label_gt = pg.TextItem(text='Tracking Error', **param_dict)
        label_ref = pg.TextItem(text='Reference Image', **param_dict)

        font.setPointSize(16)
        label_score.setFont(font)
        label_gt.setFont(font)
        label_ref.setFont(font)
        label_score.setParentItem(self.score_map)
        label_gt.setParentItem(self.groundtruth_img)
        label_ref.setParentItem(self.ref_img)

        self.score_box.addItem(label_score)

        self.ref_box.addItem(label_ref)

        # display buttons 
        self.display_Btn.clicked.connect(self.addImages)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)       

        self.i = 0
        self.error =np.zeros((1))

        self.updateTime = ptime.time()
        self.fps = 0

        # display error plot 
        self.error_plot = self.graphicsWindow.addPlot(3,0, colspan=200,
            title='Center to Center Distance (Pixels)')
        self.error_data = np.zeros((3, ))
        self.curve1 = self.error_plot.plot(self.error_data)

        MainWindow.show()

    def exit(self):
        sys.exit()

    def setDataset(self):
        if self.radBtn_1.isChecked():
            self.img_disp_path = "bolt1/"
            self.template_path = "bolt.jpg"
            self.temp_img =  self.load_temp()
            self.error_plot.removeItem(self.curve1) 
            self.error_data = self.read_error()

        if self.radBtn_2.isChecked():
            self.img_disp_path  = "bolt2/"
            self.template_path = "bolt2.jpg"
            self.temp_img =  self.load_temp()

            self.error_plot.removeItem(self.curve1) 
            self.error_data = self.read_error()  

        if self.radBtn_3.isChecked():
            self.img_disp_path = "football/"
            self.template_path = "football.jpg"
            self.temp_img =  self.load_temp()
            self.error_plot.removeItem(self.curve1) 
            self.error_data = self.read_error()

        if self.radBtn_4.isChecked():
            self.img_disp_path  = "football1/"
            self.template_path = "football1.jpg"
            self.temp_img =  self.load_temp()
            self.error_plot.removeItem(self.curve1) 
            self.error_data = self.read_error()   

        if self.radBtn_5.isChecked():
            self.img_disp_path  = "mountainbike/"
            self.template_path = "mountainbike.jpg"
            self.temp_img =  self.load_temp()
            self.error_plot.removeItem(self.curve1) 
            self.error_data = self.read_error()   

    def setModel(self):
        if self.model_pulldown.currentText() == "KCF":
            self.error_plot.removeItem(self.curve1) 
            self.img_root = self.path["KCF"]
       
        if self.model_pulldown.currentText() == "MDNet":
            self.error_plot.removeItem(self.curve1) 
            self.img_root = self.path["MDNet"]

        if self.model_pulldown.currentText() == "SiamFC":
            self.error_plot.removeItem(self.curve1) 
            self.img_root = self.path["SiamFC"]

    def addImages(self, MainWindow):

        self.i = 0

        self.data_set = self.load_data()
        self.error =np.zeros((1))
        self.curve1 = self.error_plot.plot(np.zeros((1, ))) 
        self.error_plot.removeItem(self.curve1) 
        self.curve1 = self.error_plot.plot(np.zeros((1, ))) 

        self.updateData()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Select Dataset"))
        self.groupBox_legend.setTitle(_translate("MainWindow", "Legend"))

        self.radBtn_1.setText(_translate("MainWindow", "Bolt1"))
        self.radBtn_2.setText(_translate("MainWindow", "Bolt2"))
        self.radBtn_3.setText(_translate("MainWindow", "football"))
        self.radBtn_4.setText(_translate("MainWindow", "football1"))
        self.radBtn_5.setText(_translate("MainWindow", "mountbike"))

        self.display_Btn.setText(_translate("MainWindow", "Display!"))
     
    def load_temp(self):
        imagePath = os.path.join(self.img_root + self.template_path )
   
        temp = cv2.imread(imagePath)
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)

        return temp

    def load_data(self):
        n_files = len(os.listdir(self.img_root + self.img_disp_path)) - 3
        image_set = []
        for i in range(1, n_files):
        
            imagePath = os.path.join(self.img_root + self.img_disp_path + "%08d.jpg"%i)
          
            frame = cv2.imread(imagePath) # 1 for colored imaged     
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_set.append(frame)
      
        return image_set

    def read_error(self):
        lineList = []

        filePath = os.path.join(self.img_root + self.img_disp_path + "error.txt")
        with open(filePath, 'r') as file:
            for line in file :
                lines = [float(number) for number in line.strip().split()]
                lineList.append(lines[0])
        return np.array(lineList) 

    def updateData(self):
        self.score_map.setImage(self.data_set[self.i])
        self.ref_img.setImage(self.temp_img)
        self.i = (self.i + 1) % len(self.data_set)
        now = ptime.time()

        fps2 = 1.0/(now - self.updateTime)
        self.updateTime = now 
        self.fps = self.fps*0.9 + fps2*0.1
        time.sleep(0.01)
        QtCore.QTimer.singleShot(100, self.updateData)

        self.curve1.setData(self.error_data[0:self.i])
# 
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()

    path = {"KCF": './datasets/gui_dataset_kcf/', 
            "MDNet": './datasets/gui_dataset_mdnet/', 
            "SiamFC": './datasets/gui_dataset_siamfc/'}

    ui = MainUI(win, path)
    win.show()
    sys.exit(app.exec_())
