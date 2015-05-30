#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:04:53 2015

@author: pavel
"""
from sys import argv
import pygame

import tones, config, control


class Button(object):    
    def __init__(self, screen, img, img_pressed, pos_x, pos_y):
        self._screen = screen        
        
        self.pos = (pos_x, pos_y)        

        self.img = img
        self.img_pressed = img_pressed

        self.rect = self.img.get_rect() 
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.is_pressed = False
        self.is_visible = True
        
               
    def render(self):              
        if self.is_visible:
            if self.is_pressed:
                self._screen.blit(self.img_pressed, self.pos) 
            else:
                self._screen.blit(self.img, self.pos) 
        
    def do_action(self, *args):
        raise NotImplemented
    def stop_action(self, *args):
        raise NotImplemented
        
    def press(self, *args)  :
        if not self.is_pressed:
            self.is_pressed = True
            self.do_action(*args)
    def unpress(self, *args):
        if self.is_pressed:
            self.is_pressed = False
            self.stop_action(self, *args)

    def get_rectangle(self):
        return self.rect


class MusicButton(Button):
    def __init__(self, screen, img, img_pressed, pos_x, pos_y, play_funct,
                 stop_playing_funct, relative_octave, note):
        super(MusicButton, self).__init__(screen, img, img_pressed, pos_x, pos_y)
        
        self.play_function = play_funct
        self.stop_playing_function = stop_playing_funct
        self.relative_octave = relative_octave
        self.note = note
        #self.octave = None
        
    def do_action(self, *args):
        self.play_function(self.relative_octave, self.note)

    def  stop_action(self, *args):
        self.stop_playing_function(self.relative_octave, self.note)
        

class ControlButton(Button):
    def __init__(self, screen, img, img_pressed, pos_x, pos_y, on_press_funct,
                 on_release_funct = None, name=""):
        super(ControlButton, self).__init__(screen, img, img_pressed, pos_x, pos_y)
        self.on_press = on_press_funct
        self.on_release = on_release_funct
        self.name = name             
    def do_action(self, *args):
        self.on_press(*args)
    def stop_action(self, *args):
        if self.on_release is not None:
            self.on_release(*args)
    
        
class  MusicBoard():    
    DEFAULT_DURATION = tones.Tone.DURATION.LONG
    DEFAULT_SOUND_TYPE = tones.Tone.SOUND_TYPES.DECAYED

    
    def __init__(self, screen):
        self._screen = screen
        self.toneManager = tones.Tone()
        
        self.start_octave =  config.START_OCTAVE
        self.duration =  MusicBoard.DEFAULT_DURATION
        self.sound_type =  MusicBoard.DEFAULT_SOUND_TYPE
        self.volume = config.DEFAULT_VOLUME
        
        down_right_pos = self._init_music_buttons_(config.UP_LEFT_KEYS_POSITION) 
        self._init_control_buttons_(down_right_pos)
        self._init_controllers_()            
                
        
        self. need_to_render = True        

        
    def _init_music_buttons_(self, up_left_position):
        self.white_buttons = []
        self.black_buttons = []
        
        white_button_img = pygame.image.load( config.WHITE_KEY_IMG_PATH)
        white_button_pr_img = pygame.image.load( config.WHITE_KEY_PRESSED_IMG_PATH)
        black_button_img = pygame.image.load( config.BLACK_KEY_IMG_PATH)
        black_button_pr_img = pygame.image.load( config.BLACK_KEY_PRESSED_IMG_PATH)
        
        white_size = white_button_img.get_rect().size
        white_width = white_size[0]
        white_height = white_size[1]
        
        x_position, y_position = up_left_position
        for octave in range( config.NUM_OCTAVES_SHOW):
            for i in range( tones.NOTES.NUM_WHITE_NOTES):
                w_mb = MusicButton(self._screen, white_button_img, white_button_pr_img, 
                                   x_position, y_position,
                                   self.play_note, self.stop_playing, 
                                   octave, tones.NOTES.WHITE_NOTES[i])
                self.white_buttons.append(w_mb) 
                
                
                if tones.NOTES.BLACK_NOTES_N[i] is not None:  
                    b_mb = MusicButton(self._screen, black_button_img, black_button_pr_img, 
                             x_position + white_width/2, y_position,
                             self.play_note, self.stop_playing,
                             octave, tones.NOTES.BLACK_NOTES_N[i])
                    self.black_buttons.append(b_mb) 
                    
                x_position += white_width + config.HORIZONTAL_PADDING
        
        down_right_position = (x_position, white_height)       
        return down_right_position
    
    def _init_control_buttons_(self, down_left_position):
        self.control_buttons = []       
        
        
        def create_button(img_path, img_pressed_path, (x_left, y_down), *args, **kwargs):
            img = pygame.image.load(img_path)
            img_pr = pygame.image.load(img_pressed_path)
            size = img.get_rect().size           
            
            x_right = x_left + size[0]
            y_up = y_down - size[1]
            
            
            button = ControlButton(self._screen, img, img_pr, 
                                   x_left, y_up, *args, **kwargs)
            
            return button, (x_left, y_up, x_right, y_down)
            
        pos_next_type = down_left_position
        next_type, (xl, yu, xr, yd) = create_button(config.NEXT_TONE_IMG_PATH,
                                    config.NEXT_TONE_PRESSED_IMG_PATH, pos_next_type,
                                    self.change_sound_type, name = "sound_type")

        pos_oct_d = (xl, yu-config.HORIZONTAL_PADDING)
        octave_down, (xl, yu, xr, yd) = create_button(config.OCTAVE_DOWN_IMG_PATH,
                                    config.OCTAVE_DOWN_PRESSED_IMG_PATH, pos_oct_d,
                                    self.octave_down, name = "octave_down")
                                    
        pos_vol_d = (xr + config.HORIZONTAL_PADDING,yd )          
        vol_down, (xl, yu, xr, yd) = create_button(config.VOL_DOWN_IMG_PATH,
                                    config.VOL_DOWN_PRESSED_IMG_PATH,pos_vol_d,
                                    self.volume_down, name = "volume_down")
                                    
        pos_vol_u = (xl, yu-config.HORIZONTAL_PADDING) 
        pos_oct_u = (xr + config.HORIZONTAL_PADDING,yd )

        vol_up, (xl, yu, xr, yd) = create_button(config.VOL_UP_IMG_PATH,
                                    config.VOL_UP_PRESSED_IMG_PATH,pos_vol_u,
                                    self.volume_up, name = "volume_up")  
        
        
        octave_up, (xl, yu, xr, yd) = create_button(config.OCTAVE_UP_IMG_PATH,
                                    config.OCTAVE_UP_PRESSED_IMG_PATH,
                                    pos_oct_u, self.octave_up, name = "octave_up")
                                    
        self.control_buttons.append(next_type)                            
        self.control_buttons.append(octave_down)
        self.control_buttons.append(vol_down)
        self.control_buttons.append(vol_up)
        self.control_buttons.append(octave_up)
        
   
    def _init_controllers_(self):
        self.keyboard = control.KeyBoard()
        self.mouse = control.Mouse()
        
        self.keyboard.add_mult_keys_obj(config.WHITE_BUTTONS_MAP, self.white_buttons, "press", "unpress")
        self.keyboard.add_mult_keys_obj(config.BLACK_BUTTONS_MAP, self.black_buttons, "press", "unpress")  
        
        control_buttons_map = [config.CONTROL_BUTTONS_MAP.get(button.name, 0) for button in self.control_buttons ]
        
        self.keyboard.add_mult_keys_obj(control_buttons_map, self.control_buttons,"press", "unpress")
        
        self.mouse.add_mult_obj(self.black_buttons, 0)
        self.mouse.add_mult_obj(self.white_buttons, 1)
        self.mouse.add_mult_obj(self.control_buttons, 2)
        
        
    def on_render(self):        
        self.need_to_render = False
        for button in self.white_buttons:
            button.render()
        for button in self.black_buttons:
            button.render()
        for button in self.control_buttons:
            button.render()
    def on_event(self, event):
        #print event        
        if event.type == pygame.ACTIVEEVENT:
            pass
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            self.mouse.on_move(event.pos, self.start_octave, self.duration, self.sound_type)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse.on_button_down(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse.on_button_up(event.pos)
            
        elif event.type == pygame.KEYDOWN:
            print event.scancode
            self.keyboard.on_key_down(event.scancode, self.start_octave, self.duration, self.sound_type)
            
        elif event.type == pygame.KEYUP:
            self.keyboard.on_key_up(event.scancode)            
        self.need_to_render = True

    def play_note(self, relative_octave, note):
        octave = self.start_octave + relative_octave
        self.toneManager.play_note(note, octave,self.sound_type, 
                                   self.duration, self.volume)
    def stop_playing(self, relative_octave, note):
        octave = self.start_octave + relative_octave
        self.toneManager.stop_play_note(octave, note, self.sound_type)
        
    def octave_up(self, *args):
        self.start_octave = min(config.OCTAVE_MAX-config.NUM_OCTAVES_SHOW + 1,
                                self.start_octave + 1)
    def octave_down(self, *args):
        self.start_octave = max(config.OCTAVE_MIN, self.start_octave - 1)
    def volume_down(self, *args):
        self.volume = max(config.MIN_VOLUME, self.volume - config.VOLUME_STEP)
    def volume_up(self, *args):
        self.volume = min(config.MAX_VOLUME, self.volume + config.VOLUME_STEP)
    def change_sound_type(self, *args):
        self.sound_type = tones.Tone.SOUND_TYPES.next_type(self.sound_type)
        
class App:
    def __init__(self):
        self._running = False
        self._screen = None
        self._background = None
        self._size = self._width, self._height = config.WINDOW_SIZE
        
    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self._size)
        pygame.display.set_caption('Basic Pygame program')
        
        self._background = pygame.Surface(self._size).convert()	
        self._background.fill(config.BACKGROUND_COLOR)
        
        self._running = True
        
        self.keyboard =  MusicBoard(self._screen)
        
    def on_event(self, event):
        
        if event.type == pygame.QUIT:
            self._running = False
        else:
            self.keyboard.on_event(event)
            
    def on_loop(self):
        pass
        
    def on_render(self):
        if self.keyboard.need_to_render:            
            self._screen.blit(self._background, (0,0))             
            self.keyboard.on_render()
            
            pygame.display.flip()
        
    def on_cleanup(self):
        pygame.quit()
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.time.wait(5)
        self.on_cleanup()

def main(arg):
    print argv
    
    
if __name__ == "__main__":   
    theApp = App()
    theApp.on_execute()
     #main(argv)
