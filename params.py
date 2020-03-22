#! -*- coding: utf-8 -*-
"""
# parameters would be used during training the RL system
"""

# game parameters
GAMMA = 0.99  # decay rate of past observations original 0.99
OBSERVATION = 50000.  # timesteps to observe before training
EXPLORE = 100000  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001  # final value of epsilon
INITIAL_EPSILON = 0.1  # starting value of epsilon
REPLAY_MEMORY = 50000  # number of previous transitions to remember
BATCH = 32  # size of minibatch
FRAME_PER_ACTION = 1

# Chrome v80 https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/
# to get other versions please check: https://chromedriver.chromium.org/downloads
