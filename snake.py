from collections import deque

class Snake:
    def __init__(self, start_x, start_y):
        self.head = (start_x, start_y)
        self.direction = (1, 0)
        self.body = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.grow_by = 0

    def set_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction

    def move(self):
        x, y = self.head
        dx, dy = self.direction
        self.head = (x + dx, y + dy)
        self.body.appendleft(self.head)
        if self.grow_by > 0:
            self.grow_by -= 1
        else:
            self.body.pop()

    def grow(self):
        self.grow_by += 1

    def intersects(self, pt):
        return pt in list(self.body)

    def collides_self(self):
        return self.head in list(self.body)[1:]
