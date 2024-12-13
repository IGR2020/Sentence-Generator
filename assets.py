import pygame as pg

from loader import loadAssets

assets: dict[str, pg.Surface] = {}
assets.update(loadAssets("Assets/GUI"))

fontLocation = "Assets/Fonts/"