import torchvision
import cv2
import torch
import numpy as np

from options.test_options import TestOptions
from models.smis_model import SmisModel
opt = TestOptions()
opt.aspect_ratio=1.0
opt.batchSize=4
opt.cache_filelist_read=False
opt.cache_filelist_write=False
opt.checkpoints_dir='./checkpoints'
opt.clean_code=False
opt.contain_dontcare_label=False
opt.crop_size=256
opt.dataroot='./test1'
opt.dataset_mode='deepfashion'
opt.display_winsize=256
opt.gpu_ids=[0]
opt.how_many=float("inf")
opt.init_type='xavier'
opt.init_variance=0.02
opt.isTrain=False
opt.label_nc=8
opt.load_from_opt_file=False
opt.load_size=256
opt.max_dataset_size=9223372036854775807
opt.model='smis'
opt.nThreads=0
opt.name='deepfashion_smis'
opt.nef=16
opt.netE='conv'
opt.netG='deepfashion'
opt.ngf=160
opt.no_flip=True
opt.no_instance=True
opt.no_pairing_check=False
opt.no_spectral=False
opt.norm_D='spectralinstance'
opt.norm_E='spectralinstance'
opt.norm_G='spectralspadesyncbatch3x3'
opt.num_upsampling_layers='more'
opt.output_nc=3
opt.phase='test'
opt.preprocess_mode='resize_and_crop'
opt.resnet_n_downsample=3
opt.results_dir='./results/'
opt.semantic_nc=8
opt.serial_batches=True
opt.test_mask=-1
opt.test_times=1
opt.test_type='visual'
opt.use_vae=True
opt.vgg_path=''
opt.which_epoch='latest'
opt.z_dim=256
opt.gpu_ids=[0]
opt.netG="deepfashion"
opt.ngf=160
opt.num_upsampling_layers="more"
opt.batchSize=4
opt.name="deepfashion_smis"
from change_color import color2gray,gray2color

model = SmisModel(opt)
model.eval()


def mask2img(mask_cv2):
    mask = torch.from_numpy(mask_cv2.astype(np.float32)).clone()
    mask=mask.permute(2,0,1)
    mask=torch.unsqueeze(mask,0)
    data={'label':mask, 'instance':mask, 'image':mask, 'path':"test.png"}
    #img=model.test(mask)
    img = model(data, mode='inference')
    print(img[0].shape)
    img=img[0][0]
    print(img.max())
    #torchvision.utils.save_image(img,"test.png")
    img=img.permute(1,2,0)
    img = img.to('cpu').detach().numpy().copy()
    img=(img*255)
    img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

if __name__ == '__main__':
    img=cv2.imread("input.png")
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img=color2gray(img)
    #cv2.imwrite("apple2.png",gray2color(img))
    img=mask2img(img)
    cv2.imwrite("apple.png",img)

