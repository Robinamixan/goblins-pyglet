import pyglet
from src.GameWindow import *
from pyglet.gl import *

if __name__ == '__main__':
    window = GameWindow(width=1000, height=800, caption='test application', resizable=True)
    glClearColor(1, 1, 1, 1)
    window.run()
