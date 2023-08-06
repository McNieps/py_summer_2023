import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import TilemapScene, EntityScene
from isec.environment.base import Entity, Pos
from isec.environment.sprite import PymunkSprite

from game.objects.game.player import Player
from game.objects.game.player_spotlight import PlayerSpotlight


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "test") -> None:

        super().__init__(fps=120)
        tile_map = Resource.data["maps"][map_name]
        tile_set = TilemapScene.create_tileset(Resource.image["tileset"]["tileset_1"], 8, 0, 1)

        self.tilemap_scene = TilemapScene(tile_map,
                                          tile_set)
        self.entity_scene = EntityScene(120, camera=self.tilemap_scene.camera)

        self.entity_scene.space.damping = 0.2

        self.player = Player(self.entity_scene)
        self.player_col = Entity(self.player.position, PymunkSprite(self.player.position))
        self.player.add_control_callbacks(self)

        self.player_spotlight = PlayerSpotlight(self.player.position)
        self.entity_scene.add_entities(self.player)

        async def swap_velocity():
            if self.player.velocity == self.player.exploration_velocity:
                self.player.velocity = self.player.chase_velocity
                print('chase velocity')
                return

            self.player.velocity = self.player.exploration_velocity
            print('exploration velocity')

        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_buttondown_callback(4, self.increment_inter_tile)
        self.event_handler.register_buttonup_callback(5, self.decrement_inter_tile)
        self.event_handler.register_keyup_callback(pygame.K_ESCAPE, self.quit_instance)
        self.event_handler.register_keydown_callback(pygame.K_LALT, swap_velocity)

    async def loop(self) -> None:
        LoopHandler.fps_caption()
        self.window.fill(Resource.data["color"]["list"][-1])
        self.tilemap_scene.update(self.delta)
        self.entity_scene.update(self.delta)

        self.entity_scene.camera.position.position[0] = self.player.position.position[0] - 200
        self.entity_scene.camera.position.position[1] = self.player.position.position[1] - 150

        self.tilemap_scene.render()
        self.entity_scene.render()

        spotlight_points = self.player_spotlight.create_spotlight_youtube(self.tilemap_scene.tilemap, 8)
        for i in range(len(spotlight_points)):
            spotlight_points[i] = self.entity_scene.camera.get_offset_pos(Pos(position=spotlight_points[i]))

        for point in []:  # spotlight_points:
            pygame.draw.circle(self.window,
                               (255, 255, 255),
                               point,
                               2)

        pygame.draw.polygon(self.window,
                            Resource.data["color"]["list"][1],
                            spotlight_points,
                            )



    async def move_camera(self) -> None:
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6

    async def increment_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance += 1

    async def decrement_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance -= 1

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
