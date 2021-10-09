# reclycloth
![demo](/imgs/demo.gif)
## Requirements
- FastAPI

## Getting Started

### Pretrained models
[Download](https://drive.google.com/file/d/1og_9By_xdtnEd9-xawAj4jYbXR6A9deG/view) the models and create the following directories
```
checkpoints/ade20k_smis
checkpoints/cityscapes_smis
checkpoints/deepfashion_smis
```
[Download](https://drive.google.com/file/d/1l7PUB8uAGRyqvZ0ti0ZACoI2CzJxOVoI/view) the model and put in the following directory
```
pretrain/
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
