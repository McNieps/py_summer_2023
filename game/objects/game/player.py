import pygame
import math
import time

from isec.app import Resource
from isec.environment import Entity, Sprite, EntityScene
from isec.environment.position import PymunkPos
from isec.instance import BaseInstance

from game.objects.controls import Controls
from game.objects.game.bubble import Bubble
from game.objects.game.collision_types import CollisionTypes


class Player(Entity):
    def __init__(self,
                 linked_scene: EntityScene,
                 initial_pos: tuple[int, int] = (100, 100)) -> None:

        self.linked_scene = linked_scene

        position = PymunkPos(position=initial_pos, shape_collision_type=CollisionTypes.PLAYER)
        player_surface = Resource.image["game"]["submarine_1"]

        position.create_circle_shape(radius=Resource.data["objects"]["player"]["radius"],
                                     friction=Resource.data["objects"]["player"]["friction"],
                                     density=Resource.data["objects"]["player"]["density"])

        sprite = Sprite(player_surface, rendering_technique="rotated")

        super().__init__(position, sprite)

        self.sprite_flipped = False

        # Gameplay related
        self.integrity = Resource.data["objects"]["player"]["integrity"]

        # Physics related
        self.exploration_velocity = Resource.data["objects"]["player"]["exploration_thrust"]
        self.chase_velocity = Resource.data["objects"]["player"]["chase_thrust"]
        self.velocity = self.exploration_velocity
        self.torque_mult = 0.5
        self.boost_mult = Resource.data["objects"]["player"]["boost_multiplier"]

        # Particle related
        self.max_bubble_spawn_frequency = 200
        self.max_speed_max_frequency = 200
        self.bubble_last_spawn = time.time()

        # Controls related
        self.pressed = {"up": False, "down": False, "left": False, "right": False, "boost": False}

        # Audio related
        self.sound_to_play = None
        self.current_sound = None
        self.current_channel = None

    def update(self,
               delta: float) -> None:

        super().update(delta)
        self.position.body.angular_velocity *= 0.02 ** delta

        angle_difference = self.get_angle_cursor_player()

        self.rotate_player(angle_difference, delta)
        self.move_player(delta)
        self.spawn_bubble(delta)
        self.flip_sprite()
        self.play_sound()

    def get_angle_cursor_player(self) -> float | None:
        player_screen_pos = pygame.Vector2(self.linked_scene.camera.get_offset_pos(self.position))
        cursor_screen_pos = pygame.Vector2(pygame.mouse.get_pos())
        relative_pos = cursor_screen_pos - player_screen_pos

        if relative_pos.length() == 0:
            return None

        goal_angle = relative_pos.angle_to(pygame.Vector2(1, 0)) % 360
        current_angle = self.position.a

        difference = (goal_angle - current_angle) % 360
        if difference > 180:
            difference -= 360

        return difference

    def rotate_player(self,
                      angle_difference: float,
                      delta: float) -> None:

        if angle_difference is None:
            return

        torque = angle_difference * delta * self.torque_mult

        self.position.body.apply_force_at_world_point((0, -torque), (self.position.position[0] + 50000, 0))
        self.position.body.apply_force_at_world_point((0, torque), (self.position.position[0] - 50000, 0))

    def move_player(self,
                    delta: float) -> None:

        forward_angle = math.degrees(self.position.body.rotation_vector.angle) % 360

        input_vec = pygame.math.Vector2(0, 0)
        if self.pressed["up"]:
            input_vec += (0, -1)
        if self.pressed["down"]:
            input_vec += (0, 1)
        if self.pressed["left"]:
            input_vec += (-1, 0)
        if self.pressed["right"]:
            input_vec += (1, 0)

        if input_vec.length() <= 0:
            self.pressed = {"up": False, "down": False, "left": False, "right": False, "boost": False}
            self.sound_to_play = None
            return

        self.sound_to_play = "sub_slow" if self.velocity == self.exploration_velocity else "sub_fast"

        input_vec.normalize_ip()
        input_angle = (-input_vec.angle_to((1, 0))) % 360
        difference = (input_angle - forward_angle) % 360
        if difference > 180:
            difference -= 360

        speed = input_vec * delta * self.velocity
        if -90 < difference < 90:
            mult = 1+math.cos(math.radians(difference))**2
            if self.pressed["boost"]:
                self.sound_to_play += "_boost"
                mult *= self.boost_mult

            speed *= mult

        speed.rotate_ip(-forward_angle)
        self.position.body.apply_force_at_local_point(tuple(speed), (0, 0))

        self.pressed = {"up": False, "down": False, "left": False, "right": False, "boost": False}

    def play_sound(self) -> None:
        if self.sound_to_play is None:
            if self.current_sound is not None:
                self.current_channel.fadeout(1000)
                self.current_sound = None
                self.current_channel = None
            return

        if self.current_sound != self.sound_to_play:
            if self.current_channel is not None:
                self.current_channel.fadeout(1000)

            self.current_sound = self.sound_to_play
            self.current_channel = Resource.sound["game"][self.sound_to_play].play(-1)

    def flip_sprite(self) -> None:
        if (90 < self.position.a < 270) and not self.sprite_flipped:
            self.sprite_flipped = True
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)
        elif (self.position.a < 90 or self.position.a > 270) and self.sprite_flipped:
            self.sprite_flipped = False
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)

    def spawn_bubble(self, delta) -> None:
        bubble_spawn_frequency = self.position.body.velocity.length / self.max_speed_max_frequency * self.max_bubble_spawn_frequency
        if bubble_spawn_frequency < 0.05:
            return

        bubble_spawn_period = 1 / bubble_spawn_frequency

        diff = time.time() - self.bubble_last_spawn
        while diff >= bubble_spawn_period:
            diff -= bubble_spawn_period
            self.bubble_last_spawn += bubble_spawn_period
            self.linked_scene.add_entities(Bubble(tuple(self.position.position-2*self.position.body.rotation_vector),
                                                  self.position.body.rotation_vector.angle_degrees))

    def handle_impact(self,
                      kinetic_energy: float) -> None:

        print(kinetic_energy)

    async def up(self) -> None:
        self.pressed["up"] = True

    async def down(self) -> None:
        self.pressed["down"] = True

    async def left(self) -> None:
        self.pressed["left"] = True

    async def right(self) -> None:
        self.pressed["right"] = True

    async def boost(self) -> None:
        self.pressed["boost"] = True

    def add_control_callbacks(self, linked_instance: BaseInstance) -> None:
        linked_instance.event_handler.register_keypressed_callback(Controls.UP, self.up)
        linked_instance.event_handler.register_keypressed_callback(Controls.DOWN, self.down)
        linked_instance.event_handler.register_keypressed_callback(Controls.LEFT, self.left)
        linked_instance.event_handler.register_keypressed_callback(Controls.RIGHT, self.right)
        linked_instance.event_handler.register_keypressed_callback(Controls.BOOST, self.boost)
