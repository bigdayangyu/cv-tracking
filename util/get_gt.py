import glob 
import os
# Python Copy File - Sample Code
        
from shutil import copy
from sys import exit
def copy_gt(source, target):

    # adding exception handling
    try:
        copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    print("\nFile copy done!\n")

def main():
    gt_root = './testdataset/'
    gt_datasets = glob.glob(gt_root + "*/groundtruth_rect.txt")
    target_root = './test_target/'
    for p in gt_datasets:
        new_name = p[14:-21] 
     
        new_target = target_root + new_name + '/'
        
        print(p)
        print(new_target)
        if os.path.exists(new_target) == False:
            os.makedirs(new_target)
        copy_gt(p , new_target)

if __name__ == '__main__':
    main()