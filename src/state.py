# -*- coding: utf-8 -*-
from typing import Tuple, ByteString
from src.helpers import show_img
from src.helpers import grab_screen

import src.params as param
import pandas as pd
import numpy as np
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
        actions = actions.astype(int)
        action_index = np.argmax(actions, axis=None)
        self.actions_df.loc[len(self.actions_df)] = action_index
        score = self._game.get_score()
        high_score = self._game.get_highest_score()
        is_game_over = self._agent.is_dino_crashed()
        is_dino_jumped = self._agent.is_dino_jumped()
        reward = 0.01 * score

        if is_game_over:
            self.scores_df.loc[len(self.loss_df)] = score
            self._game.restart()
            reward = -10 / score if (high_score >= score) else -5 / score
            is_game_over = True
        else:
            # if 1 (jump) || 0 (Run) assigned to agent
            if action_index == 1:
                reward = 0.1 * score
                self._agent.jump()

        image = grab_screen(self._game.driver)
        self._screen.send(image)

        return image, reward, is_game_over, is_dino_jumped
