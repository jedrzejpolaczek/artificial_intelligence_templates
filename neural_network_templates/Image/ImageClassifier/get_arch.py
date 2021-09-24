# Imports python modules
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
