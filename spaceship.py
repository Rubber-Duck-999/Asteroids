from pygame.math import Vector2
from models import GameObject
from models import UP
from utils import load_sprite, load_sound
from pygame.transform import rotozoom
from bullet import Bullet

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.engine = load_sound("engine")
        self.destruction = load_sound("explosion")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 
        if clockwise is False:
            sign = -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
    
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        self.engine.play()

    def stop(self):
        self.velocity = self.direction * 0
    
    def destroy(self):
        self.destruction.play()