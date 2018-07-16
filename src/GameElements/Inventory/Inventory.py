class InventoryClass:
    size = 0
    stock = {}

    def __init__(self, size):
        self.size = size

        self.stock = {a: {} for a in range(self.size)}

        for index in range(0, self.size):
            self.stock[index]['amount'] = 0
            self.stock[index]['object'] = None

    def get_info(self):
        info = {
            'size': self.size,
            'items': {a: {} for a in range(self.size)}
        }
        for index in range(0, self.size):
            info['items'][index]['amount'] = self.stock[index]['amount']
            info['items'][index]['object'] = self.stock[index]['object']
        return info

    def add_items(self, item, amount):
        for index, cell in self.stock.items():
            if cell['object'] is None:
                cell['object'] = item
                cell['amount'] = amount
                return True
            elif cell['object'].name == item.name:
                if item.stack is not None and cell['amount'] < item.stack:
                    cell['amount'] += amount
                    return True

        return False

    def delete_all_items(self, item):
        index = self.get_cell_number_for_item(item)
        if isinstance(index, int):
            return self.delete_items(item, self.stock[index]['amount'])

    def delete_items(self, item, amount):
        index = self.get_cell_number_for_item(item)
        if isinstance(index, int):
            cell = self.stock[index]
            if cell['amount'] > amount:
                cell['amount'] -= amount
                return True
            elif cell['amount'] == amount:
                cell['amount'] = 0
                cell['object'] = None
                return True
            elif cell['amount'] < amount:
                return False
        else:
            return False

    def get_cell_number_for_item(self, item):
        for index, cell in self.stock.items():
            if cell['object'].name == item.name:
                return index

        return False

    def is_full(self):
        full_inventory = True
        for index, cell in self.stock.items():
            if cell['object'] is not None:
                if cell['object'].stack is None or cell['amount'] < cell['object'].stack:
                    full_inventory = False
                    break
            else:
                full_inventory = False
                break
        return full_inventory
