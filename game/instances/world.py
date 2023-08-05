import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import TilemapScene, EntityScene
from isec.environment.base import Entity
from isec.environment.sprite import PymunkSprite

from game.objects.game.player import Player


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "map") -> None:

        super().__init__()
        tile_map = Resource.data["maps"][map_name]
        tile_set = TilemapScene.create_tileset(Resource.image["tileset"]["simple"], 8, 0, 1)

        self.tilemap_scene = TilemapScene(tile_map,
                                          tile_set)
        self.entity_scene = EntityScene(camera=self.tilemap_scene.camera)

        self.entity_scene.space.damping = 0.4

        self.player = Player(self.entity_scene)
        self.player_col = Entity(self.player.position, PymunkSprite(self.player.position))
        self.player.add_control_callbacks(self)

        self.entity_scene.add_entities(self.player)   # , self.player_col)

        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_buttondown_callback(4, self.increment_inter_tile)
        self.event_handler.register_buttonup_callback(5, self.decrement_inter_tile)
        self.event_handler.register_keyup_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self) -> None:
        self.window.fill(Resource.data["color"]["list"][-1])
        self.tilemap_scene.update(self.delta)
        self.entity_scene.update(self.delta)
        self.tilemap_scene.render()
        self.entity_scene.render()

    async def move_camera(self) -> None:
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6

    async def increment_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance += 1

    async def decrement_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance -= 1

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
