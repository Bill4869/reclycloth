from pydantic.main import BaseModel
from fastapi import FastAPI
from PIL import Image
from fastapi import FastAPI, Request, File, UploadFile
from typing import List
import io
import cv2
import base64
import numpy as np
from skgtoimg import skech2img
from skgtoimg_shoes import skech2img_shoes
import copy

from gen_mask import gen_mask
from PIL import Image
import cv2

from change_color import color2gray
from mask2img import mask2img

from txt_syn_trans1 import texture_synth1
from txt_syn_trans import texture_synth
from segment import segment
from blend import blend

from fastapi.middleware.cors import CORSMiddleware
from make_mask import get_mask
from skgtoimg import pil_loader


from fastapi.middleware.cors import CORSMiddleware
ori_txt=pil_loader("ori_txt.jpg")
use_txt_syn=False

app = FastAPI()
test_dir="test/"

origins = [
    "http://127.0.0.1:8887",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class imgs(BaseModel):
    skg: str
    txt: str

def base642img(code):
    img=code.split(',',1)[1]
    img = base64.b64decode(img) # base64に変換された画像データを元のバイナリデータに変換 # bytes
    img = io.BytesIO(img) # _io.BytesIO pillowで扱えるように変換
    img = Image.open(img).convert("RGB") 
    return img
def resize(img, long_side_px=512):
    org_h, org_w, c = img.shape
    scale = max(org_h, org_w)
    h = int(org_h / scale * long_side_px)
    w = int(org_w / scale * long_side_px)
    resized = cv2.resize(img, (w, h))

    return resized

@app.post('/api/imgtoimg') # methodとendpointの指定
async def skechtoimg(Images:imgs):
    skg=base642img(Images.skg)
    txt=base642img(Images.txt)
    txt = np.array(txt, dtype=np.uint8)
    img = np.array(skg, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #txt = cv2.cvtColor(txt, cv2.COLOR_RGB2BGR)
    img_h,img_w,c=img.shape
    #img = resize(img, long_side_px=512)
    img_txt = resize(img, long_side_px=512)
    cv2.imwrite(test_dir+"input.png",img)
    cv2.imwrite(test_dir+"texture.png",cv2.cvtColor(txt, cv2.COLOR_RGB2BGR))

    
    h,w,c=txt.shape
    s=70
    #txt=txt[h//2-s:h//2+s,w//2-s:w//2+s,:]
    s=min(h,w)
    txt=txt[s//4:s*3//4,s//4:s*3//4,:]
    h,w,c=txt.shape
    txt = cv2.resize(txt, dsize=(100, 100))
    h,w,c=txt.shape


    in_img=copy.deepcopy(img)

    seg = segment(img)
    mask=gen_mask(seg)
    img_txt=img_txt.astype(np.float32)
    img_txt[np.where(mask != 255)]=0
    trans = texture_synth(txt, img_txt, patch_length= int(80))
    trans=cv2.resize(trans,(img_w,img_h))
    mask=cv2.resize(mask,(img_w,img_h))
    #trans_resize = resize(trans,long_side_px=512)
    img = blend(img, mask, trans)
    img = resize(img, long_side_px=512)
    ret, dst_data = cv2.imencode('.jpg', img)
    dst_str = base64.b64encode(dst_data)
    cv2.imwrite(test_dir+"mask.png",mask)
    cv2.imwrite(test_dir+"in_texture.png",trans)
    trans[np.where(mask != 255)]=0
    in_img[np.where(mask != 255)]=255
    cv2.imwrite(test_dir+"mask_cloth_w.png",in_img)
    in_img[np.where(mask != 255)]=0
    cv2.imwrite(test_dir+"mask_cloth_b.png",in_img)
    cv2.imwrite(test_dir+"syn.png",trans)
    cv2.imwrite(test_dir+"output.png",img)
    return {"response": dst_str}

@app.post('/api/skechtoimg_cloth') # methodとendpointの指定
async def skechtoimg(Images:imgs):
    #skg= Image.open(io.BytesIO(file[0].file.read())).convert('RGB')
    #txt= Image.open(io.BytesIO(files[1].file.read())).convert('RGB')
    skg=base642img(Images.skg)
    txt=base642img(Images.txt)
    txt = np.array(txt, dtype=np.uint8)
    img = np.array(skg, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    txt = cv2.cvtColor(txt, cv2.COLOR_RGB2BGR)
    cv2.imwrite(test_dir+"input.png",img)
    cv2.imwrite(test_dir+"texture.png",txt)
    img,part_mask=color2gray(img)
    img=mask2img(img)
    #background,body,hair,face,Upper clothes, Down clothes , shoes
    up_cloth_mask=part_mask[4]
    up_cloth_mask=cv2.resize(up_cloth_mask, dsize=(256, 256))
    up_cloth_mask[up_cloth_mask!=0]=255
    mask=up_cloth_mask

    h,w,c=txt.shape
    s=70
    #txt=txt[h//2-s:h//2+s,w//2-s:w//2+s,:]
    s=min(h,w)
    txt=txt[s//4:s*3//4,s//4:s*3//4,:]
    h,w,c=txt.shape
    txt = cv2.resize(txt, dsize=(100, 100))
    h,w,c=txt.shape

    cv2.imwrite(test_dir+"cloth.png",img)
    in_img=copy.deepcopy(img)
    in_img[np.where(mask != 255)]=0


    trans = texture_synth1(txt, in_img,patch_length = min(h,w)//2)
    trans = cv2.cvtColor(trans, cv2.COLOR_BGR2RGB)
    img = blend(img, up_cloth_mask, trans)
    img = resize(img, long_side_px=512)
    


    ret, dst_data = cv2.imencode('.jpg', img)
    dst_str = base64.b64encode(dst_data)
    cv2.imwrite(test_dir+"in_texture.png",trans)
    trans[np.where(mask != 255)]=0
    cv2.imwrite(test_dir+"mask.png",mask)
    trans[np.where(mask != 255)]=0
    cv2.imwrite(test_dir+"syn.png",trans)
    cv2.imwrite(test_dir+"output.png",img)
    cv2.imwrite(test_dir+"mask_cloth.png",in_img)
    return {"response": dst_str}


@app.post('/api/skechtoimg_bag') # methodとendpointの指定
async def skechtoimg(Images:imgs):
    skg=base642img(Images.skg)
    txt=base642img(Images.txt)
    img = np.array(skg, dtype=np.uint8)
    img=get_mask(img)
    seg=Image.fromarray(img)

    cv2.imwrite(test_dir+"input.png",cv2.cvtColor(np.array(skg), cv2.COLOR_RGB2BGR))
    cv2.imwrite(test_dir+"texture.png",cv2.cvtColor(np.array(txt), cv2.COLOR_RGB2BGR))
    cv2.imwrite(test_dir+"mask.png",cv2.cvtColor(np.array(seg), cv2.COLOR_RGB2BGR))

    img=skech2img(skg,seg,txt)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if use_txt_syn:
        img = cv2.resize(img, dsize=(256,256))


        mask=1*((img[:,:,0]>=240)*(img[:,:,1]>=240)*(img[:,:,2]>=240)).astype(np.float32)
        mask=255*(1-mask)

        img=img.astype(np.float32)

        txt = np.array(txt, dtype=np.uint8)
        txt = cv2.cvtColor(txt, cv2.COLOR_RGB2BGR)
        h,w,c=txt.shape
        s=min(h,w)
        txt=txt[s//4:s*3//4,s//4:s*3//4,:]
        h,w,c=txt.shape
        txt = cv2.resize(txt, dsize=(100, 100))
        h,w,c=txt.shape
        trans = texture_synth1(txt, img,patch_length = min(h,w)//2)
        trans = cv2.cvtColor(trans, cv2.COLOR_BGR2RGB)
        img = blend(img, mask, trans)

        trans[np.where(mask != 255)]=0
        cv2.imwrite(test_dir+"syn.png",trans)
    img = resize(img, long_side_px=512)
    cv2.imwrite(test_dir+"output.png",img)
    ret, dst_data = cv2.imencode('.jpg', img)
    dst_str = base64.b64encode(dst_data)
    return {"response": dst_str}
    
    
    
@app.post('/api/skechtoimg_shoes') # methodとendpointの指定
async def skechtoimg(Images:imgs):
    skg=base642img(Images.skg)
    txt=base642img(Images.txt)
    img = np.array(skg, dtype=np.uint8)
    img=get_mask(img)
    seg=Image.fromarray(img)
    cv2.imwrite(test_dir+"input.png",cv2.cvtColor(np.array(skg), cv2.COLOR_RGB2BGR))
    cv2.imwrite(test_dir+"texture.png",cv2.cvtColor(np.array(txt), cv2.COLOR_RGB2BGR))
    cv2.imwrite(test_dir+"mask.png",cv2.cvtColor(np.array(seg), cv2.COLOR_RGB2BGR))

    img=skech2img_shoes(skg,seg,txt)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if use_txt_syn:
        img = cv2.resize(img, dsize=(256,256))


        mask=1*((img[:,:,0]>=240)*(img[:,:,1]>=240)*(img[:,:,2]>=240)).astype(np.float32)
        mask=255*(1-mask)

        img=img.astype(np.float32)

        txt = np.array(txt, dtype=np.uint8)
        txt = cv2.cvtColor(txt, cv2.COLOR_RGB2BGR)
        h,w,c=txt.shape
        s=min(h,w)
        txt=txt[s//4:s*3//4,s//4:s*3//4,:]
        h,w,c=txt.shape
        txt = cv2.resize(txt, dsize=(100, 100))
        h,w,c=txt.shape
        trans = texture_synth1(txt, img,patch_length = min(h,w)//2)
        trans = cv2.cvtColor(trans, cv2.COLOR_BGR2RGB)
        img = blend(img, mask, trans)
        trans[np.where(mask != 255)]=0
        cv2.imwrite(test_dir+"syn.png",trans)
    img = resize(img, long_side_px=512)
    cv2.imwrite(test_dir+"output.png",img)

    ret, dst_data = cv2.imencode('.jpg', img)
    dst_str = base64.b64encode(dst_data)
    return {"response": dst_str}


@app.post('/api/debug') # methodとendpointの指定
async def skechtoimg(files: List[UploadFile] = File(...)):
    img1= Image.open(io.BytesIO(files[0].file.read())).convert('RGB')
    img2= Image.open(io.BytesIO(files[1].file.read())).convert('RGB')
    img1 = np.array(img1, dtype=np.uint8)
    img2 = np.array(img2, dtype=np.uint8)
    w,h,c=img1.shape
    img2.resize(w,h,c)
    alpha=0.5
    img=img1*alpha+img2*(1-alpha)

    ret, dst_data = cv2.imencode('.jpg', img)
    dst_str = base64.b64encode(dst_data)
    return {"response": dst_str}
