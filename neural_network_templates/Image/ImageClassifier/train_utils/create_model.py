# Imports python modules
import torchvision.models

# Imports functions created for this program
from train_utils.get_arch import get_arch
from train_utils.get_classifier import get_classifier


def create_model(arch: str, hidden_units: int) -> torchvision.models:
    # Load pre-trained model based on selected architecture
    model = get_arch(arch)
        
    # Create ower own classifier
    model.classifier = get_classifier(hidden_units)
    
    return model
