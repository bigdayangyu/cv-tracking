import cv2
import selectivesearch

img = cv2.imread('road/00000526.jpg')
img_lbl, regions = selectivesearch.selective_search(img, scale = 500, sigma=0.9, min_size = 400)
print(len(regions))

for i in range(len(regions)):
  label = regions[i]
  rect = label['rect']
  
  pt1 = rect[0], rect[1]
  pt2 = rect[0] + rect[2], rect[1] +rect[3]
  cv2.rectangle(img,pt1, pt2, (0,255,0),2)

cv2.imshow("test", img)
cv2.waitKey(0)

