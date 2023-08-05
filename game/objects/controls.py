import pygame


class Controls:
    FORWARD = pygame.K_z
    BACKWARD = pygame.K_s
    LEFT = pygame.K_q
    RIGHT = pygame.K_d
    UP = pygame.K_SPACE
    DOWN = pygame.K_LCTRL
    BOOST = pygame.K_LSHIFT
    PAUSE = pygame.K_ESCAPE
    DEBUG = pygame.K_F3
    DEBUG_COLLISION = pygame.K_F4
    DEBUG_PHYSICS = pygame.K_F5
    DEBUG_FPS = pygame.K_F6
    DEBUG_CAMERA = pygame.K_F7

    KEY_NAMES = {vars(pygame)[key]: key for key in vars(pygame) if key.startswith("K_")}

    @classmethod
    def change_bind(cls, action, key):
        if key not in cls.KEY_NAMES:
            raise ValueError("Key not found")

        if action not in vars(cls):
            raise ValueError("Action not found")

        setattr(cls, action, key)

    @classmethod
    def check_if_bound(cls, key):
        if key not in cls.KEY_NAMES:
            raise ValueError("Key not found")

        for action_name, action_key in vars(cls).items():
            if action_key == key:
                return action_name

        return None

    @classmethod
    def get_key_name(cls, key):
        if key not in cls.KEY_NAMES:
            raise ValueError("Key not found")

        return cls.KEY_NAMES[key]

    @classmethod
    def get_key(cls, action):
        if action not in vars(cls):
            raise ValueError("Action not found")

        return getattr(cls, action)
