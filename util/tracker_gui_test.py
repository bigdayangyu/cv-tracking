# # -*- coding: utf-8 -*-

# # Form implementation generated from reading ui file 'C:\Users\Zoe\Desktop\cv\test.ui'
# #
# # Created by: PyQt5 UI code generator 5.13.0
# #
# # WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import sys
import os
import cv2
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


class MainUI(object):
    def __init__(self, MainWindow, data_path):
        MainWindow.setWindowTitle('Tracking demo')
        MainWindow.resize(1000, 900)

        self.gt_path = data_path
        self.data_set = self.load_data(data_path)


        # Define the ViewBoxes for each of the images to be displayed
        self.score_box = MainWindow.addViewBox(1, 0, colspan=3)
        self.groundtruth_box = MainWindow.addViewBox(3, 0, colspan=2)
        self.ref_box = MainWindow.addViewBox(3, 2)

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

        self.score_box.addItem(self.score_map)
        self.groundtruth_box.addItem(self.groundtruth_img)
        self.ref_box.addItem(self.ref_img)

        # bounding box 
        self.bbox = QtWidgets.QGraphicsRectItem()
        self.bbox.setPen(QtGui.QColor(255, 0, 0))
        self.bbox.setParentItem(self.groundtruth_img)
        self.groundtruth_box.addItem(self.bbox)
        
        # add heat map to score 
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        self.peak = pg.GraphItem(size=30, symbol='+', pxMode=True,
                                 symbolBrush=brush,
                                 symbolPen=None)
        self.peak.setParentItem(self.score_map)
        self.score_box.addItem(self.peak)

        # prior 
        self.peak_pos = None
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, alpha=0))
        self.prior_radius = pg.GraphItem(size=0, symbol='o', pxMode=True,
                                         symbolBrush=brush, symbolPen='b')
        self.prior_radius.setParentItem(self.score_map)
        self.score_box.addItem(self.prior_radius)

        # laybels 
        # Add the Labels to the images
        font = QtGui.QFont()
        font.setPointSize(4)
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

        self.i = 0

        self.updateTime = ptime.time()
        self.fps = 0

        MainWindow.show()

    def exit(self):
        sys.exit()
     
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

    # app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    # ui = Ui_Dialog()
    # ui.setupUi(Dialog)
    # Dialog.show()
    # sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    win = pg.GraphicsLayoutWidget(border=True)
    path = './Biker/Biker/img/'
    ui = MainUI(win,path)
    
    # data = load_data(path)
   
    ui.updateData()
    win.show()
    sys.exit(app.exec_())



