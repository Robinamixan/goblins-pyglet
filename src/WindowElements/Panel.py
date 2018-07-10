import pyglet
from pyglet.gl import gl
from src.WindowElements.FixedLabel import FixedLabel
from src.Constants import *


class Panel:
    def __init__(self, window, start_point, end_point, color):
        self.window = window
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.batch = pyglet.graphics.Batch()
        self.labels = {}
        self.variable = 0

        start_x = self.start_point[0]
        start_y = self.start_point[1]

        end_x = self.end_point[0]
        end_y = self.end_point[1]

        self.batch.add(
            4,
            gl.GL_POLYGON,
            None,
            ('v2i', [start_x, start_y, start_x, end_y, end_x, end_y, end_x, start_y]),
            ('c4B', self.color * 4))

    def add_label(self, label_id, position):
        current_position = [0, 0]
        current_position[0] = position[0] + self.start_point[0]
        current_position[1] = position[1] + self.start_point[1]
        label = FixedLabel(self.window, '', current_position, color=black, fixed_bottom=False, font_size=12)
        self.labels[label_id] = label

    def update_text(self, camera, game_object, mouse_position):
        for label_id, label in self.labels.items():
            if camera:
                if label_id == 'camera_bottom':
                    label.update(str(int(camera.bottom)))
                elif label_id == 'camera_top':
                    label.update(str(int(camera.top)))
                elif label_id == 'camera_right':
                    label.update(str(int(camera.right)))
                elif label_id == 'camera_left':
                    label.update(str(int(camera.left)))
            if game_object:
                if label_id == 'object_name':
                    label.update(game_object.get_name())
                elif label_id == 'object_position':
                    position = game_object.get_point()
                    text = '[' + str(int(position[0])) + ', ' + str(int(position[1])) + ']'
                    label.update(text)
                elif self.window.game_controller.is_mob(game_object):
                    if label_id == 'object_vector':
                        vector = game_object.get_vectors()
                        text = '[' + str(int(vector[0])) + ', ' + str(int(vector[1])) + ']'
                        label.update(text)
                    elif label_id == 'object_destination':
                        destination = game_object.get_destination()
                        text = '[' + str(int(destination[0])) + ', ' + str(int(destination[1])) + ']'
                        label.update(text)
                    elif label_id == 'object_action':
                        action = game_object.get_action()
                        text = action
                        label.update(text)
                    elif label_id == 'object_inventory_info':
                        inventory = game_object.get_inventory_info()
                        empty = True
                        for index, item in inventory['items'].items():
                            if item['object'] is not None:
                                empty = False
                                break

                        text = 'size: ' + str(inventory['size'])
                        if empty:
                            text += ', empty'

                        label.update('Inventory: ' + text)
                    elif label_id == 'object_inventory_contain':
                        inventory = game_object.get_inventory_info()
                        empty = True
                        text = ''
                        for index, item in inventory['items'].items():
                            if item['object'] is not None:
                                empty = False
                                text += item['object'].name + '(' + str(item['amount']) + '), '

                        if not empty:
                            label.update('Contain: ' + text)

                else:
                    label.update('')
            else:
                label.update('')
            if mouse_position:
                point = self.window.game_controller.get_point_by_coord(mouse_position)
                if label_id == 'coord_point_x':
                    label.update(str(int(mouse_position[0])) + '[' + str(int(point[0])) + ']')
                elif label_id == 'coord_point_y':
                    label.update(str(int(mouse_position[1])) + '[' + str(int(point[1])) + ']')
            else:
                if label_id == 'object_name':
                    label.update('')
                elif label_id == 'object_position':
                    label.update('')

    def draw(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.window.width, 0, self.window.height, -1, 1)

        self.batch.draw()
        for label_id, label in self.labels.items():
            label.raw_draw()

        gl.glPopMatrix()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
