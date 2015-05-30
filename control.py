#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 14:21:35 2015

@author: pavel
"""
class KeyBoard():
    def __init__(self):
        self.key_mapping = {}
    def add_key(self, scancode, func_down, func_up):
        self.key_mapping[scancode] = (func_down, func_up)
        
    def add_key_obj(self, scancode, obj, func_down_name, func_up_name):
        func_down = getattr(obj, func_down_name)
        func_up = getattr(obj, func_up_name)
        self.add_key(scancode, func_down, func_up)
        
    def add_mult_keys(self, scancode_list, func_down_list, func_up_list):
        length = min(len(scancode_list), len(func_down_list), len(func_up_list))
        for i in range(length):
            self.add_key(scancode_list[i], func_down_list[i], func_up_list[i])
    def add_mult_keys_obj(self, scancode_list, obj_list, func_down_name, func_up_name):
        for i in range(min(len(scancode_list), len(obj_list))):
            self.add_key_obj(scancode_list[i], obj_list[i], func_down_name, func_up_name)
            
    def on_key_down(self, scancode, *params):
        if scancode in self.key_mapping:
            self.key_mapping[scancode][0](*params)
            
    def on_key_up(self, scancode, *params):
        if scancode in self.key_mapping:
            self.key_mapping[scancode][1](*params)
    

class Mouse():
    def __init__(self):
        self.prioritized_obj_list = []        
        self.obj_under_mouse = None
    def add_obj(self, obj, order = 0):
        """ Order needs when checking objects. Objects with lower priority will be checked first.If there are two objects under mouse pointer, one with higher order will be rejected.
        Object must have 3 methods: get_rectange(), press(), unpress() """
        
        self.prioritized_obj_list.append((order, obj))
        self.prioritized_obj_list.sort()
    def add_mult_obj(self, obj_list, order = 0):     
        for obj in obj_list:
            self.prioritized_obj_list.append((order, obj))
        self.prioritized_obj_list.sort()
        
    def _get_obj_at_pos_(self, coursor_pos):
        for (_, obj) in self.prioritized_obj_list:
            if obj.get_rectangle().collidepoint(coursor_pos):
                return obj
        
        
    def on_button_down(self, coursor_pos, *params):
        if self.obj_under_mouse is None:
            obj = self._get_obj_at_pos_(coursor_pos)        
            if obj is not None:
                self.obj_under_mouse = obj
                obj.press(*params)
    def on_move(self, coursor_pos, *params):        
        obj = self._get_obj_at_pos_(coursor_pos)            
        if obj != self.obj_under_mouse:
            if self.obj_under_mouse is not None:
                self.obj_under_mouse.unpress(*params)
                
            self.obj_under_mouse = obj
            if obj is not None:
                obj.press(*params)
    def on_button_up(self, coursor_pos, *params):
        if self.obj_under_mouse is not None:
            self.obj_under_mouse.unpress(*params)
            self.obj_under_mouse = None