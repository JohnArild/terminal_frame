#!/usr/bin/env python3

import subprocess
import time

"""
This only works in linux and mac.
Getting the terminal size in Windows is a bit more involved.
This is a little demo of how to draw a frame that fills the 
whole terminal window.

"""

def get_screen_size():
    command_wdith = "tput cols"
    command_height = "tput lines"
    width = subprocess.getoutput(command_wdith)
    height = subprocess.getoutput(command_height)
    return int(width), int(height)

def draw_frame(width, height):
    print("\033c", end="") #Clear screen
    print("\033[?25l", end="") #Hide cursor
    print("".rjust(width, "*"), end="") #Top frame
    for line in range(height):
        print(f"\033[{line};1H*", end="") #Left frame
        print(f"\033[{line};{width}H*", end="") #Right frame
    print("".rjust(width, "*"), end="") #Bottom frame
    print("", end="\r") #Show text

def draw_info(width, height):
    def center_text(text, line):
        start_pos_column = int((width - 2 - len(text)) / 2)
        print(f"\033[{line};{start_pos_column}H{text}", end="")
    def bottom_text(text):
        line = height - 1
        start_pos_column = 3
        print(f"\033[{line};{start_pos_column}H{text}", end="")
    center_text("Try resizing the window", 3)
    bottom_text("Press Ctrl+c to exit")
    print("", end="\r") #Show text

def loop():
    screen_size = None
    while True:
        time.sleep(0.1)
        """Redraw if size has changed"""
        if screen_size != get_screen_size():
            screen_size = get_screen_size()
            draw_frame(*screen_size)
            draw_info(*screen_size)
        

if __name__ == '__main__':
    try:
        subprocess.run(["stty", "-echo"]) #echo off
        loop()
    except KeyboardInterrupt:
        print("\033[?25h") #Show cursor
        print("\033c", end="\r") #Clear screen
        subprocess.run(["stty", "echo"]) #echo on
