# -*- coding: utf-8 -*-
from typing import Tuple, ByteString
from src.helpers import show_img
from src.helpers import grab_screen

import src.params as param
import pandas as pd
import os


class State(object):
    """State Module Implementation"""
    loss_df = pd.read_csv(param.LOSS_FILE_PATH) \
        if os.path.isfile(param.LOSS_FILE_PATH) \
        else pd.DataFrame(columns=['loss'])

    scores_df = pd.read_csv(param.SCORES_FILE_PATH) \
        if os.path.isfile(param.LOSS_FILE_PATH) \
        else pd.DataFrame(columns=['scores'])

    actions_df = pd.read_csv(param.ACTIONS_FILE_PATH) \
        if os.path.isfile(param.ACTIONS_FILE_PATH) \
        else pd.DataFrame(columns=['actions'])

    q_values_df = pd.read_csv(param.ACTIONS_FILE_PATH) \
        if os.path.isfile(param.Q_VALUE_FILE_PATH) \
        else pd.DataFrame(columns=['qvalues'])

    def __init__(self, agent, game):
        """Constructor"""
        self._agent = agent
        self._game = game
        self._screen = show_img()
        self._screen.__next__()  # execute coroutine

    def state(self, actions) -> Tuple[ByteString, int, bool]:
        self.actions_df.loc[len(self.actions_df)] = actions[1]
        score = self._game.get_score()
        high_score = self._game.get_highest_score()
        reward = 0
        is_game_over = False

        # if 1 (jump) assigned to agent
        reward_factor = abs(score - high_score)
        if actions[1] == 1:
            self._agent.jump()
            reward = 0.5
        elif actions[1] == 0:
            reward = 0.45
        elif actions[1] == 2:
            self._agent.duck()
            reward = 0.5

        image = grab_screen(self._game.driver)
        self._screen.send(image)

        if self._agent.is_dino_crashed():
            self.scores_df.loc[len(self.loss_df)] = score
            self._game.restart()
            reward = -1
            is_game_over = True

        return image, reward, is_game_over
