import numpy as np 
import json
import os
import matplotlib.pyplot as plt
import glob 

def read_matches(filePath):
    lineList = []
    with open(filePath, 'r') as file:
        for line in file :
            lines = [float(number) for number in line.strip().split(",")]
            lineList.append(lines)
    return lineList 



	

def convert_json(file_path):	
    with open(file_path, 'r') as f:
        datastore = json.load(f)

    result = datastore["res"]

    return result

def read_all_bbox(gt_root, result_root,name):
    '''
    input data root path 
    return avg precision 
    '''

    gt_datasets = glob.glob(gt_root + "*/groundtruth_rect.txt")

    result_datasets = glob.glob(result_root + "*/result.json")

    gt_datasets = sorted(gt_datasets)
    result_datasets = sorted(result_datasets)
    
    if len(result_datasets) != 0:
        gt_list = []
        result_list = []

        for file in gt_datasets:
            # print('groundtruth file: %s' %file)
            lineList = []
            with open(file,'r') as f:
                for line in f:
                    lines = [float(number) for number in line.strip().split(",")]
                    lineList.append(lines)
            gt_list.append(lineList)

        for file in result_datasets:
            # print('results file: %s' %file)
            r = convert_json(file)
            result_list.append(r)

    else:
        if name == "kcf":
        	result_datasets = glob.glob(result_root + "*/result.txt")
        if name == "siamfc":
        	result_datasets = glob.glob(result_root + "*/results.txt")

        result_datasets = sorted(result_datasets)

        gt_list = []
        result_list = []


        for file in gt_datasets:
            # print('groundtruth file: %s' %file)
            lineList = []

            with open(file,'r') as f:
                for line in f:
                    lines = [float(number) for number in line.strip().split(",")]
                    lineList.append(lines)
            gt_list.append(lineList)

        for file in result_datasets:
            # print('results file: %s' %file)
            lineList = []
            with open(file, 'r') as f:
                cntr = 0
                for line in f:
                    lines = [float(number) for number in line.strip().split(",")]
                    lineList.append(lines)
                    if cntr==0:
                    	lineList.append(lines)
                    cntr += 1
            result_list.append(lineList)

    return gt_list, result_list


def location_err(bbox, gt):
    error = []
    for b, g in zip(bbox, gt):
        xb, yb, wb, hb = b[0], b[1], b[2], b[3]
        xg, yg, wg, hg = g[0], g[1], g[2], g[3]

        bbox_center = [xb + wb/2 , yb + hb/2]
        gt_center = [xg + wg/2 , yg + hg/2]

        # pixel distance 
        err = np.sqrt((bbox_center[0] - gt_center[0])**2 +(bbox_center[1] - gt_center[1])**2)
        error.append(err)

    # print(b)
    # print('space')
    # print(g)
    return error


def precision_plot(error):
    error_np = np.array(error)
    precision_thresh = range(0,100)
    precision = []
    for p in precision_thresh:
        current_p = np.where(error_np < p, 1, 0).sum()/len(error)
        precision.append(current_p)
    return precision


def eval_all_precision(gt_path, result_path, name):
    '''
    Calculates average IoU across all datasets
    Inputs: ground truth path, result path, name of model (deafult MDNet) 
    Outputs: average iou, 1x100 numpy array 
    '''

    gt_list, result_list = read_all_bbox(gt_path, result_path, name)

    total_precision = np.zeros((100))
    for gt, result in zip(gt_list, result_list):
        error = location_err(result, gt)
        precision = precision_plot(error)

        total_precision += np.array(precision)
    avg_precision = total_precision/len(gt_list)
    return avg_precision


def calc_iou(bbox, gt):
    '''
    Calculates the IoU for a given dataset
    Input: bbox is an nx4 list of bounding box results
           gt is an nx4 list of ground truth bounding boxes
    Output: list of IoU for each frame

    '''
    iou = []
    for b, g in zip(bbox, gt):
        xb, yb, wb, hb = b[0], b[1], b[2], b[3]
        xg, yg, wg, hg = g[0], g[1], g[2], g[3]

        area_b = wb*hb
        area_g = wg*hg

        x_left = max(xb, xg)
        y_left = max(yb, yg)
        x_right = min(xb+wb, xg+wg)
        y_right = min(yb+hb, yg+hg)

        if x_right <= x_left or y_right <= y_left:
            overlap = 0
        else:
            overlap = (x_right-x_left)*(y_right-y_left)

        iou_calc = overlap/(area_b + area_g - overlap)
        iou.append(iou_calc)

    return iou


def success_plot(iou):
    '''
    Calculates succss rate at each threshold
    Input: iou is a 1xn list of iou for each frame
    Output: success is a 1x100 list of success rates for each threshold
    '''

    iou_np = np.array(iou)
    success_thresh = np.arange(0,1,0.01)
    success = []
    for s in success_thresh:
        current_s = np.where(iou_np > s, 1, 0).sum()/len(iou)
        success.append(current_s)
    return success


def eval_all_iou(gt_path, result_path, name):
    '''
    Calculates average IoU across all datasets
    Inputs: ground truth path, result path, name of model (deafult MDNet) 
    Outputs: average iou, 1x100 numpy array
    '''

    gt_list, result_list = read_all_bbox(gt_path, result_path, name)

    total_iou = np.zeros((100))
    for gt, result in zip(gt_list, result_list):
        iou = calc_iou(result, gt)
        success = success_plot(iou)

        total_iou += np.array(success)
    avg_iou = total_iou/len(gt_list)
    return avg_iou


