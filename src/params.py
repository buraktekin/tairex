#! -*- coding: utf-8 -*-

"""
# ALL PARAMETERS
"""

# Game Parameters
ACTIONS = 2  # Run & Jump
GAMMA = 0.99  # decay rate of past observations original 0.99
OBSERVATION = 100.  # timesteps to observe before training
EXPLORE = 100  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001  # final value of epsilon
INITIAL_EPSILON = 0.1  # starting value of epsilon
REPLAY_MEMORY = 5000  # number of previous transitions to remember
BATCH = 32  # size of minibatch
FRAME_PER_ACTION = 1
LEARNING_RATE = 0.001
IMG_ROWS = 40
IMG_COLS = 20
IMG_CHANNELS = 4

# Paths
GAME_URL = "chrome://dino"
CHROME_DRIVER_PATH = "../chromedriver"
LOG_PATH = "./logs/"
LOSS_FILE_PATH = "./logs/loss_df.csv"
ACTIONS_FILE_PATH = "./logs/actions_df.csv"
SCORES_FILE_PATH = "./logs/scores_df.csv"
Q_VALUE_FILE_PATH = "./logs/q_values.csv"
MODEL_H5 = "./model/model.h5"
MODEL_JSON = "./model/model.json"

# My version of Chrome is v80 https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/
# to get other versions please check: https://chromedriver.chromium.org/downloads
# Normally it is automatically detecting the browser version now. However, in case of
# a compatiblity issues, you may want to check the links given above.
