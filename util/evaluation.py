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
        
def eval_all(gt_path, result_path, name):
    '''
    input: model, data path 
    return: average precision 

    '''
    gt_list, result_list = read_all_bbox(gt_path, result_path, name)
    precision_list = []
    total_precision = np.zeros((100))
    for gt, result in zip(gt_list, result_list):
        error = location_err(result, gt)
        precision = precision_plot(error)

        total_precision += np.array(precision)
    avg_precision = total_precision/len(gt_list)
    return avg_precision


def main():

    gt = "./GroundTruth/VOT16/"
    MDNet_result = "./Result/MDNet/VOT/results/"
    KCF_result = "./Result/KCF/VOT/results/"
    SiamFC_result = "./Result/SiamFC/VOT/results/"

    MDNet_avg = eval_all(gt, MDNet_result, name = None)
    KCF_avg = eval_all(gt, KCF_result, name = "kcf")
    SiamFC_avg = eval_all(gt, SiamFC_result, name = "siamfc")

    # print(KCF_avg)

    fig, ax = plt.subplots()
    ax.plot(range(100), MDNet_avg, label ='MDNet')
    ax.plot(range(100), KCF_avg, label='KCF')
    ax.plot(range(100), SiamFC_avg, label='SiamFC')

    ax.set(xlabel='Location Error Threshold (px)', ylabel='Precision',
           title='VOT16')
    ax.grid()
    ax.legend()

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
    # main()
    test_main()