class Item:
    def __init__(self, item_id, category, stop_index):
        self.item_id = item_id
        self.category = category
        self.stop_index = int(stop_index)

class ShipmentsQueue:
    def __init__(self):
        self.data = []

    def add(self, item):
        self.data.append(item)

    def get_next(self):
        if self.data:
            return self.data.pop(0)
        return None

class StorageArray:
    def __init__(self, size=6):
        self.size = size
        self.slots = [None] * size

    def put_in_slot(self, item, index):
        if 0 <= index < self.size:
            if self.slots[index] is None:
                self.slots[index] = item
                return True
        return False

    def clear_and_get_all(self):
        items = [i for i in self.slots if i is not None]
        self.slots = [None] * self.size
        return items

class TruckStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None