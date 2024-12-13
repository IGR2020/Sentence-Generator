import csv
import json
import pickle
from os import listdir
from os.path import isfile
import pygame as pg


def loadAssets(path, scale=1, size=None) -> dict[str, pg.Surface]:
    assets = {}
    for file in listdir(path):
        if not isfile(f"{path}/{file}"):
            continue
        if size is None:
            assets[file.replace(".png", "")] = pg.transform.scale_by(pg.image.load(f"{path}/{file}"), scale)
            continue
        assets[file.replace(".png", "")] = pg.transform.scale(
            pg.transform.scale_by(pg.image.load(f"{path}/{file}"), scale), size)
    return assets


def loadFileAndConvert(path):
    data = None
    if ".csv" in path:
        data = loadCsvData(path)
    elif ".json" in path:
        data = loadJsonData(path)
    elif ".pkl" in path:
        data = loadPickleData(path)
    else:
        data = loadTextData(path)
    return extractStrings(data)

def loadTextData(path):
    with open(path, "r") as file:
        data = file.read()
        file.close()
    return data

def loadJsonData(path):
    with open(path, "r") as file:
        data = json.load(file)
        file.close()
    return data

def loadPickleData(file):
    with open(file, "rb") as file:
        data = pickle.load(file)
        file.close()
    return data

def loadCsvData(path):
    with open(path, "r") as file:
        data = csv.reader(file)
        data = [word for word in data]
        file.close()
    return data

def extractStrings(data):
    strings = []
    if isinstance(data, str):
        strings += data.split()

    elif isinstance(data, list):

        for val in data:
            strings += extractStrings(val)

    elif isinstance(data, dict):

        for val in data:
            strings += extractStrings(data[val])

    return strings