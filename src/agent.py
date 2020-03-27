#! -*- coding: utf-8 -*-

"""The Agent that will play the game"""

import time


class Agent(object):
    """Agent Module Implementation"""

    def __init__(self, interface):
        """Constructor"""
        self._interface = interface
        self.jump()
        time.sleep(.5)

    def jump(self) -> None:
        self._interface.jump()

    def duck(self) -> None:
        self._interface.duck()

    def is_dino_crashed(self) -> bool:
        return self._interface.is_dino_crashed()

    def is_dino_running(self) -> bool:
        return self._interface.is_dino_running()

    def is_dino_jumped(self) -> bool:
        return self._interface.is_dino_jumped()