def main():

    gt_VOT = "./GroundTruth/VOT16/"
    MDNet_VOTresult = "./Result/MDNet/VOT/results/"
    KCF_VOTresult = "./Result/newKCF/VOT/results/"
    SiamFC_VOTresult = "./Result/SiamFC/VOT/results/"

    # gt_OTB = "./GroundTruth/OTB/"
    # MDNet_OTBresult = "./Result/MDNet/OTB/results/"
    # newKCF_OTBresult = "./Result/newKCF/OTB/results/"
    # SiamFC_OTBresult = "./Result/SiamFC/OTB/results/"


    ## Figure 1: VOT precision
    MDNet_VOTprec = eval_all_precision(gt_VOT, MDNet_VOTresult, name = None)
    KCF_VOTprec = eval_all_precision(gt_VOT, KCF_VOTresult, name = "kcf")
    SiamFC_VOTprec = eval_all_precision(gt_VOT, SiamFC_VOTresult, name = "siamfc")

    fig1, ax1 = plt.subplots()
    ax1.plot(range(100), MDNet_VOTprec, label ='MDNet')
    ax1.plot(range(100), KCF_VOTprec, label='Improved KCF')
    ax1.plot(range(100), SiamFC_VOTprec, label='SiamFC')

    ax1.set(xlabel='Location Error Threshold (px)', ylabel='Precision',
           title='VOT16 Precision')
    ax1.grid()
    ax1.legend()

    ## Figure 2: VOT success (IoU)
    MDNet_VOTiou = eval_all_iou(gt_VOT, MDNet_VOTresult, name = None)
    KCF_VOTiou = eval_all_iou(gt_VOT, KCF_VOTresult, name = "kcf")
    SiamFC_VOTiou = eval_all_iou(gt_VOT, SiamFC_VOTresult, name = "siamfc")

    fig2, ax2 = plt.subplots()
    ax2.plot(np.arange(0,1,0.01), MDNet_VOTiou, label ='MDNet')
    ax2.plot(np.arange(0,1,0.01), KCF_VOTiou, label='Improved KCF')
    ax2.plot(np.arange(0,1,0.01), SiamFC_VOTiou, label='SiamFC')

    ax2.set(xlabel='Overlap Threshold', ylabel='Success Rate',
           title='VOT16 Success Rate')
    ax2.grid()
    ax2.legend()

    ## Figure 3: OTB precision
    MDNet_OTBprec = eval_all_precision(gt_OTB, MDNet_OTBresult, name = None)
    KCF_OTBprec = eval_all_precision(gt_OTB, KCF_OTBresult, name = "kcf")
    SiamFC_OTBprec = eval_all_precision(gt_OTB, SiamFC_OTBresult, name = "siamfc")

    fig3, ax3 = plt.subplots()
    ax3.plot(range(100), MDNet_OTBprec, label ='MDNet')
    ax3.plot(range(100), KCF_OTBprec, label='Improved KCF')
    ax3.plot(range(100), SiamFC_OTBprec, label='SiamFC')

    ax3.set(xlabel='Location Error Threshold (px)', ylabel='Precision',
           title='OTB Precision')
    ax3.grid()
    ax3.legend()

    ## Figure 4: OTB success (IoU)
    MDNet_OTBiou = eval_all_iou(gt_OTB, MDNet_OTBresult, name = None)
    KCF_OTBiou = eval_all_iou(gt_OTB, KCF_OTBresult, name = "kcf")
    SiamFC_OTBiou = eval_all_iou(gt_OTB, SiamFC_OTBresult, name = "siamfc")

    fig4, ax4 = plt.subplots()
    ax4.plot(np.arange(0,1,0.01), MDNet_OTBiou, label ='MDNet')
    ax4.plot(np.arange(0,1,0.01), KCF_OTBiou, label='Improved KCF')
    ax4.plot(np.arange(0,1,0.01), SiamFC_OTBiou, label='SiamFC')

    ax4.set(xlabel='Overlap Threshold', ylabel='Success Rate',
           title='OTB Success Rate')
    ax4.grid()
    ax4.legend()

    # fig.savefig("test.png")
    plt.show()

def test_main():
	gt = "./GroundTruth/VOT16/"
	SiamFC_result = "./Result/SiamFC/VOT/results/"
	KCF_result = "./Result/KCF/VOT/results/"
	MDNet_result = "./Result/MDNet/VOT/results/"


	gt_list, result_list = read_all_bbox(gt, MDNet_result, name = None)
	print(len(gt_list),len(result_list))
	cntr = -1
	for i in range(8):
		cntr = cntr + 1
		bag_result = result_list[cntr]
		bag_gt = gt_list[cntr]
		error =location_err(bag_result, bag_gt)
		precision = precision_plot(error)
		print(precision[21])
	gt_list, result_list = read_all_bbox(gt, SiamFC_result, name = 'siamfc')
	print('siamfc')
	cntr = -1
	for i in range(8):
		cntr = cntr + 1
		bag_result = result_list[cntr]
		bag_gt = gt_list[cntr]
		error =location_err(bag_result, bag_gt)
		precision = precision_plot(error)
		print(precision[21])
	gt_list, result_list = read_all_bbox(gt, KCF_result, name = 'kcf')
	print('kcf')
	cntr = -1
	for i in range(8):
		cntr = cntr + 1
		bag_result = result_list[cntr]
		bag_gt = gt_list[cntr]
		error =location_err(bag_result, bag_gt)
		precision = precision_plot(error)
		print(precision[21])
		#precision = precision_plot(error)

	# fig, ax = plt.subplots()
	# # ax.plot(range(50), MDNet_avg)
	# ax.plot( error)
	# # ax.plot(range(50), SiamFC_avg)

	# ax.set(xlabel='Location Error Threshold (px)', ylabel='Precision',
	#        title='VOT16')
	# ax.grid()

	# # fig.savefig("test.png")
	# plt.show()




if __name__ == '__main__':
    main()
    # test_main()