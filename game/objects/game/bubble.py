import pygame
import random
import time

from isec.app import Resource
from isec.environment import Sprite, Entity
from isec.environment.position import SimplePos


class Bubble(Entity):
    def __init__(self,
                 position: tuple[int, int],
                 angle: float) -> None:

        speed = pygame.Vector2(random.randint(0, 1000)/20, 0)
        speed.rotate_ip(random.gauss(180+angle, 60))

        position = SimplePos(position, speed)
        super().__init__(position, Sprite(Resource.image["game"]["bubble"]))

        self.spawn_time = time.time()
        self.lifetime = random.randint(100, 200) / 400

    def update(self,
               delta: float) -> None:
        super().update(delta)

        damping = 0.05 ** delta
        self.position.speed[0] *= damping
        self.position.speed[1] = (self.position.speed[1] - 50 * delta) * damping

        if time.time() > self.spawn_time+self.lifetime:
            self.to_delete = True
