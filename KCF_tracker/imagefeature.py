import numpy as np
import cv2
import HOG

def cos_window(window_size):
    """
    Generate the periodic cosine window
    Args: window_size(height, width)
    """
    return np.outer(np.hanning(window_size[0]),np.hanning(window_size[1]))

def process_cos(img,cos_window):
    if len(img.shape)==2:
        return img*cos_window
    elif len(img.shape) == 3:
        channel = img.shape[2]
        cos_mc = np.tile(cos_window,(channel,1,1))
        cos_window_out = np.transpose(cos_mc,[1,2,0])
        return img*cos_window_out

def getFeature(x,cos_window,HOG_flag=0):
    if HOG_flag:
        x = HOG.hog(x)
    else:
        x = x/255.
        x = (x - np.mean(x)) / np.std(x)
    x = process_cos(x,cos_window)
    return x

def get_subwindow(img, bbox, window_size, scale_factor=1 ,rez_to_yshape=None):
    (x,y,w,h) = bbox
    x_center = np.int(x + w//2)
    y_center = np.int(y + h//2)
    #w = np.floor(1.0*w*scale_factor)
    #h = np.floor(1.0*h*scale_factor)
    ix,iy = img.shape[0],img.shape[1]
    
    x_min = int(x_center - scale_factor*window_size[0]//2)
    x_max = int(x_center + scale_factor*window_size[0]//2)
    y_min = int(y_center - scale_factor*window_size[1]//2)
    y_max = int(y_center + scale_factor*window_size[1]//2)
    
    x_left_pad = 0
    y_left_pad = 0
    x_right_pad = 0
    y_right_pad = 0
    if x_min < 0:
      x_left_pad = x_min*-1
    if y_min < 0:
      y_left_pad = y_min*-1
    if x_max > ix:
      x_right_pad = x_max - ix
    if y_max > iy: 
      y_right_pad = y_max - iy 
    
    x_min = max(0, x_min)
    x_max = min(ix, x_max)
    y_min = max(0, y_min)
    y_max = min(iy, y_max)   
    ww, hh = x_max - x_min, y_max - y_min
    img_crop = img[x_min:x_min+ww,y_min:y_min+hh]
    
    if x_left_pad == 0 and y_left_pad == 0 and x_right_pad == 0 and y_right_pad == 0:
        
        if rez_to_yshape is not None:
            return cv2.resize(img_crop,rez_to_yshape[::-1])
        else:
            return img_crop
    else:
    # Pad with edge value (same as the paper implementation)
        if len(img_crop.shape)==3:
            img_crop = np.pad(img_crop,
                              ((x_left_pad,x_right_pad),(y_left_pad,y_right_pad),(0,0)),
                              'edge')
        else:
            img_crop = np.pad(img_crop,
                              ((x_left_pad,x_right_pad),(y_left_pad,y_right_pad)),
                              'edge')
        
        if rez_to_yshape is not None:
            return cv2.resize(img_crop,rez_to_yshape[::-1])
        else:
            return img_crop
