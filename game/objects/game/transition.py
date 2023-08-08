import pygame
import random

from collections.abc import Iterable

from isec.app import Resource

from isec.environment import Sprite, Entity
from isec.environment.position import SimplePos


class Transition(Entity):
    def __init__(self, map_name: str):
        self.map_name = map_name
        self.ready_to_transition = False
        self.transitioned = False
        self.done = False

        speed = 800
        angle = random.randint(0, 3) * 90
        fpos = pygame.Vector2(1, 0).rotate(angle)
        self.direction = int(fpos[0]), int(fpos[1])
        pos = 200 + 400 * -self.direction[0], 150 + 300 * -self.direction[1]
        self.speed = speed * fpos[0], speed * fpos[1]

        position = SimplePos(pos, self.speed)
        sprite = Sprite(Resource.image["game"]["frame"])
        super().__init__(position, sprite)

    def get_delta_multiplier(self) -> float:
        dist_x = abs(self.position.position[0] - 200)
        dist_y = abs(self.position.position[1] - 150)

        if dist_x > dist_y:
            multiplier = dist_x / 400
        else:
            multiplier = dist_y / 300

        return multiplier ** 0.2

    def update(self,
               delta: float) -> None:

        print(self.get_delta_multiplier())
        if self.done:
            return

        super().update(delta)

        if not self.ready_to_transition:
            if self.direction[0] > 0 and self.position.position[0] > 200:
                self.position.position = (200, self.position.position[1])
                self.ready_to_transition = True

            elif self.direction[0] < 0 and self.position.position[0] < 200:
                self.position.position = (200, self.position.position[1])
                self.ready_to_transition = True

            elif self.direction[1] > 0 and self.position.position[1] > 150:
                self.position.position = (self.position.position[0], 150)
                self.ready_to_transition = True

            elif self.direction[1] < 0 and self.position.position[1] < 150:
                self.position.position = (self.position.position[0], 150)
                self.ready_to_transition = True

        if self.direction[0] > 0 and self.position.position[0] > 600:
            self.done = True

        elif self.direction[0] < 0 and self.position.position[0] < -200:
            self.done = True

        elif self.direction[1] > 0 and self.position.position[1] > 450:
            self.done = True

        elif self.direction[1] < 0 and self.position.position[1] < -150:
            self.done = True

    def render(self,
               camera_offset: Iterable,
               surface: pygame.Surface,
               rect: pygame.Rect) -> None:

        if self.done:
            return
        super().render(camera_offset, surface, rect)
