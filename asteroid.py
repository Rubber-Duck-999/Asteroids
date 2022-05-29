from models import GameObject
from utils import load_sprite, get_random_velocity
from pygame.transform import rotozoom

class Asteroid(GameObject):

    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {
            3: 2,
            2: 1,
            1: 0.5,
        }
        if size == 3:
            image = "asteroid-big"
        else:
            image = "asteroid"
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite(image), 0, scale)

        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )
    
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

