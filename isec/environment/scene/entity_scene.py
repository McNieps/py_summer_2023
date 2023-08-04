import pygame
import pymunk

from isec.environment.base.scene import Scene
from isec.environment.base.entity import Entity
from isec.environment.base.camera import Camera
from isec.environment.position.pymunk_pos import PymunkPos


class EntityScene(Scene):
    def __init__(self,
                 surface: pygame.Surface = None,
                 entities: list[Entity] = None):

        super().__init__(surface)

        if entities is None:
            entities = []
        self.entities = entities

        self.space = pymunk.Space()

    def add_entities(self,
                     *entities) -> None:

        self.entities.extend([entity for entity in entities
                              if entity not in self.entities])

        for entity in entities:
            if isinstance(entity.position, PymunkPos):
                if entity.position.body not in self.space.bodies:
                    self.space.add(entity.position.body)
                self.space.add(*[shape for shape in entity.position.shapes if shape not in self.space.shapes])

    def update(self,
               delta: float) -> None:

        for entity in self.entities:
            entity.update(delta)

        self.space.step(delta)

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        for entity in self.entities:
            entity.render(camera.get_offset(entity.position), self.surface, self.rect)
