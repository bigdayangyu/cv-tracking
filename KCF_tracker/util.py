import os
import cv2
import time
import numpy as np


def load_bbox(groundtruth_path,resize,dataformat=0, mode = 'nVOT'):
    
    # 'train' mode is used for VOT16 data set 
    # because the bounding box is saved with the coordinates of the four corners
    if mode == 'VOT':
      bbox = []
      with open(groundtruth_path) as f:
        for line in f: 
          content = line.split(',')
          tmp = np.array([float(i) for i in content])
          x_min = int(min(tmp[0], tmp[2], tmp[4], tmp[6]))
          x_max = int(max(tmp[0], tmp[2], tmp[4], tmp[6]))
          w = x_max - x_min
          y_min = int(min(tmp[1], tmp[3], tmp[5], tmp[7]))
          y_max = int(max(tmp[1], tmp[3], tmp[5], tmp[7]))
          h = y_max - y_min
        
          if resize:
            bbox.append([x_min//2, y_min//2, w//2, h//2])
          else:
            bbox.append([x_min, y_min, w, h])
      f.close()
      bbox = np.array(bbox)

    # 'result' mode is used for evaluating the result
    # the bounding box is saved using top-left corner and its width and height
    if mode == 'nVOT':
      bbox=[]
      f = open(groundtruth_path)
      lines=f.readlines()
      for line in lines:
        if line:
            pt= line.strip().split(',')
            bbox.append(pt)
      bbox = np.array(bbox)
      if resize:
          bbox = (bbox.astype('float32')/2).astype('int')
      else:
          bbox = bbox.astype('float32').astype('int')

    if dataformat:
        bbox[:,2] = bbox[:,0]+bbox[:,2]
        bbox[:,3] = bbox[:,1]+bbox[:,3]
    return bbox

def load_imglst(img_dir, num_frames, VOT16 = True):
    #file_lst = [pic for pic in os.listdir(img_dir) if '.jpg' in pic]
    #img_lst = [os.path.join(img_dir,filename) for filename in file_lst]
    #file_num = len(os.listdir(img_dir)) - 7
    img_lst = []
    for i in range(1,num_frames+1):
      if VOT16:
        file_dir = os.path.join(img_dir + "/%08d.jpg"%i)
      else:
        file_dir = os.path.join(img_dir + "/%04d.jpg"%i)
      img_lst.append(file_dir)
      
    return img_lst 


def display_tracker(img_lst,bbox_lst,bbox_true_lst,save_flag,save_directory):
    length = min(len(img_lst),len(bbox_lst))
    for i in range(length):
        img = cv2.imread(img_lst[i])
        name = save_directory + "/%08d.jpg"%i
        visual(img,bbox_lst[i],bbox_true_lst[i], save_flag, name)
        #if save_flag:
            #if i%50==0:
                #save(img,bbox_lst[i],str(i)+'.png')
    cv2.destroyAllWindows()

def visual(img,bbox, bbox_true, save_flag, name):
    (x,y,w,h) = bbox
    pt1,pt2 = (x,y),(x+w,y+h)
    img_rec = cv2.rectangle(img,pt1,pt2,(0,255,0),2)
    (x,y,w,h) = bbox_true
    pt1,pt2 = (x,y),(x+w,y+h)
    img_rec = cv2.rectangle(img_rec,pt1,pt2,(0,0,255),2)
    cv2.imshow('window',img_rec)
    cv2.waitKey(20)
    if save_flag: 
      cv2.imwrite(name, img_rec)


def evaluate(result_file, bbox, resize):
  """
  Evaluate 20 pixel precision
  """ 
  # Calculate pixel precision
  acc_cntr = 0
  result = load_bbox(result_file,resize,dataformat=0, mode = 'nVOT')
  total_iou = 0
  cntr = 0
  for r, b in zip(result, bbox):
    cntr+=1
    if cntr > 500:
      break
    rx = r[0] + r[2]//2
    ry = r[1] + r[3]//2
    bx = b[0] + b[2]//2
    by = b[1] + b[3]//2
    if (rx - bx)**2 + (ry - by)**2 <= 20*20:
      acc_cntr += 1
  
  # Calculate IOU
  
    arear = r[2]*r[3]
    areab = b[2]*b[3]
  
    x_left = max(r[0], b[0])
    y_left = max(r[1], b[1])
    x_right = min(r[0] + r[2], b[0] + b[2])
    y_right = min(r[1] + r[3], b[1] + b[3])
  
    if x_right<= x_left or y_right<= y_left:
      overlap = 0
    else:
      overlap = (x_right-x_left)*(y_right-y_left)

    iou = overlap/(arear+areab-overlap)
    total_iou += iou

  frames = len(bbox)
  
  
  return acc_cntr / frames, total_iou/frames
  
