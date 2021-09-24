# Imports python modules
import torch
from torchvision import models


def get_arch(arch: str):
    if arch == 'resnet18':
        model = models.resnet18(pretrained=True)
    if arch == 'alexnet':
        model = models.alexnet(pretrained=True)
    if arch == 'vgg13':
        model = models.vgg13(pretrained=True)
    if arch == 'vgg16':    
        model = models.vgg16(pretrained=True)
    
    return model
        

# Function that loads a checkpoint and rebuilds the model
def load_checkpoint(filepath: str):
    # Solve problem switching between cuda and cpu device
    if torch.cuda.is_available():
        map_location=lambda storage, loc: storage.cuda()
    else:
        map_location='cpu'
    
    # Load checkpoint dict
    checkpoint = torch.load(filepath, map_location=map_location)
    
    # Load model
    model = get_arch(checkpoint['arch'])
        
    for param in model.parameters():
        param.requires_grad = False
        
    model.class_to_idx = checkpoint['class_to_idx']
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['model_state_dict'])
        
    return model
