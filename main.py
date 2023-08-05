import asyncio
import numpy
import pymunk
import pygame
import math
import time

from isec.app import App
from game.instances.menu import Menu


async def main():
    App.init("game/assets/")
    await Menu().execute()


asyncio.run(main())
