import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import TilemapScene, EntityScene
from isec.environment.base.scene import Scene
from isec.environment.base import Entity
from isec.environment.tile_utils import TileCollision

from game.objects.TileHelper import TileHelper
from game.objects.game.player import Player
from game.objects.game.player_spotlight import PlayerSpotlight
from game.objects.game.collision_types import CollisionTypes
from game.objects.game.rock import Rock
from game.objects.game.vent import Vent
from game.objects.game.detector import Detector
from game.objects.game.stars import Stars
from game.objects.game.sea_top import SeaTop
from game.objects.game.sea_boat import SeaBoat
from game.objects.game.sea_botton import SeaBottom
from game.objects.game.blob import Blob
from game.objects.game.artifact import Artifact


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "abyss_1") -> None:

        super().__init__(fps=120)

        self.map_name: str = map_name
        self.map_dict: dict = {}

        self.color = None
        self.scenes: list[Scene] = []
        self.entity_scene: EntityScene | None = None
        self.terrain_scene: TilemapScene | None = None
        self.collision_map: list[list[bool]] | None = None

        self.player: Player | None = None
        self.screen_filter: pygame.Surface | None = None

        self.spawn_position: tuple[int, int] | None = None
        self.spawn_angle: float | None = None

        self.detectors: list[Detector] = []

        self.current_track: str = "menu"

    async def setup(self):
        await self.load_world(self.map_name)

    async def loop(self) -> None:
        LoopHandler.fps_caption()

        self.window.fill(self.color)

        for scene in self.scenes:
            scene.update(self.delta)

        if self.map_name == "surface" and self.player.position.position[1] < 223:
            force = tuple(pygame.Vector2(0, 200000).rotate(self.player.position.a))
            self.player.position.body.apply_force_at_local_point(force, (0, 0))

        for detector in self.detectors:
            await detector.update(tuple(self.player.position.position))

        self.sync_camera_with_player()

        for scene in self.scenes:
            scene.render()

        self.window.blit(self.screen_filter, (0, 0), special_flags=pygame.BLEND_MULT)

    async def finish(self):
        pygame.mixer.stop()

    # region generation
    async def load_world(self,
                         map_name: str) -> None:

        self.map_name = map_name
        self.map_dict = Resource.data["maps"][map_name]

        self.color = self.map_dict["graphics"]["color_id"]

        if self.spawn_position is None:
            self.spawn_position = self.map_dict["initial_condition"]["position"]
            self.spawn_angle = self.map_dict["initial_condition"]["angle"]

        await self.purge_world()
        await self.create_scenes()
        await self.create_terrain()
        await self.create_entities()
        await self.create_detectors()
        await self.generate_screen_filter()
        await self.create_callbacks()
        await self.set_music()

    async def purge_world(self) -> None:
        pygame.mixer.fadeout(100)
        self.scenes.clear()
        self.event_handler.clear()
        self.detectors.clear()
        self.window.fill(Resource.data["color"]["list"][-1])

    async def create_scenes(self) -> None:
        self.entity_scene = EntityScene(fps=self.fps)
        self.terrain_scene = TilemapScene(tilemap=Resource.data["maps"][f"{self.map_name}_terrain"],
                                          tileset=TileHelper.get_tile_set(),
                                          camera=self.entity_scene.camera)

        self.entity_scene.space.damping = 0.2

        self.scenes.append(self.terrain_scene)
        self.scenes.append(self.entity_scene)

    async def create_terrain(self) -> None:
        self.collision_map = TilemapScene.create_collision_map(Resource.data["maps"][f"{self.map_name}_terrain"],
                                                               TileHelper.get_collision_tile_id())

    async def create_entities(self) -> None:

        self.player = Player(self.entity_scene, self.spawn_position)   # (850, 20))
        self.player.position.a = self.spawn_angle
        tile_collision = TileCollision(self.collision_map,
                                       TileHelper.tile_size,
                                       collision_type=CollisionTypes.WALL,
                                       wall_friction=0.2)

        additional_background_entities = []
        additional_foreground_entities = []
        for map_entities_dict in Resource.data["maps"][self.map_name]["entities"].values():
            is_background, entity = self.create_entity_from_dict(map_entities_dict)
            if is_background:
                additional_background_entities.append(entity)
                continue
            additional_foreground_entities.append(entity)
            # additional_entities.append(self.create_entity_from_dict(map_entities_dict))

        self.entity_scene.add_entities(tile_collision,
                                       *additional_background_entities,
                                       self.player,
                                       *additional_foreground_entities)

        if self.map_dict["graphics"]["spotlight_enabled"]:
            player_spotlight = PlayerSpotlight(self.player.position,
                                               self.collision_map,
                                               TileHelper.tile_size)

            self.entity_scene.add_entities(player_spotlight)

    async def add_entity_dict(self,
                              entity_dict: dict) -> None:

        is_background, entity = self.create_entity_from_dict(entity_dict)
        self.entity_scene.add_entities(entity)

    async def generate_screen_filter(self) -> None:
        if not self.map_dict["graphics"]["filter_enabled"] or self.map_dict["graphics"]["filter_brightness"] == 255:
            self.screen_filter = pygame.Surface((1, 1), pygame.SRCALPHA)
            return

        filter_darkness = self.map_dict["graphics"]["filter_brightness"]
        self.screen_filter = Resource.image["game"]["shadow"].copy()

        if filter_darkness < 0:
            filter_darkness = abs(filter_darkness)
            surf = pygame.Surface((400, 300))
            surf.fill((filter_darkness, filter_darkness, filter_darkness))
            self.screen_filter.blit(surf, (0, 0), special_flags=pygame.BLEND_RGB_SUB)
            return

        surf = pygame.Surface((400, 300))
        surf.fill((filter_darkness, filter_darkness, filter_darkness))
        self.screen_filter.blit(surf, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    async def create_callbacks(self) -> None:
        # Collision callbacks
        t = self.entity_scene.space.add_collision_handler(CollisionTypes.PLAYER, CollisionTypes.WALL)

        def post_step(arbiter, _space, _data):
            if arbiter.is_first_contact:
                self.player.handle_impact(arbiter.total_ke)
            return True

        t.post_solve = post_step

        t = self.entity_scene.space.add_collision_handler(CollisionTypes.PLAYER, CollisionTypes.ROCK)

        def post_step(arbiter, _space, _data):
            if arbiter.is_first_contact:
                self.player.handle_impact(arbiter.total_ke)
            return True

        t.post_solve = post_step

        # Callbacks
        self.player.add_control_callbacks(linked_instance=self)
        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_keyup_callback(pygame.K_ESCAPE, self.quit_instance)
        self.event_handler.register_keydown_callback(pygame.K_LALT, self.swap_velocity)
        self.event_handler.register_buttondown_callback(1, self.print_location)
        self.event_handler.register_quit_callback(LoopHandler.stop_game)

    async def set_music(self,
                        track_name: str = None,
                        track_volume: str = None) -> None:

        if track_name is None:
            track_name = self.map_dict["music"]["track"]

        if track_name is None:
            pygame.mixer.music.stop()
            return

        if track_volume is None:
            track_volume = self.map_dict["music"]["volume"] * Resource.data["engine"]["resource"]["sound"]["volume"]

        if track_name != self.current_track:
            track_path = f"{Resource.project_assets_directory}sound/music/{track_name}.ogg"
            self.current_track = track_name
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(track_volume)

    async def create_detectors(self) -> None:
        for detector_dict in self.map_dict["detectors"].values():
            self.detectors.append(Detector(self,
                                  detector_dict))

    # endregion

    def create_entity_from_dict(self,
                                entity_dict: dict) -> tuple[bool, Entity]:
        """Return a bool indicating whether the entity is a background entity and the entity itself"""

        entity_type = entity_dict["type"]

        if entity_type == "vent":
            vent_position = entity_dict["position"]
            vent_angle = entity_dict["angle"]
            vent_strength = entity_dict["strength"]
            vent_pattern = entity_dict["pattern"]
            vent_offset = entity_dict["offset"]
            return False, Vent(vent_position,
                               vent_angle,
                               vent_strength,
                               vent_pattern,
                               vent_offset)

        if entity_type.startswith("rock_"):
            rock_position = entity_dict["position"]
            rock_angle = entity_dict["angle"]
            rock_speed = entity_dict["speed"]
            return False, Rock(entity_type.removeprefix("rock_"),
                               rock_position,
                               rock_speed,
                               rock_angle)

        if entity_type == "stars":
            return True, Stars()

        if entity_type == "sea_top":
            return True, SeaTop()

        if entity_type == "sea_boat":
            return True, SeaBoat()

        if entity_type == "sea_bottom":
            return False, SeaBottom()

        if entity_type == "blob":
            return False, Blob(self.player,
                               entity_dict["direction"],
                               entity_dict["position"],
                               entity_dict["speed"])

        if entity_type == "artifact":
            return False, Artifact()

        else:
            raise ValueError(f"Unknown entity type {entity_type}")

    def sync_camera_with_player(self) -> None:
        camera_x = min(max(0, self.player.position.position[0]-200), self.terrain_scene.map_size_pixels[0] - 400)
        camera_y = min(max(0, self.player.position.position[1]-150), self.terrain_scene.map_size_pixels[1] - 300)

        self.terrain_scene.camera.position.position[0] = camera_x
        self.terrain_scene.camera.position.position[1] = camera_y

    async def move_camera(self) -> None:
        self.terrain_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6
        self.terrain_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)

    async def print_location(self):
        print(self.entity_scene.camera.position.position + pygame.mouse.get_pos())

    async def swap_velocity(self) -> None:
        if self.player.velocity == self.player.exploration_velocity:
            self.player.velocity = self.player.chase_velocity
            print('Chase')
            return

        self.player.velocity = self.player.exploration_velocity
        print('Exploration')
