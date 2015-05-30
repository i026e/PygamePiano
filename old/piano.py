#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:04:53 2015

@author: pavel
"""
from sys import argv
import pygame
from gi.repository import Gtk

import os.path
import sys

#import pygtk
#pygtk.require("2.0")


class CONST:
        NOTES = ['C', 'C#', 'D', 'D#','E', 'F', 'F#','G','G#', 'A', 'A#', 'B']
        DURATION_SHORT = 1
        DURATION_MEDIUM = 2
        DURATION_LONG = 3
        OCTAVE_MIN = 0
        OCTAVE_MAX = 8

class MySound:  
    #directories
    DIRECTORY = "notes"
    EXT = ".wav"
    DURATIONS = {CONST.DURATION_SHORT:"0.5", 
                 CONST.DURATION_MEDIUM:"1", 
                 CONST.DURATION_LONG:"3"}

    PATHES = {}
    for octave in range(CONST.OCTAVE_MIN, CONST.OCTAVE_MAX+1):
        PATHES[octave] = {}
        for dur in DURATIONS:
            PATHES[octave][dur] = {}
            for n in CONST.NOTES:
                path = os.path.join(DIRECTORY,DURATIONS[dur],n+str(octave)+EXT)
                if os.path.exists(path):
                    PATHES[octave][dur][n] = path
    print PATHES

    def __init__(self):
        pygame.init()
        #self.snd.read('elka.wav')
    
    def playNote(self, note, octave, duration):
        if octave in MySound.PATHES:
            if duration in MySound.PATHES[octave]:
                if note in MySound.PATHES[octave][duration]:
                    path = MySound.PATHES[octave][duration][note]
                    print(path)
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()


class Board(object):    
    sound = MySound()

    def __init__(self, buttonToToneMap={}, buttonToFuncMap={}):
        #buttonToToneMap dictionary of key_name:(note, shift_from_start_octave)
        ##buttonFuncMap dictionary of key_name:func_name
        self.buttonMap = buttonToToneMap
        self.funcMap = buttonToFuncMap
        Board.duration = CONST.DURATION_MEDIUM
        Board.start_octave = 3
        
    def pressKey(self, key):
        if key in self.buttonMap:
            self.pressMusicKey(key)
        else:
            self.pressFuncKey(key)

    def pressMusicKey(self, key):        
        note, shift = self.buttonMap.get(key,(None, None))
        if not( note is None or shift is None):
            octave = Board.start_octave + shift
            Board.sound.playNote(note, octave, Board.duration)
    
    def pressFuncKey(self, key):        
        if key in self.funcMap:
            self.funcMap[key]()
    
    def up_octave(self):
        if Board.start_octave < CONST.OCTAVE_MAX:
            Board.start_octave += 1
    def down_octave(self):
        if Board.start_octave > CONST.OCTAVE_MIN:
            Board.start_octave -= 1
    def incr_duration(self):
        if Board.duration == CONST.DURATION_SHORT:
            Board.duration = CONST.DURATION_MEDIUM
        elif Board.duration == CONST.DURATION_MEDIUM:
            Board.duration = CONST.DURATION_LONG
    def decr_duration(self):        
        if Board.duration == CONST.DURATION_LONG:
            Board.duration = CONST.DURATION_MEDIUM
        elif Board.duration == CONST.DURATION_MEDIUM:
            Board.duration = CONST.DURATION_SHORT
        


class MusicBoard(Board):    
    def __init__(self):
        num_octaves = 2
        start_kbd_index = 1
        label_pattern = '{note}_{ind}'

        lables={}
        for note in CONST.NOTES:
            for shift in range(num_octaves):
                label = label_pattern.format(note=note,
                                                  ind= start_kbd_index+shift)
                lables[label] = (note, shift)
        super(MusicBoard, self).__init__(buttonToToneMap=lables)
    def highlight(self, note, shift):
        pass

class KeyBoard(Board):  
    
    def __init__(self):
        class codes:
            left_Ctrl = 65507
            right_Ctrl = 65508
            left_Alt = 65513
            right_Alt = 65514                       
        
        funcKeys = {
            codes.left_Ctrl:self.down_octave, 
            codes.right_Ctrl:self.up_octave,
            codes.left_Alt:self.decr_duration, 
            codes.right_Alt:self.incr_duration, 
        }
        
        first_octave = "q2w3er5t6y7u"
        second_octave = "zsxdcvgbhnjm"
        
        noteKeys = {}
        for i in range(len(CONST.NOTES)):
            small_first = ord(first_octave[i])
            capital_first = ord(first_octave[i].upper())
            
            small_second = ord(second_octave[i])
            capital_second = ord(second_octave[i].upper())
            
            noteKeys[small_first] = noteKeys[capital_first] = (CONST.NOTES[i], 0)
            noteKeys[small_second] = noteKeys[capital_second] = (CONST.NOTES[i], 1)
            
        
        
        super(KeyBoard, self).__init__(buttonToToneMap=noteKeys, buttonToFuncMap=funcKeys)


class Handler:
    def __init__(self, musicBoard, keyBoard):
        self.musicBoard = musicBoard
        self.keyBoard = keyBoard
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, widget, *args):
        #print(dir(button))
        if widget.get_name() == 'GtkLabel':
            print(widget.get_label())
            self.musicBoard.pressMusicKey(widget.get_label())

    def onButtonClicked(self, widget, *args):
        print(widget)
        pass
    def onButtonReleased(self, widget, *args):
        pass
        #print(widget)
        #data = args[0]
        #print(data.state)
    def onKeyPressed(self, widget, *args):
        #print(widget)
        data = args[0]
        if data:
            self.keyBoard.pressKey(data.keyval)
            print(data.keyval)
    def onKeyReleased(self, widget, *args):
        #print(widget)
        #data = args[0]
        #print(data.keyval)
        pass


class PianoGTK:
    """This is an Hello World GTK application"""

    def __init__(self):
        #Set the Glade file
        self.gladefile = "gui/piano.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)

        mboard = MusicBoard()
        kboard = KeyBoard()

        self.glade.connect_signals(Handler(mboard, kboard))


        self.glade.get_object("MainWindow").show_all()

    def on_MainWindow_delete_event(self, widget, event):
        Gtk.main_quit()


def main(arg):
    #print argv
    hwg = PianoGTK()
    Gtk.main()
if __name__ == "__main__":
    main(argv)
