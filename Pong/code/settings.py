import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
SIZE = {'paddle': (40,100), 'ball': (30,30)}
POS = {'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 'opponent': (50, WINDOW_HEIGHT / 2)}
SPEED = {'player': 550, 'opponent': 450, 'ball': 600}
COLORS = {
    'paddle': "#ffffff",
    'paddle shadow': '#b12521',
    'ball': "#c5ff08",
    'ball shadow': '#c14f24',
    'bg': "#044E07",
    'bg detail': "#ffffff"
}