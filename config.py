#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:23:52 2015

@author: pavel
"""

## Window
WINDOW_SIZE = (780, 300)
BACKGROUND_COLOR = (100, 100, 100)


# MusicBoard
WHITE_KEY_IMG_PATH = "./gui/white_.png"
WHITE_KEY_PRESSED_IMG_PATH = "./gui/white_pressed.png"
BLACK_KEY_IMG_PATH = "./gui/black_.png"
BLACK_KEY_PRESSED_IMG_PATH = "./gui/black_pressed.png"

VOL_UP_IMG_PATH = "./gui/volume_up.png"
VOL_UP_PRESSED_IMG_PATH = "./gui/volume_up_pressed.png"
VOL_DOWN_IMG_PATH = "./gui/volume_down.png"
VOL_DOWN_PRESSED_IMG_PATH = "./gui/volume_down_pressed.png"

OCTAVE_UP_IMG_PATH = "./gui/treble.png"
OCTAVE_UP_PRESSED_IMG_PATH = "./gui/treble_pressed.png"
OCTAVE_DOWN_IMG_PATH = "./gui/bass.png"
OCTAVE_DOWN_PRESSED_IMG_PATH = "./gui/bass_pressed.png"

NEXT_TONE_IMG_PATH = "./gui/next_.png"
NEXT_TONE_PRESSED_IMG_PATH = "./gui/next_pressed.png"

UP_LEFT_KEYS_POSITION = (0,0)
HORIZONTAL_PADDING = 1

START_OCTAVE = 3
NUM_OCTAVES_SHOW = 2
OCTAVE_MIN = 0
OCTAVE_MAX = 8

WHITE_BUTTONS_MAP = [24, 25, 26, 27, 28,29, 30, 52, 53, 54, 55, 56, 57, 58]
BLACK_BUTTONS_MAP = [11, 12, 14, 15, 16, 39, 40, 42, 43, 44]
CONTROL_BUTTONS_MAP = {"octave_up":114, "octave_down":113,
                       "volume_up":111, "volume_down":116,
                       "sound_type":65}

MAX_VOLUME = 1.0
MIN_VOLUME = 0.0
DEFAULT_VOLUME = 0.8
VOLUME_STEP = 0.1