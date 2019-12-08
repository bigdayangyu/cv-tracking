

import cv2
import numpy as np
import selectivesearch
from scipy import signal

def selectiveSearch(img, pos, template):
  """
  Args:
    Image: the orginal image. Used for selective search
    Pos: (x,y,w,h) of the bounding box
    Template: the template captured in the first frame
  Output:
    proposed regions
  """
  x,y,w,h = pos
  min_size = np.floor(w*h/4).astype(int)
  img_lbl, regions = selectivesearch.selective_search(img, scale = 500, sigma=0.9, min_size = min_size)
  candidates = []
  rect_img = img.copy()
  for item in regions:
    rect = item['rect']
    pt1 = rect[0], rect[1]
    pt2 = rect[0] + rect[2], rect[1] +rect[3]
    cv2.rectangle(rect_img,pt1, pt2, (0,255,0),2)
    if rect[2] > 1.75*h or rect[3] > 1.75*w or rect[2]<0.25*h or rect[3] < 0.25*w :
      continue
    if np.abs(rect[0] - y) > img.shape[1]/1.5 or np.abs(rect[1] - x) > img.shape[0]/1.5:
      continue 
    candidates.append(rect)
  #cv2.imshow("test", rect_img)
  #cv2.waitKey(0)
  best_rect = findPatch(img, candidates, template)
  return best_rect
 
def findPatch(img, candidates, template):
  """
  Find the most suitable candidates use crosscorrelation
  """
  if len(candidates) == 0:
    return None
  if len(candidates) >= 10:
    candidates = candidates[0:10] # search the first 15 boxes
  best_score = -1
  best_rect = None
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  for rect in candidates: 
    y,x,h,w = rect
    patch = img[x:x+w, y:y+h]
    patch = cv2.resize(patch, (template.shape[1],template.shape[0]))
    #cv2.imshow("Test", patch)
    #cv2.waitKey(0)
    
    score = correlation_coefficient(patch, template)
    #print(score)
    if score > best_score:
      best_score = score
      best_rect = rect
  
  if best_score < 0:
    return None
  else:
    x,y,w,h = best_rect
  #cv2.imshow("Test", img[y:y+h, x:x+w])
  #cv2.waitKey(0)
    best_rect = (y,x,h,w) 
    return best_rect

def correlation_coefficient(patch1, patch2):
    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product  
