from queue import Queue
import copy


class PathCreator:
    def __init__(self, game_map):
        self.map = game_map
        self.limit_max = [0, 0]
        self.all_nodes = []
        self.came_from = {}
        self.update_nodes(self.map.cells)

    def neighbors(self, node):
        directs = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, 1], [-1, -1], [1, -1]]
        result = []
        for direct in directs:
            neighbor = [node[0] + direct[0], node[1] + direct[1]]
            if 0 <= neighbor[0] < self.limit_max[0] and 0 <= neighbor[1] < self.limit_max[1]:
                if neighbor in self.all_nodes:
                    result.append(neighbor)
        return result

    def create_text(self, list):
        return str(list[0]) + '_' + str(list[1])

    def create_path(self, start, end):
        if end not in self.all_nodes or end == start:
            return []
        # including mobs in graph
        self.update_nodes(self.map.cells)
        self.fill_graph(start, end)
        current = end
        path = [current]
        prev = self.get_prev(current)
        while prev is not None:
            path.insert(0, prev)
            current = copy.copy(prev)
            prev = self.get_prev(current)
        return path

    def get_prev(self, node):
        return self.came_from[self.create_text(node)]

    def update_nodes(self, cells):
        self.limit_max = [len(cells), len(cells[0])]
        self.all_nodes = []
        for x in range(self.limit_max[0]):
            for y in range(self.limit_max[1]):
                if cells[x][y].is_passable():
                    self.all_nodes.append([x, y])

    def fill_graph(self, start, end):
        frontier = Queue()
        frontier.put(start)
        self.came_from = {}
        self.came_from[self.create_text(start)] = None
        while not frontier.empty():
            current = frontier.get()
            for next in self.neighbors(current):
                if self.create_text(next) not in self.came_from:
                    frontier.put(next)
                    self.came_from[self.create_text(next)] = current
                    if next == end:
                        break
