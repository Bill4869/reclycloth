import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

class Fashion_tools(object):
    def __init__(self, ckpt_path, version=1.1):
        self.model   = load_model(ckpt_path)
        self.version = version

    def resize(self, img, long_side_px=512, bgcolor=255):
        org_h, org_w, c = img.shape
        scale = max(org_h, org_w)
        h = int(org_h / scale * long_side_px)
        w = int(org_w / scale * long_side_px)
        resized = cv2.resize(img, (w, h))
        canvas = np.ones((long_side_px, long_side_px, c)).astype(np.uint8) * bgcolor
        margin = ((long_side_px-w)//2, (long_side_px-h)//2)
        canvas[margin[1]:margin[1]+h, margin[0]:margin[0]+w] = resized
        return canvas, margin

    def hist_normalize(self, bgr, mode=0, gridsize=3):
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV) # hsv票色系に変換
        h,s,v = cv2.split(hsv) # 各成分に分割
        if mode == 1:
            v = cv2.equalizeHist(v)
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(gridsize,gridsize))
            v = clahe.apply(v)
        hsv = cv2.merge((h, s, v))
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr

    def create_gamma_img(self, img, gamma):
        gamma_cvt = np.zeros((256,1), dtype=np.uint8)
        for i in range(256):
            gamma_cvt[i][0] = 255*(float(i)/255)**(1.0/gamma)
        return cv2.LUT(img, gamma_cvt)


    def get_dress(self, img, rgb_mode=True, stack=False, hist_normalize=-1, gamma=1.0):
        """limited to top wear and full body dresses (wild and studio working)"""
        """takes input rgb----> return PNG"""
        org_h, org_w, org_c = img.shape
        org_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2BGRA)

        img, margin = self.resize(img)
        # cv2.imwrite("results/p1.png", img)
        if hist_normalize >= 0:
            img = self.hist_normalize(img, mode=hist_normalize)
            # cv2.imwrite("results/p1_norm.png", img)
        if gamma != 1.0:
            img = self.create_gamma_img(img, gamma)
            # cv2.imwrite("results/p1_gamma.png", img)
        h, w, c = img.shape

        if rgb_mode:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # img_tf = tf.image.resize_with_pad(img, target_height=h,target_width=w)
        img_tf = tf.image.resize_with_pad(img, target_height=512,target_width=512)
        rgb  = img_tf.numpy()
        img_tf = np.expand_dims(img_tf,axis=0)/ 255.
        seq = self.model.predict(img_tf)
        seq = seq[3][0,:,:,0]
        seq = np.expand_dims(seq,axis=-1)
        c1x = rgb*seq
        c2x = rgb*(1-seq)
        cfx = c1x+c2x
        dummy = np.ones((rgb.shape[0],rgb.shape[1],1))
        rgbx = np.concatenate((rgb,dummy*255),axis=-1).astype(np.uint8)
        rgbx = rgbx[margin[1]:h-margin[1], margin[0]:w-margin[0]]
        rgbs = np.concatenate((cfx,seq*255.),axis=-1).astype(np.uint8)
        rgbs = rgbs[margin[1]:h-margin[1], margin[0]:w-margin[0]]

        if rgb_mode:
            rgbs = cv2.cvtColor(rgbs, cv2.COLOR_RGBA2BGRA)
            rgbx = cv2.cvtColor(rgbx, cv2.COLOR_RGBA2BGRA)

        mask = rgbs[:, :, 3] > 210
        mask = mask.astype(np.uint8)
        mask = cv2.resize(mask, (org_w, org_h))
        rgbs = org_img.copy()
        rgbs[:,:,3] = rgbs[:,:,3] * mask

        if stack:
            rgbx = cv2.resize(rgbx, (org_w, org_h))
            stacked = np.hstack((org_img,rgbs))
            return stacked
        else:
            return rgbs

    def get_patch(self):
        return None



def segment(np_img):
    ckpt_file = "./pretrain/save_ckp_frozen.h5"
    api = Fashion_tools(ckpt_file)

    result = api.get_dress(np_img, stack=False, hist_normalize=1, gamma=1.5)

    return result