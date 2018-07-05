import pyglet
from src.Window import *
from pyglet.gl import *

if __name__ == '__main__':
    window = Window(width=600, height=400, caption='test application', resizable=True)
    glClearColor(1, 1, 1, 1)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
