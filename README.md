# reclycloth
[SLIDES and VIDEO](https://drive.google.com/drive/folders/1oeLI2vDESiZ2I11qH6NPFbnLGIcn3LNa?usp=sharing)

**Hack Aichi 2021 - 2nd Place**

**Theme:** sustainble fashion

This project's functions include:
- Replace the top part's texture with the selected one
- Generate objects from sketches and replace their textures with the selected one
- Generate images from semantic segmentation using semantic manipulation, and change the top part's texture with the selected one
![demo](/imgs/demo.gif)
## Requirements
- FastAPI

## Getting Started

### Pretrained models
[Download](https://drive.google.com/file/d/1og_9By_xdtnEd9-xawAj4jYbXR6A9deG/view) the models and create the following directories ([original repository](https://github.com/Seanseattle/SMIS))
```
api/checkpoints/ade20k_smis
api/checkpoints/cityscapes_smis
api/checkpoints/deepfashion_smis
```
[Download](https://drive.google.com/file/d/1l7PUB8uAGRyqvZ0ti0ZACoI2CzJxOVoI/view) the model and put in the following directory ([original repository](https://github.com/anish9/Fashion-AI-segmentation))
```
api/pretrain/
```

### Run API
Go to dir `api/` and run the following command
```
uvicorn api:app
```

Then run `index.html` on local server

## Result

### From photo
![sample1](/imgs/sample1.JPG)
### From sketch
![sample1](/imgs/sample2.JPG)
![sample1](/imgs/sample3.JPG)

### From semantic segmentation image
![sample1](/imgs/sample4.JPG)
