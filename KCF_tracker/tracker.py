import os
import numpy as np
import cv2 

def generate_gaussian_label(window_size,sigma):
    """
    Generate the regression label, which is Gaussian shaped and has a bandwidth defined by sigma
    Args: window_size (height, width)
          sigma 
    """
    h,w = window_size
    #rx = np.arange(w/2)
    #ry = np.arange(h/2)
    #x = np.hstack((rx,rx[::-1]))
    #y = np.hstack((ry,ry[::-1]))
    #xx,yy = np.meshgrid(x,y)
    #label = np.exp(-1*(xx**2+yy**2)/(sigma**2))
    
    #return label
    
    x = np.arange(-w//2 + 1, w//2 + 1)
    y = np.arange(-h//2 + 1, h//2 + 1)
  
    xx, yy = np.meshgrid(x,y, indexing = 'xy')
    label = np.exp(-0.5*(xx**2+yy**2)/(sigma**2))
    label = np.roll(label, -w//2 + 1, axis = 1)
    label = np.roll(label, -h//2 + 1, axis = 0)

    assert label[0,0] == 1, 'Wrong shift.'

    return label

def fft(img):
    """
    2D fourier transform
    """
    f = np.fft.fft2(img,axes=(0,1))
    return f 


def train(x,y,sigma,lamb):
    """
    Eq.17 Train
    Args: x input feature
          y regression label
    Output: alphaf in Fourier Domain
    """
    k = guassian_correlation(x,x,sigma)
    alphaf = fft(y)/(fft(k)+lamb)
    return alphaf

def detect(alphaf,x, model_x,sigma):
    """
    Eq.22
    """
    k = guassian_correlation(model_x, x,sigma)
    response = np.real(np.fft.ifft2(alphaf*fft(k)))
    return response

def guassian_correlation(x1,x2,sigma):
    """
    Eq.31
    Calculate the correlation of the Gaussian kernel
    Args: x1 (model_x)
          x2
          sigma
    """
    
    if len(x1.shape)==2:
      # Use gray scale
      c = np.fft.ifft2((np.conj(fft(x1))*fft(x2)))
    else:
      # Use HOG
      c = np.fft.ifft2(np.sum(np.conj(fft(x1))*fft(x2),2))
    d= (x1*x1).sum() + (x2*x2).sum() - 2*c
    k = np.real(np.exp(-1 * d / (sigma**2*x1.size)))
    return k


def update_tracker(response,img_size,pos,padding, scale_factor=1):
    """
    Update the tracker
    Args: response [real domain], window size 
           
    """
    res_w,res_h = response.shape
    iw,ih = img_size
    px,py,w,h = pos
    res_pos = np.unravel_index(response.argmax(),response.shape)
    move = list(res_pos)
    
    scale_w = 1.0*scale_factor*(w*(1+padding))/res_w
    scale_h = 1.0*scale_factor*(h*(1+padding))/res_h
    
    
    if move[0] > res_w/2:
      move[0] = move[0] - res_w
    if move[1] > res_h/2:
      move[1] = move[1] - res_h
    px_new = px + 1.*move[0]*scale_w
    py_new = py + 1.*move[1]*scale_h
        #px_new = [px+1.0*move[0]*scale_w,px-(start_w-1.0*move[0])*scale_w][move[0]>start_w/2] 
        #py_new = [py+1.0*move[1]*scale_h,py-(start_h-1.0*move[1])*scale_h][move[1]>start_h/2]
    px_new = np.int(px_new) 
    py_new = np.int(py_new)
    
    if px_new<0: px_new = 0
    if px_new>iw: px_new = iw-1
    if py_new<0: py_new = 0
    if py_new>ih: py_new = ih-1
    w_new = np.ceil(w*scale_factor)
    h_new = np.ceil(h*scale_factor)
    
    new_pos = (px_new,py_new,w_new,h_new)
    return new_pos




