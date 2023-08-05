import pygame
import math

from isec.app import Resource
from isec.environment import Entity, Sprite, EntityScene
from isec.environment.position import PymunkPos
from isec.instance import BaseInstance

from game.objects.controls import Controls


class Player(Entity):
    def __init__(self,
                 linked_scene: EntityScene) -> None:

        self.linked_scene = linked_scene

        position = PymunkPos(position=(100, 100))
        player_surface = Resource.image["game"]["submarine_1"]
        position.create_rect_shape(player_surface, density=50, radius=-1.5)

        sprite = Sprite(player_surface, rendering_technique="rotated")

        super().__init__(position, sprite)

        self.sprite_flipped = False
        self.velocity = 1000000
        self.exploration_velocity = 1000000
        self.chase_velocity = 2500000

        self.pressed = {"up": False, "down": False, "left": False, "right": False, "boost": False}

    def update(self,
               delta: float) -> None:

        super().update(delta)
        self.position.body.angular_velocity *= 0.1 ** delta

        angle_difference = self.get_angle_cursor_player()

        self.rotate_player(angle_difference, delta)
        self.move_player(delta)

        self.flip_sprite()

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

        torque = angle_difference * delta * 10

        self.position.body.apply_impulse_at_world_point((0, torque), (10, 0))
        self.position.body.apply_impulse_at_world_point((0, torque), (-10, 0))

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
            return

        input_vec.normalize_ip()
        input_angle = (-input_vec.angle_to((1, 0))) % 360
        difference = (input_angle - forward_angle) % 360
        if difference > 180:
            difference -= 360

        speed = input_vec * delta * self.velocity
        if -90 < difference < 90:
            mult = 1+math.cos(math.radians(difference))
            if self.pressed["boost"]:
                mult *= 5
                print("HIIIIAAA")
            speed *= mult

        self.position.body.apply_force_at_world_point(tuple(speed), tuple(self.position.position))

        self.pressed = {"up": False, "down": False, "left": False, "right": False, "boost": False}

    def flip_sprite(self) -> None:
        if (90 < self.position.a < 270) and not self.sprite_flipped:
            self.sprite_flipped = True
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)
        elif (self.position.a < 90 or self.position.a > 270) and self.sprite_flipped:
            self.sprite_flipped = False
            self.sprite.surface = pygame.transform.flip(self.sprite.surface, False, True)

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
