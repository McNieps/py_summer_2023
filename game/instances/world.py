import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import TilemapScene, EntityScene
from isec.environment.base.scene import Scene
from isec.environment.tile_utils import TileCollision

from game.objects.TileHelper import TileHelper
from game.objects.game.player import Player
from game.objects.game.player_spotlight import PlayerSpotlight
from game.objects.game.collision_types import CollisionTypes


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "abyss_4") -> None:

        super().__init__(fps=120)

        self.map_name: str = map_name
        self.map_dict: dict = {}

        self.scenes: list[Scene] = []
        self.entity_scene: EntityScene | None = None
        self.terrain_scene: TilemapScene | None = None

        self.player: Player | None = None
        self.screen_filter: pygame.Surface | None = None

        self.spawn_position: tuple[int, int] | None = None
        self.spawn_angle: float | None = None

    async def setup(self):
        await self.load_world(self.map_name)

    async def loop(self) -> None:
        LoopHandler.fps_caption()

        self.window.fill(Resource.data["color"]["list"][-1])  # TODO: Load this color in map.json

        for scene in self.scenes:
            scene.update(self.delta)

        self.scenes[1].camera.position.position[0] = self.player.position.position[0] - 200
        self.scenes[1].camera.position.position[1] = self.player.position.position[1] - 150

        for scene in self.scenes:
            scene.render()

        self.window.blit(self.screen_filter, (0, 0), special_flags=pygame.BLEND_MULT)

    async def load_world(self,
                         map_name: str) -> None:

        self.map_name = map_name
        self.map_dict = Resource.data["maps"][map_name]

        await self.purge_world()
        await self.generate_screen_filter()

        # Loading terrain
        tile_map = Resource.data["maps"][f"{map_name}_terrain"]
        collision_map = TilemapScene.create_collision_map(tile_map,
                                                          TileHelper.get_collision_tile_id())

        # Scenes
        self.entity_scene = EntityScene(fps=self.fps)
        self.terrain_scene = TilemapScene(tilemap=tile_map,
                                          tileset=TileHelper.get_tile_set(),
                                          camera=self.entity_scene.camera)
        self.entity_scene.space.damping = 0.2

        self.scenes.append(self.terrain_scene)
        self.scenes.append(self.entity_scene)

        # Creating entities
        self.player = Player(self.entity_scene, (850, 20))

        player_spotlight = PlayerSpotlight(self.player.position,
                                           collision_map,
                                           TileHelper.tile_size)

        tile_collision = TileCollision(collision_map,
                                       TileHelper.tile_size,
                                       collision_type=CollisionTypes.WALL,
                                       wall_friction=0.2)

        self.entity_scene.add_entities(self.player, player_spotlight, tile_collision)
        await self.create_callbacks()

    async def purge_world(self) -> None:
        self.scenes.clear()
        self.window.fill(Resource.data["color"]["list"][-1])

    async def create_scene(self) -> None:
        pass

    async def create_terrain(self) -> None:
        pass

    async def add_entities(self) -> None:
        pass

    async def generate_screen_filter(self) -> None:
        filter_darkness = 0   # TODO: LINK WITH MAP DICT

        self.screen_filter = Resource.image["game"]["shadow"].copy()
        if filter_darkness > 0:
            surf = pygame.Surface((400, 300))
            value = int(255 * filter_darkness)
            surf.fill((value, value, value))
            self.screen_filter.blit(surf, (0, 0), special_flags=pygame.BLEND_MULT)

    async def create_callbacks(self) -> None:
        # Collision callbacks
        t = self.entity_scene.space.add_collision_handler(CollisionTypes.PLAYER, CollisionTypes.WALL)

        def post_step(arbiter, _space, _data):
            if arbiter.is_first_contact:
                self.player.handle_impact(arbiter.total_ke)
            return True

        t.post_solve = post_step

        # Callbacks
        self.player.add_control_callbacks(linked_instance=self)
        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_buttondown_callback(4, self.increment_inter_tile)
        self.event_handler.register_buttonup_callback(5, self.decrement_inter_tile)
        self.event_handler.register_keyup_callback(pygame.K_ESCAPE, self.quit_instance)
        self.event_handler.register_keydown_callback(pygame.K_LALT, self.swap_velocity)
        self.event_handler.register_buttondown_callback(1, self.print_location)

    async def move_camera(self) -> None:
        self.terrain_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6
        self.terrain_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6

    async def increment_inter_tile(self) -> None:
        self.terrain_scene.inter_tile_distance += 1

    async def decrement_inter_tile(self) -> None:
        self.terrain_scene.inter_tile_distance -= 1

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)

    async def print_location(self):
        print(self.entity_scene.camera.position.position + pygame.mouse.get_pos())

    async def swap_velocity(self) -> None:
        if self.player.velocity == self.player.exploration_velocity:
            self.player.velocity = self.player.chase_velocity
            print('Chase velocity')
            return

        self.player.velocity = self.player.exploration_velocity
        print('Exploration velocity')
