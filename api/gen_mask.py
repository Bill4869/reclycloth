# import numpy as np
# from PIL import Image
import cv2

def gen_mask(im):
  threshold = 150

  # im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
  ret, mask = cv2.threshold(im[:, :, 3], threshold, 255, cv2.THRESH_BINARY)

  return mask


#   # ni = np.array(img)
#   alpha = img[:,:,3]>240
# #   alpha = ni[:,:,3]>200
#   mask = Image.fromarray((alpha*255).astype(np.uint8))


# path = 'target/00000062_01_1.png'
# mask = gen_mask(path)
# cv2.imwrite('out.jpg', mask)