import numpy as np
import cv2 
import tracker
import imagefeature as F
import os
import argparse
import sys
import time
import util
import HOG


def main(args):
    # Load  arg
    dataset = args.dataset_descriptor
    save_directory = args.save_directory
    img_channel = args.multi_channel
    HOG_flag = args.HOG_feature
    scaling = args.scaling
    save_flag = args.save_img
    resize = args.resize
    show_result = args.show_result
    padding = 2
    if args.is_VOT == True:
    	VOT16 = True
    	input_mode = 'VOT'
    else:
      VOT16 = False
      input_mode = 'nVOT'
       
    # Load bbox and image dirs
    bbox_lst = util.load_bbox(os.path.join(dataset+'/groundtruth.txt'),resize,mode = input_mode)
    frames = len(bbox_lst)
    img_lst = util.load_imglst(dataset, frames, VOT16)
    py,px,h,w = bbox_lst[0]
    o_pos = (px,py,w,h)
    pos = (px,py,w,h)

    # Get image information and init parameter
    img = cv2.imread(img_lst[0],img_channel)
    if resize:
        img_size = np.int(img.shape[0]/2),np.int(img.shape[1]/2)
    else:
        img_size = img.shape[:2]

    if HOG_flag:
        window_size = 32,32
        l = 0.0001
        sigma = 0.2 #default 0.6
        inter_factor = 0.012
        scale_weight = 0.99
    else:
        # Use grey image
        window_size = np.int(1+padding)*w,np.int(1+padding)*h
        l = 0.0001
        sigma = 0.2
        inter_factor = 0.015
        scale_weight = 0.99
    f = inter_factor
    
    print("Window size:", window_size)
    # Generate y label
    output_sigma_factor = 1. / 16.
    output_sigma = np.sqrt(np.prod(window_size)) * output_sigma_factor
    cos_window = F.cos_window(window_size)
    print("cos_window:", cos_window.shape)
    y = tracker.generate_gaussian_label(window_size,output_sigma)
    print("Gaussian label:", y.shape)
    rez_shape = y.shape
    # Create file to save result
    tracker_bb =[]
    # Load dataset information and get start position
    title = dataset.split('/')
    title = [ t for t in title if t][-1]
    result_file = os.path.join(save_directory,title+'_'+'result.txt')
    file = open(result_file,'w')
    start_time = time.time()
    
    # Tracking
    for i in range(frames):
        img = cv2.imread(img_lst[i],img_channel)
        if resize:
           img = cv2.resize(img,img_size[::-1])
        if i==0:
            x =  F.get_subwindow(img, pos, window_size, 1, rez_shape)
            print(x.shape)
            x = F.getFeature(x,cos_window,HOG_flag)
            alphaf = tracker.train(x,y,sigma,l)
            z = x
            best_scale = 1
        else:
            x = F.get_subwindow(img, pos, window_size, 1,rez_shape)
            x = F.getFeature(x,cos_window,HOG_flag) 
            response = tracker.detect(alphaf,x,z,sigma)
            
            best_scale = 1
            peak_res = response.max()
            if scaling == True:
                Allscale = [0.96, 1.01, 1.02]
                for scale in Allscale:
                    x = F.get_subwindow(img, pos, window_size, scale,rez_shape)
                    x = F.getFeature(x,cos_window,HOG_flag)
                    res = tracker.detect(alphaf,x,z,sigma)
                    if res.max()*scale_weight > peak_res:
                        peak_res = res.max()
                        best_scale = scale
                        response = res


            # Update position x z alphaf
            new_pos = tracker.update_tracker(response,img_size,pos,HOG_flag, padding, best_scale)
            ww = new_pos[2]
            hh = new_pos[3]
            if new_pos[2]< 0.75*o_pos[2]:
              ww = 0.75*o_pos[2]
            
            if new_pos[3]< 0.75*o_pos[3]:
              hh = 0.75*o_pos[3]
            
            if new_pos[2]>2*o_pos[2]:
              ww = 2*o_pos[2]
            
            if new_pos[3]> 2*o_pos[3]:
              hh = 2*o_pos[3]
            new_pos = (new_pos[0], new_pos[1], ww, hh)
            x = F.get_subwindow(img, new_pos, window_size, best_scale, rez_shape)
            x = F.getFeature(x,cos_window,HOG_flag)
            new_alphaf = tracker.train(x,y,sigma,l)
            # linear interpolate
            alphaf = f*new_alphaf+(1-f)*alphaf
            new_z = x
            z = (1-f)*z+f*new_z
            pos = new_pos
            
            

        # Write the position
        if resize:
            out_pos = [int(pos[1]*2),int(pos[0]*2),int(pos[3]*2),int(pos[2]*2)]
        else:
            out_pos = [pos[1],pos[0],pos[3],pos[2]]
        win_string = [ str(p) for p in out_pos]
        win_string = ",".join(win_string)
        tracker_bb.append(win_string)
        file.write(win_string+'\n')
        

    duration = time.time()-start_time
    fps = int(frames/duration)
    print ('each frame costs %3f second, fps is %d'%(duration/frames,fps))
    file.close()
    
    evaluation, iou = util.evaluate(result_file, bbox_lst, resize = 0)
    print('precision (20pixel):', evaluation)
    print('mean IOU:', iou)

    result = util.load_bbox(result_file,0, mode='nVOT')
    if show_result:
        util.display_tracker(img_lst,result, bbox_lst, save_flag,save_directory)
    
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_descriptor', type=str, 
        help='The directory of video and groundturth file')
    parser.add_argument('save_directory', type=str, 
        help='The directory of result file')
    parser.add_argument('--show_result', type=int, 
        help='Show result or not',default=1)
    parser.add_argument('--resize', type=float, 
        help='Resize img or not',default=0)
    parser.add_argument('--multi_channel', type=int, 
        help='Use multi channel image or not',default=0)
    parser.add_argument('--HOG_feature', type=int, 
        help='Use HOG or not',default=0)
    parser.add_argument('--scaling', type=bool, 
        help='bbox scale factor',default= False)
    parser.add_argument('--save_img', type=int, 
        help='save img or not',default=1)
    parser.add_argument('--is_VOT', type = bool,
        help='whether using a vot dataset', default = True)

    return parser.parse_args(argv)
    

if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))

