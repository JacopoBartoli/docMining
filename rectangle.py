class Rectangle(object):
    def __init__(self, width=1, height=1, x_center=0.5, y_center=0.5):
        self.width = width
        self.height = height
        self.x_center = x_center
        self.y_center = y_center

    @property
    def area(self):
        return self.width * self.height
