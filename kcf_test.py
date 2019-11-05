from __future__ import print_function
import sys
import cv2
import os
from random import randint

class ImageTracker():
    def __init__(self, trackerType = 'KCF'):
        
        trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

        if trackerType == trackerTypes[0]:

            self.tracker = cv2.TrackerBoosting_create()
        elif trackerType == trackerTypes[1]: 
            self.tracker = cv2.TrackerMIL_create()
        elif trackerType == trackerTypes[2]:
            self.tracker = cv2.TrackerKCF_create()
        elif trackerType == trackerTypes[3]:
            self.tracker = cv2.TrackerTLD_create()
        elif trackerType == trackerTypes[4]:
            self.tracker = cv2.TrackerMedianFlow_create()
        elif trackerType == trackerTypes[5]:
            self.tracker = cv2.TrackerGOTURN_create()
        elif trackerType == trackerTypes[6]:
            self.tracker = cv2.TrackerMOSSE_create()
        elif trackerType == trackerTypes[7]:
            self.tracker = cv2.TrackerCSRT_create()
        else:
            self.tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in trackerTypes:
                print(t)
    def tracking(self, path):
        template_path = os.path.join(path+ "0001.jpg")
        frame = cv2.imread(template_path)
        ## Select boxes
        bboxes = []
        colors = [] 
        while True:
            # draw bounding boxes over objects
            # selectROI's default behaviour is to draw box starting from the center
            # when fromCenter is set to false, you can draw box starting from top left corner
            bbox = cv2.selectROI('MultiTracker',frame)
            bboxes.append(bbox)
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            print("Press q to quit selecting boxes and start tracking")
            print("Press any other key to select next object")
            k = cv2.waitKey(0) & 0xFF
            if (k == 113):  # q is pressed
                break

        print('Selected bounding boxes {}'.format(bboxes))


        # Create MultiTracker object
        multiTracker = cv2.MultiTracker_create()
         
        # Initialize MultiTracker 
        for bbox in bboxes:
          multiTracker.add(self.tracker, frame, bbox)

        n_files = len(os.listdir(path))
        for i in range(2,n_files):
          # path = "/Users/liruilin/Desktop/course/JHU/CV/cv-tracking/Biker/img/"
          imagePath = os.path.join(path+ "%04d.jpg"%i)
          
          frame = cv2.imread(imagePath)
           
          # get updated location of objects in subsequent frames
          success, boxes = multiTracker.update(frame)
          print(success)
          # draw tracked objects
          for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
         
          # show frame
          cv2.imshow('MultiTracker', frame)
           
          # quit on ESC button
          if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

# Extra Credit
def main():

    path = "/Users/liruilin/Desktop/course/JHU/CV/cv-tracking/datasets/Panda/img/"
    # choose from ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSxSE', 'CSRT']
    tracker = ImageTracker('KCF')
    tracker.tracking(path)
  



if __name__ == '__main__':
    main()
         
