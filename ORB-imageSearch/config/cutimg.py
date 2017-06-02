import cv2
import os
def cutimage(dir,suffix):
 # allfiles = []
  for root,dirs,files in os.walk(dir):
    for file in files:
      filepath = os.path.join(root, file)
      filesuffix = os.path.splitext(filepath)[1][1:]
      if  filesuffix in suffix:
        #allfiles.append(file)
        image = cv2.imread(file)
        #cv2.imshow(file,image)
        dim =(350,200)
        resized =cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
        #cv2.imshow("resize:%s"%file,resized)
        cv2.imwrite("../cv/%s"%file,resized)
  cv2.waitKey(0)

suffix = ["jpg"]
dir = '.'
cutimage(dir,suffix)
