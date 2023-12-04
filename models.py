import torchvision.models as tvm
import torch
from abc import ABC, abstractmethod
from pipelines import Classic_Pipeline, CLIP_Pipeline

from constants import *

def a_or_an(word):
    vowels = "aeiouy"
    if word[0] in vowels:
        return "an"
    return "a"


def generate_text_lst(classes, image_noun):
    if not image_noun: return classes
    out = []
    for c in classes:
        out.append(f"{a_or_an(image_noun)} {image_noun} of {a_or_an(c)} {c}")
    print(f"Sample label: {out[0]}")
    return out


def get_label_text_lst(dataset, extensions=None, image_noun=None, prefix_mod="", suffix_mod=""):
    if dataset == "cifar10":
        text_lst = [prefix_mod + x + suffix_mod for x in CIFAR10_LABELS_TEXT]
    elif dataset == "imagenet":
        text_lst = [prefix_mod + x + suffix_mod for x in IMAGENET_LABELS_TEXT]
    else:
        raise Exception("Unknown dataset.")

    if extensions:
        text_lst += [prefix_mod + x + suffix_mod for x in extensions]
    return generate_text_lst(text_lst, image_noun)


def get_pipeline(model_name, dataset_name, use_clip, label_noun=None, extensions=None,
                 prefix_mod="", suffix_mod=""):
    if use_clip:
        label_texts = get_label_text_lst(dataset_name, extensions, label_noun, prefix_mod, suffix_mod)
        return CLIP_Pipeline(model_name, label_texts)
    else:
        return Classic_Pipeline(model_name, dataset_name)


if __name__ == "__main__":
    pipeline = get_pipeline("clip", "CIFAR10")
    print(pipeline)