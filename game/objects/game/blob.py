import pygame

from isec.app import Resource
from isec.environment import Entity
from isec.environment.sprite import AnimatedSprite
from isec.environment.position import SimplePos


class Blob(Entity):
    def __init__(self,
                 player: Entity,
                 direction: tuple[int, int],
                 pos: int,
                 speed: int) -> None:

        self.player = player
        self.direction = direction
        self.blocked = False

        if all(direction):
            # raise error because no diagonal movement is allowed
            raise ValueError("No diagonal movement is allowed")

        position = SimplePos(position=(pos*abs(direction[0]), pos*abs(direction[1])),
                             speed=(speed*direction[0], speed*direction[1]))

        monster_surfaces = [Resource.image["game"][f"blob_{i+1}"] for i in range(3)]
        if direction[1]:
            for i in range(len(monster_surfaces)):
                monster_surfaces[i] = pygame.transform.rotate(monster_surfaces[i], -90)

        if direction[0] < 0:
            for i in range(len(monster_surfaces)):
                monster_surfaces[i] = pygame.transform.flip(monster_surfaces[i], True, False)

        if direction[1] < 0:
            for i in range(len(monster_surfaces)):
                monster_surfaces[i] = pygame.transform.flip(monster_surfaces[i], False, True)

        self.animated_sprite = AnimatedSprite(monster_surfaces,
                                              rendering_technique="static",
                                              frame_durations=[1, 0, 0])

        super().__init__(position, self.animated_sprite)
        self.sprite: AnimatedSprite

    def update(self,
               delta: float) -> None:

        x, y = self.position.position
        x = self.player.position.position[0] if self.direction[0] == 0 else x
        y = self.player.position.position[1] if self.direction[1] == 0 else y
        self.position.position = x, y

        super().update(delta)

        distance_x = abs(self.player.position.position[0] - self.position.position[0])
        distance_y = abs(self.player.position.position[1] - self.position.position[1])
        distance = (distance_x**2 + distance_y**2)**0.5

        if distance > 120:
            self.animated_sprite.frame_durations = [0, 1, 0]
        elif distance > 70:
            self.animated_sprite.frame_durations = [1, 0, 0]
        else:
            self.animated_sprite.frame_durations = [0, 0, 1]

    # kill dist = 70
        # open dist = 100

