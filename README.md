# cv-tracking 

## Introduction 
Our team set out to implement, compare, and contrast traditional computer vision (CV) and deep learning (DL) algorithms for single object tracking, specifically with the aim of helping us casual, yet clueless sports spectators to better understand what is going on during a game by tracking a particular player on the field or court. 

## Methods
### Models
The Kernelized Correlation Filter (KCF) is a traditional CV algorithm introduced in 2014, and Multi-domain Convolutional Neural Networks (MDNet) and Fully Convolutional Siamese Networks (SiameseFC) are two DL-based approaches, introduced in 2015 and 2016, respectively.

### Datasets
Two datasets were used to assess the tracking algorithms. The first was the VOT16 benchmark, and the second was the OTB15 Visual Tracker Benchmark, specifically the TB-50 sequences. Both datasets contain test sequences exhibiting challenging aspects in visual tracking like occlusion, deformation, motion blur, etc. These datasets were chosen because they correspond to the approximate time when the algorithms were first introduced. 

### KCF Improvements
Based on the original paper [1], we wrote our own KCF tracker code in Python using normalized grayscale pixel values as the feature. We found several problems with this vanilla KCF and tried to improve KCF in three aspects. First, we want to make KCF adaptive to changing scales. Second, we added an object detection procedure to help relocate the target when KCF fails. Finally, we explored the capability of HOG as a feature descriptor based on the author’s code [4].

#### Multi-scale Sampling
The vanilla KCF uses a window with a fixed size. Therefore, it cannot adapt to targets with changing scales (i.e. when the target gets closer or further from the camera). We address this problem by using a multi-scale sampling scheme. In the detection step of the algorithm, sub-windows of different scales are tested by sampling a different sized window and then scaling it to match the original image size, and the option providing the highest response is set as the current scale of the target. To avoid unnecessarily frequent changes in scales, the scores of scaled patches are weighted. The overall performance of the scaled KCF on the entire VOT16 dataset is slightly worse than the unscaled one, but better results are observed for certain sequences. The overall performance is not necessarily better than the unscaled version, since for images without scaling effects, multi-scale sampling increases the instability in the detection and update of the tracker. We hypothesize that using a bounding box regression or a DL-based detector may help improve the overall performance in mean IoU on benchmark datasets.

<p align="center"><img src ="https://github.com/bigdayangyu/cv-tracking/blob/master/Image_result/kcf.gif" width =30% /></p>

#### Detection for Failure Recovery
One fatal disadvantage of KCF is that it cannot recover when it loses track of the target. KCF only samples a window around the previously tracked position, so the tracker fails if the target moves too far away. This can easily happen if the object is occluded for a period time, since the object has shifted too far from the previous tracked position after occlusion. KCF also easily fails when the object undergoes a significant movement between frames because the object is no longer observable in a nearby window. For example, when some frames are purposely removed in the middle of a sequence, the target jumps to another position out of the detecting window, and KCF loses track and cannot recover.

We hypothesized that this problem could be solved by incorporating an additional detector, which can detect objects globally rather than in the surrounding window. In our algorithm, when the response score of KCF is lower than a threshold or suspiciously high, we assume that KCF has lost track of the object, and the detector is triggered. Selective search [7] is implemented to propose possible regions of objects. The regions are restricted given the posterior knowledge of the previous target position and size. Then normalized cross correlations of the proposed regions and the template are compared to find the target. For the purposes of this project, our implementation was relatively straightforward, and there exist more powerful and efficient trackers which perform very well in real-time object detection, for example, F-RCNNs [8] and YOLO [9]. Another benefit of using such a hybrid tracker is that we can also resize the bounding box when the object has greatly changed in its appearance.

<p align="center"><img src ="https://github.com/bigdayangyu/cv-tracking/blob/master/Image_result/kcf+detector.gif" width =30% /></p>

