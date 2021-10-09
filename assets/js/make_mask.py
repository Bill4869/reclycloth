import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image   

#必ずUTF-8にて保存のこと
def pil_loader(path):
    # open path as file to avoid ResourceWarning
    # (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


def get_mask(img):

  mask = cv2.Canny(img, 100, 200) 
  mask = cv2.copyMakeBorder(mask, 1, 1, 1, 1, 
    cv2.BORDER_REPLICATE)
  w,h,c=img.shape
  cv2.floodFill( img, mask, (0,0), (0,0,0))
  cv2.floodFill( img, mask, (w-1,0), (0,0,0))
  cv2.floodFill( img, mask, (0,h-1), (0,0,0))
  cv2.floodFill( img, mask, (w-1,h-1), (0,0,0))
  sz = img.shape[:2]
  img=img//1
  cv2.imwrite("canny.png",img)
  return img

if __name__=='__main__':
  img=pil_loader("test_img/skg.jpg")
  print(img)
  img = np.array(img, dtype=np.uint8)
  img=get_mask(img)
  img=img//10
  img=Image.fromarray(img)
  print(img)
  cv2.imwrite("canny.png",img)
