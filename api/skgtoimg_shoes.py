import torch
import torchvision
from utils import transforms as custom_transforms
from train import gen_input, rand_between, gen_input_rand
from utils.visualize import vis_patch, vis_image
import numpy as np
import cv2 
color_space = 'lab'
from main import get_transforms
from argparser import parse_arguments
command = '--display_port 77'
args = parse_arguments(command.split())
args.image_size =152
args.resize_max = 256
args.resize_min = 256
transform = get_transforms(args)
from models import texturegan,discriminator
from torch.autograd import Variable
model_location="./model/shoes.pth"
txt_size=20

def load_network(model, save_path):

    model_state = torch.load(save_path)

    if "state_dict" in model_state:
        model.load_state_dict(model_state["state_dict"])
    else:
        model.load_state_dict(model_state)

        model_state = {
            'state_dict': model.cpu().state_dict(),
            'epoch': epoch,
            'iteration': iteration,
            'model': args.model,
            'color_space': args.color_space,
            'batch_size': args.batch_size,
            'dataset': dataset,
            'image_size': args.image_size
        }

    model.cuda()


#change to your location

netG = texturegan.TextureGAN(5, 3, 32)
load_network(netG, model_location)

netG.eval()
def get_input(skg, seg, eroded_seg, txt):
    bs, w, h = seg.size()
    seg = seg.view(bs, 1, w, h)
    seg = torch.cat((seg, seg, seg), 1)
    eroded_seg = eroded_seg.view(bs, 1, w, h)
    eroded_seg = torch.cat((eroded_seg, eroded_seg, eroded_seg), 1)

    temp = torch.ones(seg.size()) * (1 - seg.float()).float()
    temp[:, 1, :, :] = 0
    temp[:, 2, :, :] = 0

    txt = txt.float() * seg.float() + temp

    inp, texture_loc = gen_input_rand(txt, skg, eroded_seg[:, 0, :, :] * 100,txt_size,txt_size,1)
    return inp,texture_loc

def get_inputv(inp):
    input_stack = torch.FloatTensor().cuda()
    input_stack.resize_as_(inp.float()).copy_(inp)
    inputv = Variable(input_stack)
    return inputv

def pil_loader(path):
    # open path as file to avoid ResourceWarning
    # (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        print(f)
        with Image.open(f) as img:
            return img.convert('RGB')

color_space = 'lab'

from utils import transforms as custom_transforms

from PIL import Image
def skech2img_shoes(skg,seg,txt):
    #skg=pil_loader("skg.jpg")
    #txt=pil_loader("txt.jpg")
    #seg=pil_loader("seg.jpg")
    #eroded_seg=Image.open("eroded_seg.jpg")

    skg, seg, txt = transform([skg, seg, txt])
    eroded_seg = seg

    skg=skg.unsqueeze(0)
    seg=seg.unsqueeze(0)
    txt=txt.unsqueeze(0)
    eroded_seg=eroded_seg.unsqueeze(0)



    skg = custom_transforms.normalize_lab(skg)
    txt = custom_transforms.normalize_lab(txt)
    seg = custom_transforms.normalize_seg(seg)
    eroded_seg = custom_transforms.normalize_seg(eroded_seg)

    inp,texture_loc = get_input(skg, seg, eroded_seg, txt)

    seg = seg!=0

    model = netG

    inpv = get_inputv(inp.cuda())
    output = model(inpv.cuda())

    out_img = vis_image(custom_transforms.denormalize_lab(output.data.double().cpu()),
                                        color_space)
    inp_img = vis_patch(custom_transforms.denormalize_lab(txt.cpu()),
                                custom_transforms.denormalize_lab(skg.cpu()),
                                texture_loc,
                                color_space)

    c=(np.transpose(out_img[0],(1, 2, 0))*255).astype(np.uint8)
    return c
