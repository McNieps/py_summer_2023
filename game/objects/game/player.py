import pygame

from isec.app import Resource
from isec.environment import Entity, Sprite
from isec.environment.position import PymunkPos
from isec.instance import BaseInstance

from game.objects.controls import Controls


class Player(Entity):
    def __init__(self) -> None:
        position = PymunkPos(position=(100, 100))
        player_surface = Resource.image["game"]["submarine_1"]
        position.create_rect_shape(player_surface, density=50, radius=-1.5)

        sprite = Sprite(player_surface, rendering_technique="rotated")

        super().__init__(position, sprite)

        self.sprite_flipped = False

    async def forward(self) -> None:
        self.position.body.apply_force_at_local_point((0, -100000), (0, 0))

    async def backward(self) -> None:
        self.position.body.apply_force_at_local_point((0, 100000), (0, 0))

    async def left(self) -> None:
        self.position.body.apply_force_at_local_point((-100000, 0), (0, 0))

    async def right(self) -> None:
        self.position.body.apply_force_at_local_point((100000, 0), (0, 0))

    def add_control_callbacks(self, linked_instance: BaseInstance) -> None:
        linked_instance.event_handler.register_keypressed_callback(Controls.FORWARD, self.forward)
        linked_instance.event_handler.register_keypressed_callback(Controls.BACKWARD, self.backward)
        linked_instance.event_handler.register_keypressed_callback(Controls.LEFT, self.left)
        linked_instance.event_handler.register_keypressed_callback(Controls.RIGHT, self.right)

    def update(self,
               delta: float) -> None:
        super().update(delta)

        if self.position.a % 360 > 180 and not self.sprite_flipped:
            self.sprite_flipped = True
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)
        elif self.position.a % 360 < 180 and self.sprite_flipped:
            self.sprite_flipped = False
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)
