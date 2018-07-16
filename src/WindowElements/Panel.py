import pyglet
from pyglet.gl import gl
from pyglet.input.base import Button
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
        self.labels_amount = 0

        self.button = Button('click', 'click')

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

    def create_label(self):
        index = self.labels_amount
        self.labels[index] = {}
        self.labels[index]['visible'] = False

        label = FixedLabel(self.window, '', [0, 0], color=black, fixed_bottom=False, font_size=12)
        self.labels[index]['label'] = label
        self.labels_amount += 1

        return index

    def get_free_label_index(self):
        for index, item in self.labels.items():
            if not item['visible']:
                return index

        return None

    def set_label_position(self, index, position):
        self.labels[index]['visible'] = True
        relative_position = [self.start_point[0] + position[0], self.start_point[1] + position[1]]
        self.labels[index]['label'].set_position(relative_position)

    def set_label_text(self, index, text):
        self.labels[index]['label'].update(text)

    def set_label(self, text, position):
        index = self.get_free_label_index()
        if index is None:
            index = self.create_label()

        self.set_label_position(index, position)
        self.set_label_text(index, text)

    def clear_labels(self):
        for index, item in self.labels.items():
            self.labels[index]['visible'] = False

    def update_text(self, camera, game_object, mouse_position):
        self.clear_labels()
        if camera:
            pass

        if game_object:
            self.set_label(game_object.get_name(), (90, 20))

            position = game_object.get_point()
            position_str = '[' + str(int(position[0])) + ', ' + str(int(position[1])) + ']'
            self.set_label(position_str, (90, 60))

            if self.window.game_controller.is_mob(game_object):
                self.set_mobs_labels(game_object)

            if self.window.game_controller.is_cave(game_object):
                self.set_building_labels(game_object)
        if mouse_position:
            point = self.window.game_controller.get_point_by_coord(mouse_position)

            x_str = str(int(mouse_position[0])) + '[' + str(int(point[0])) + ']'
            self.set_label(x_str, (10, 20))

            y_str = str(int(mouse_position[1])) + '[' + str(int(point[1])) + ']'
            self.set_label(y_str, (10, 40))

    def set_mobs_labels(self, game_object):
        action_str = game_object.get_action_string()
        self.set_label(action_str, (90, 40))

        destination = game_object.get_destination()
        destination_str = '[' + str(int(destination[0])) + ', ' + str(int(destination[1])) + ']'
        self.set_label(destination_str, (90, 80))

        vector = game_object.get_vectors()
        vector_str = '[' + str(int(vector[0])) + ', ' + str(int(vector[1])) + ']'
        self.set_label(vector_str, (90, 100))

        inventory = game_object.get_inventory_info()
        inventory_title = 'Inventory(size=' + str(inventory['size']) + '): '
        first_line_x = 150
        self.set_label(inventory_title, (10, first_line_x))
        line = 1
        for index, item in inventory['items'].items():
            if item['object'] is None:
                continue
            else:
                item_str = ' - ' + item['object'].get_name() + '(' + str(item['amount']) + ')'
                self.set_label(item_str, (10, first_line_x + line * 20))
                line += 1

    def set_building_labels(self, game_object):
        staff = game_object.get_staff_info()
        staff_title = 'Staff(size=' + str(staff['size']) + '): '
        first_line_x = 100
        self.set_label(staff_title, (10, first_line_x))

        line = 1
        for index, item in staff['members'].items():
            if item['mob'] is None:
                continue
            else:
                if item['inside']:
                    condition_str = 'inside'
                else:
                    condition_str = 'outside'
                item_str = ' - ' + item['mob'].get_name() + '(' + condition_str + ')'
                self.set_label(item_str, (10, first_line_x + line * 20))
                line += 1

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
            if label['visible']:
                label['label'].raw_draw()

        gl.glPopMatrix()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
