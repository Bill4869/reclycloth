import cv2
import numpy as np


color_dict={0:(255,255,255),5:(166,196,232),1:(48,80,116),2:(255,0,255),3:(0,0,255),4:(255,0,0),6:(128,0,128)}

def gray2color(img):
    print(img.shape)
    part_list=[]
    for k,v in color_dict.items():
        part_list.append(img[:,:,2]==k)

    for i,(k,v) in enumerate(color_dict.items()):
        for RGB in range(3):
            img[:,:,RGB][part_list[i]]=v[RGB]
    return img
pd=10
def color2gray(img):
    part_list=[]
    kernel = np.ones((3, 3), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    for k,v in color_dict.items():
        part_mask=1*(((img[:,:,0]<=pd+v[0]) *(img[:,:,0]>=v[0]-pd))*((img[:,:,1]<=pd+v[1]) *(img[:,:,1]>=v[1]-pd))*((img[:,:,2]<=pd+v[2]) *(img[:,:,2]>=v[2]-pd))).astype(np.uint8)
        print(part_mask)
        part_mask = cv2.dilate(part_mask, kernel, iterations = 3)
        part_list.append(part_mask)

    for i,(k,v) in enumerate(color_dict.items()):
        for RGB in range(3):
            img[:,:,RGB][part_list[i]==1]=k
    else_img=(img[:,:,0]>6)+(img[:,:,1]>6)+(img[:,:,2]>6)

    for RGB in range(3):
        img[:,:,RGB][else_img]=0


    return img,part_list


if __name__ == '__main__':
    img=cv2.imread("gray.png")
    img=gray2color(img)
    cv2.imwrite("color.png",img)

    #color2gray("color_test.png")
