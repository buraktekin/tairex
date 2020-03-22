#! -*- coding: utf-8 -*-

"""Implementation of agent that will play the game"""

from interface import Interface
import time


class Agent(object):
    """Class Implementation"""

    def __init__(self, interface):
        """Constructor"""
        self._interface = interface
        self.jump()
        time.sleep(.5)

    def jump(self):
        self._interface.jump()

    def duck(self):
        self._interface.duck()

    def is_dino_crashed(self):
        return self._interface.is_dino_crashed()

    def is_dino_running(self):
        return self._interface.is_dino_running()
