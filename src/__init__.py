import pyglet
from src.GameWindow import *
from pyglet.gl import *
from src.Constants import *

if __name__ == '__main__':
    window = GameWindow(width=screen_size[0], height=screen_size[1], caption='test application')
    glClearColor(1, 1, 1, 1)
    window.run()
