
class RayHitResult():
    def __init__(self, depth, hit_x, hit_y, segment):
        self.depth = depth
        self.hit_x = hit_x
        self.hit_y = hit_y
        self.segment = segment