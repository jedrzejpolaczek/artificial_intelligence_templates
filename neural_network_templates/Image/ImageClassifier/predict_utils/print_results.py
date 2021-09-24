# Imports python modules
import json


def print_results(top_p: list, top_class: list, category_names: str):
    # Load classes classifier will use
    with open(category_names, 'r') as f:
        cat_to_name = json.load(f)
        
    index = 0
    for elem in top_class:
        print(f"Flower: {cat_to_name[str(int(elem))]} : {top_p[index]*100:.0f}%")
        index += 1
