#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 08:21:11 2015

@author: pavel
"""

import os.path
import pygame.mixer

from sounds_generator import generate_full_period_wave




class Tone:    
    BASE_DIRECTORY = "notes/base"
    DECAY_DIRECTORY = "notes/decay"
    EXT = ".wav"
    
    class DURATION:
        INF = 0
        LONG = 3000
        MEDIUM=1000
        SHORT=300
    class SOUND_TYPES:        
        BASE=0
        DECAYED=1
        
        NUM_TYPES = 2
        
        @staticmethod
        def next_type(current_type):
            return (current_type + 1)% Tone.SOUND_TYPES.NUM_TYPES
    
   
    def __init__(self):
        if not os.path.exists(Tone.BASE_DIRECTORY) or not os.path.exists(Tone.DECAY_DIRECTORY):
            
            _genrate_sounds_()
            
        pygame.mixer.init()
        self._init_sounds_()
    def _init_sounds_(self):
        self.sounds = {Tone.SOUND_TYPES.BASE:{}, Tone.SOUND_TYPES.DECAYED:{}}
        
        for octave in range(NOTES.OCTAVE_MIN, NOTES.OCTAVE_MAX+1):
            self.sounds[Tone.SOUND_TYPES.BASE][octave] = {}
            self.sounds[Tone.SOUND_TYPES.DECAYED][octave] = {}
            for note in NOTES.NOTES:
                base_sound_path, decay_sound_path = self._get_paths_(note, octave)                
                if os.path.exists(base_sound_path):
                    self.sounds[Tone.SOUND_TYPES.BASE][octave][note] = pygame.mixer.Sound(base_sound_path)
                if os.path.exists(decay_sound_path):
                    self.sounds[Tone.SOUND_TYPES.DECAYED][octave][note] = pygame.mixer.Sound(decay_sound_path)
    @staticmethod
    def _get_paths_(note, octave):
        base_sound_path = os.path.join(Tone.BASE_DIRECTORY,
                                        note+str(octave)+Tone.EXT)
        decay_sound_path = os.path.join(Tone.DECAY_DIRECTORY,
                                        note+str(octave)+Tone.EXT)
        return base_sound_path, decay_sound_path
    

    def _get_sound_(self, note, octave, sound_type):
        if sound_type in self.sounds:
            if octave in self.sounds[sound_type]:
                if note in self.sounds[sound_type][octave]:
                    return self.sounds[sound_type][octave][note]


    def play_note(self, note, octave, sound_type, fade_duration, volume=.8):
        sound = self._get_sound_(note, octave, sound_type)
        if sound is not None:
            sound.stop()
            sound.set_volume(volume)
            
            if sound_type == Tone.SOUND_TYPES.BASE:
                sound.play(loops = -1)
                if fade_duration != Tone.DURATION.INF:
                    sound.fadeout(fade_duration)
                
            else:
                sound.play()
            
            
            
            
                
    def stop_play_note(self, note, octave, sound_type):
        if sound_type == Tone.SOUND_TYPES.BASE:
            sound = self._get_sound_(note, octave,sound_type)            
            if sound is not None:
                #pygame.mixer.pause()
                sound.fadeout(Tone.DURATION.LONG)
                #decay_sound.play()
            
    




class NOTES:
    NOTES = ['C', 'C#', 'D', 'D#','E', 'F', 'F#','G','G#', 'A', 'A#', 'B']
    WHITE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    BLACK_NOTES_N = [ 'C#',  'D#', None, 'F#','G#', 'A#', None]
    BLACK_NOTES = [ 'C#',  'D#', 'F#','G#', 'A#']
    NUM_WHITE_NOTES = 7
    NUM_BLACK_NOTES = 5

    OCTAVE_MIN = 0
    OCTAVE_MAX = 8

    DURATIONS = {}
    FREQS = {0:{'C':16.35, 'C#':17.32,'D':18.35, 'D#':19.45,'E':20.6,'F':21.83,'F#':23.12,'G':24.5,'G#':25.96, 'A':27.5, 'A#':29.14, 'B':30.87},
    1:{'C':32.7, 'C#':34.65, 'D':36.71, 'D#':38.89, 'E':41.2, 'F':43.65, 'F#':46.25, 'G':49.0, 'G#':51.91, 'A':55.0, 'A#':58.27, 'B':61.74},
    2:{'C':65.41, 'C#':69.3, 'D':73.42, 'D#':77.78, 'E':82.41, 'F':87.31, 'F#':92.5, 'G':98.0, 'G#':103.83, 'A':110.0, 'A#':116.54, 'B':123.47},
    3:{'C':130.81, 'C#':138.59, 'D':146.83, 'D#':155.56, 'E':164.81, 'F':174.61, 'F#':185.0, 'G':196.0, 'G#':207.65, 'A':220.0, 'A#':233.08, 'B':246.94},
    4:{'C':261.63, 'C#':277.18, 'D':293.66, 'D#':311.13, 'E':329.63, 'F':349.23, 'F#':369.99, 'G':392.0, 'G#':415.3, 'A':440.0, 'A#':466.16, 'B':493.88},
    5:{'C':523.25, 'C#':554.37, 'D':587.33, 'D#':622.25, 'E':659.25, 'F':698.46, 'F#':739.99, 'G':783.99, 'G#':830.61, 'A':880.0, 'A#':932.33, 'B':987.77},
    6:{'C':1046.5, 'C#':1108.73, 'D':1174.66, 'D#':1244.51, 'E':1318.51, 'F':1396.91, 'F#':1479.98, 'G':1567.98, 'G#':1661.22, 'A':1760.0, 'A#':1864.66, 'B':1975.53},
    7:{'C':2093.0, 'C#':2217.46, 'D':2349.32, 'D#':2489.02, 'E':2637.02, 'F':2793.83, 'F#':2959.96, 'G':3135.96, 'G#':3322.44, 'A':3520.0, 'A#':3729.31, 'B':3951.07},
    8:{'C':4186.01, 'C#':4434.92, 'D':4698.63, 'D#':4978.03, 'E':5274.04, 'F':5587.65, 'F#':5919.91, 'G':6271.93, 'G#':6644.88, 'A':7040.0, 'A#':7458.62, 'B':7902.13}}


def _genrate_sounds_():
    print "generating sounds..."
    
    total = len(NOTES.FREQS)
    
        
    for octave,notes in NOTES.FREQS.items():
        print "...%d%%..." %( octave*100/total)
        for note,freq in notes.items():
            base_sound_path, decay_sound_path = Tone._get_paths_(note, octave)
            generate_full_period_wave(round(freq), base_sound_path, False)
            generate_full_period_wave(round(freq), decay_sound_path, True)
    print "...100%"            
if __name__ == "__main__":    
    #_genrate_sounds_()
    pass