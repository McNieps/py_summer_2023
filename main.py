import asyncio
import numpy
import pymunk
import pygame

from isec.app import App
from game.instances.tutorial_instance import TutorialInstance


async def main():
    App.init("game/assets/")
    await TutorialInstance().execute()


asyncio.run(main())
