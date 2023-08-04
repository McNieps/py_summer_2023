import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import TilemapScene


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "map") -> None:

        super().__init__()
        tile_map = Resource.data["maps"][map_name]
        tile_set = TilemapScene.create_tileset(Resource.image["tileset"]["simple"], 8, 0, 1)
        self.scene = TilemapScene(tile_map, tile_set)

        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_buttondown_callback(4, self.increment_inter_tile)
        self.event_handler.register_buttonup_callback(5, self.decrement_inter_tile)

    async def loop(self) -> None:
        self.window.fill(Resource.data["color"]["list"][-1])
        self.scene.update(self.delta)
        self.scene.render()

    async def move_camera(self) -> None:
        self.scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel)/6
        self.scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel)/6

    async def increment_inter_tile(self):
        self.scene.inter_tile_distance += 1

    async def decrement_inter_tile(self):
        self.scene.inter_tile_distance -= 1
