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
	return error


def precision_plot(error):
	error_np = np.array(error)
	precision_thresh = range(0,50)
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
def read_all_bbox(gt_root, result_root):
    '''
    input data root path 
    return avg precision 
    '''

    gt_datasets = glob.glob(gt_root + "*/groundtruth_rect.txt")
    result_datasets = glob.glob(result_root + "*/result.json")
    
    gt_list = []
    result_list = []
    for file in gt_datasets:
        lineList = []
        with open(file,'r') as f:
            for line in f:
                lines = [float(number) for number in line.strip().split(",")]
                lineList.append(lines)
        gt_list.append(lineList)

    for file in result_datasets:

        r = convert_json(file)

        result_list.append(r)
    return gt_list, result_list
        
def eval_all(gt_path, result_path, model = "KCF"):
    '''
    input: model, data path 
    return: average precision 

    '''
    gt_list, result_list = read_all_bbox(gt_path, result_path)
    precision_list = []
    total_precision = np.zeros((50))
    for gt, result in zip(gt_list, result_list):
        error = location_err(result, gt)
        precision = precision_plot(error)

        total_precision += np.array(precision)
    avg_precision = total_precision/len(gt_list)
    return avg_precision


def main():

    MDNet_gt = "./GroundTruth/VOT16/"
    MDNet_result = "./Result/MDNet/VOT/results/"


    MDNet_avg = eval_all(MDNet_gt, MDNet_result)

    fig, ax = plt.subplots()
    ax.plot(range(50), MDNet_avg)

    ax.set(xlabel='location error (px)', ylabel='precision',
           title='Average precision vs location error ')
    ax.grid()

    # fig.savefig("test.png")
    plt.show()



if __name__ == '__main__':
    main()