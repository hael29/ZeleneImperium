from functions import crop_class_dict as cd


def get_supported_crops(dict):
    crops = ""
    for crop in dict:
        crops += f'{crop}, '
    return crops[:-2]


print(get_supported_crops(cd))