#### A Better Feature Representation - Histogram of Oriented Gradients (HOG)
In the original baseline and above implementations of KCF, raw pixels are used for detection and training. However, raw pixels used directly are not strong representations of features. A grayscale KCF very quickly loses track of Bolt and is unable to recover. A slightly higher level of representation like HOG, even though it is comparatively low level compared to those used in DL methods, results in much better performance. The HOG-based KCF implemented in the original code was run below for comparison with the grayscale KCF.

### Final Comparison
The hallmark of KCF is that it is computationally very fast, and it is the fastest tracker among the three methods. Its average frame rate is about 98 FPS on the VOT16 dataset. Using a Nvidia Geforce GTX 1050Ti GPU, the average frame rate of MDNet is 3 FPS and that of SiameseFC is 10 FPS. Although scaled KCF and the hybrid KCF are slightly slower than original KCF because additional steps are involved, they are still faster than SiameseFC and MDNet.

## Run the project
### Prerequisite 
* python 3.5.2
* selective-search
* numpy 
* openCV python 

### KCF trackers 
Run the KCF tracker:
```bash
python3 run.py img-dir save-dir
```
If enable scaling, 
```bash
python3 run.py img-dir save-dir --scaling True
```
### GUI
To demonstrate the relative performance of the different tracking algorithms on a few representative datasets from VOT16, we developed a GUI using pyqt5 that allows a user to select between 5 datasets and 3 trackers. Th GUI displays the video sequence with bounding boxes, as well as the starting reference image and a dynamic graph of the bounding box center-to-center pixel distance. 

<p align="center"><img src ="https://github.com/bigdayangyu/cv-tracking/blob/master/Image_result/gui.gif" width = 60% /></p> 
 
* download the dataset: [link](https://livejohnshopkins-my.sharepoint.com/:u:/g/personal/zli124_jh_edu/ERKmcKC83ndHgdyrawYXQN8B2L3od-0bfCaQOdQ2u6n9Aw?e=9eqMSI)

```bash
unzip datasets.zip
```

* Change the path for the video sequence 
```python
path = {"KCF": './datasets/gui_dataset_kcf/', 
        "MDNet": './datasets/gui_dataset_mdnet/', 
        "SiamFC": './datasets/gui_dataset_siamfc/'}
```

* And then run the tracker_gui.py file 

```bash
python /GUI/tracker_gui.py
```

## References
1.	J. F. Henriques, R. Caseiro, P. Martins, and J. Batista, “High-Speed Tracking with Kernelized Correlation Filters,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 37, no. 3, pp. 583–596, Mar. 2015.
2.	H. Nam and B. Han, “Learning Multi-domain Convolutional Neural Networks for Visual Tracking,” 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016. 
3.	L. Bertinetto, J. Valmadre, J. F. Henriques, A. Vedaldi, and P. H. S. Torr, “Fully-Convolutional Siamese Networks for Object Tracking,” European conference on computer vision, 2016.
4.	Kernelized Correlation Filters. [Online]. Available: http://www.robots.ox.ac.uk/~joao/circulant/
5.	H. Nam and B. Han, MDNet PyTorch Implementation, (2016), GitHub repository, https://github.com/hyeonseobnam/py-MDNet
6.	L. Bertinetto, J. Valmadre, SiamFC Tracking in TensorFlow, (2016), GitHub repository, https://github.com/torrvision/SiameseFC-tf
7.	J. R. R. Uijlings, K. E. A. van de Sande, T. Gevers, A. W. M. Smeulders, et al. "Selective search for object recognition." International journal of computer vision vol. 104, no. 2, pp. 154-171, 2013.
8.	S. Ren, K. He, R. Girshick, J. Sun, “Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks”. Advances in neural information processing systems. 2015.
9.	J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, “You Only Look Once: Unified, Real-Time Object Detection,” 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016.
10.	I. Jung, J. Son, M. Baek, and B. Han, “Real-Time MDNet,” Proceedings of the European Conference on Computer Vision (ECCV), pp. 89–104, 2018.
11.	J. Valmadre, L. Bertinetto, J. Henriques, A. Vedaldi, P. H. S. Torr, “End-To-End Representation Learning for Correlation Filter Based Tracking.” IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 2805-2813
