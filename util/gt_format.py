import glob 
import os
def convert_format(filePath):
    lineList = []
    with open(filePath, 'r') as file:        
        for line in file:
            if ',' in line:
                break
            lines = [float(number) for number in line.strip().split()]
            lineList.append(lines)

    return lineList 

def write_data(filePath, dataset):
	with open(filePath, 'w+') as f:
		for d in dataset:
			f.write(str(int(d[0])) + "," + str(int(d[1])) + "," + str(int(d[2])) + "," + str(int(d[3])) + "\n")

def replace(filePath, write_path):

    dataset = convert_format(filePath)
    if len(dataset) != 0:
        write_data(write_path,dataset)
        
def main():
    gt_root = './testdataset/'
    gt_datasets = glob.glob(gt_root + "*/groundtruth_rect.txt")
    for p in gt_datasets:
        new_name = p[:-20] 
        replace(p, p)

if __name__ == '__main__':
    main()