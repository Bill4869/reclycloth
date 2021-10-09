# import cv2
import numpy as np

def blend(target, mask, texture):

# img_path = '000118_0.jpg'
# mask_path = 'mask_150.jpg'
# texture_path = 'result_40.png'

# img = cv2.imread(img_path)
# mask = cv2.imread(mask_path)
# texture = cv2.imread(texture_path)

    res = target.copy()

    res[np.where(mask == 255)] = texture[np.where(mask == 255)]

    return res

    # cv2.imwrite('final_res.jpg', res)