import pyglet
from src.GameWindow import *
from pyglet.gl import *

if __name__ == '__main__':
    window = GameWindow(width=1200, height=800, caption='test application')
    glClearColor(1, 1, 1, 1)
    window.run()
