# -*- coding: utf-8 -*-
from src.helpers import show_img
from src.helpers import grab_screen

import src.params as param
import pandas as pd


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

    def __init__(self, agent, game):
        """Constructor"""
        self._agent = agent
        self._game = game
        self._screen = show_img()
        self._screen.__next__()  # execute coroutine

    def state(self, actions) -> Tuple:
        actions_df.loc[len(actions_df)] = actions[1]
        score = self._game.score()
        reward = score / 100
        is_game_over = False

        if actions[1] == 1:
            self._agent.jump()
            reward = score / 110
        image = grab_screen()
        self._screen.send(image)

        if self._agent.is_dino_crashed():
            scores_df.loc[len(loss_df)] = score
            self._game.restart()
            reward = -11/score
            is_game_over = True

        return image, reward, is_game_over
