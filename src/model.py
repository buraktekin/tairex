#! -*- coding: utf-8 -*-
"""Implement the Neural Network Model"""

# Neural Network imports: keras
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import Adam, SGD
from keras.callbacks import TensorBoard
from IPython.display import clear_output
from collections import deque
from src.helpers import load_logs, save_logs

import src.params as param
import numpy as np
import random
import json
import time
import os


class NNModel(object):
    """
    A Sequential Convolutional Neural Network model:
    - 3 Conv2D
    - @activation: 'relu'
    - @maxpooling: none
    - @optimizer: Adam || SGD
    - @loss: Mean Squared Error (MSE)
    """

    def __init__(self):
        print("Initializing cache")
        self.init_cache()
        # self.build_model()
        # self.trainNetwork()

    def init_cache(self):
        """Initialize caching to avoid training progress start from scratch"""
        save_logs(param.INITIAL_EPSILON, "epsilon")
        t = 0
        save_logs(t, "time")
        D = deque()
        save_logs(D, "deque")

    def build_model(self):
        print("Model building is in progress...")
        model = Sequential()
        model.add(
            Conv2D(
                filters=32,
                kernel_size=(8, 8),
                strides=(4, 4),
                padding='same',
                input_shape=(param.IMG_COLS, param.IMG_ROWS, param.IMG_CHANNELS)
            )
        )
        model.add(Activation('relu'))
        model.add(Conv2D(64, (4, 4), strides=(2, 2), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dense(param.ACTIONS))  # Num of actions: jump & duck
        adam = Adam(lr=param.LEARNING_RATE)
        model.compile(loss='mse', optimizer=adam)
        print("Model is created")

        print("Saving the model...")
        if not os.path.isfile(param.LOSS_FILE_PATH):
            model.save_weights('../model.h5')
        print("Model saved!")

        model.summary()
        return model

    def trainNetwork(self, model, game_state, observe=False):
        '''
        main training module
        Parameters:
        * @model => The Model to be trained
        * @state => Game State module with access to game environment and dino
        * @observe => flag to decide weight update
        '''

        last_time = time.time()
        # store the previous observations in replay memory
        D = load_logs("deque")  # load from file system
        # get the first state by doing nothing
        do_nothing = np.zeros(param.ACTIONS)
        do_nothing[0] = 1

        x_t, r_0, is_game_over = game_state.state(do_nothing)  # get next step after performing the action
        s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)  # stack 4 images to create placeholder input
        s_t = s_t.reshape(1, s_t.shape[0], s_t.shape[1], s_t.shape[2])  # 1*20*40*4
        initial_state = s_t

        if observe:
            OBSERVE = 999999999  # We keep observe, never train
            epsilon = param.FINAL_EPSILON
        else:  # We go to training mode
            OBSERVE = param.OBSERVATION
            epsilon = load_logs("epsilon")

        try:
            print("Loading weights...")
            model.load_weights("../model.h5")
            print("Done.")
        except FileNotFoundError as fnf:
            print(fnf)

        adam = Adam(lr=param.LEARNING_RATE)
        model.compile(loss='mse', optimizer=adam)

        t = load_logs("time")  # time checkpoint
        while (True):
            # choose an action epsilon greedy
            action_index = 0
            actions_t = np.zeros([param.ACTIONS])
            if t % param.FRAME_PER_ACTION == 0:
                if random.random() <= epsilon:  # randomly explore an action
                    print("----------Random Action----------")
                    action_index = random.randrange(param.ACTIONS)
                    actions_t[action_index] = 1
                else:  # predict the output
                    q = model.predict(s_t)  # input a stack of 4 images, get the prediction
                    max_Q = np.argmax(q)         # chosing index with maximum q value
                    action_index = max_Q
                    actions_t[action_index] = 1  # o=> do nothing, 1=> jump

            # We reduced the epsilon (exploration parameter) gradually
            if epsilon > param.FINAL_EPSILON and t > OBSERVE:
                epsilon -= (param.INITIAL_EPSILON - param.FINAL_EPSILON) / param.EXPLORE

            # run the selected action and observed next state and reward
            x_t1, reward_t, is_game_over = game_state.state(actions_t)
            print(f'fps: {1 / (time.time()-last_time)}')  # helpful for measuring frame rate
            last_time = time.time()
            x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1)  # 1x20x40x1
            s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3)  # append the new image to input stack and remove the first one

            # store the transition in D
            D.append((s_t, action_index, reward_t, s_t1, is_game_over))
            if len(D) > param.REPLAY_MEMORY:
                D.popleft()

            # only train if done observing
            loss = 0
            Q_sa = 0
            if t > OBSERVE:
                # sample a minibatch to train on
                minibatch = random.sample(D, param.BATCH)
                inputs = np.zeros((param.BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))  # 32, 20, 40, 4
                targets = np.zeros((inputs.shape[0], param.ACTIONS))  # 32, 2

                # Now we do the experience replay
                for i in range(0, len(minibatch)):
                    state_t = minibatch[i][0]    # 4D stack of images
                    action_t = minibatch[i][1]  # This is action index
                    reward_t = minibatch[i][2]  # reward at state_t due to action_t
                    state_t1 = minibatch[i][3]  # next state
                    is_game_over = minibatch[i][4]  # wheather the agent died or survided due the action

                    # predictions by the states
                    inputs[i:i + 1] = state_t
                    targets[i] = model.predict(state_t)
                    Q_sa = model.predict(state_t1)  # stochastic transitions and rewards

                    if is_game_over:
                        targets[i, action_t] = reward_t  # if terminated, only equals reward
                    else:
                        targets[i, action_t] = reward_t + param.GAMMA * np.max(Q_sa)

                loss += model.train_on_batch(inputs, targets)
                game_state.loss_df.loc[len(game_state.loss_df)] = loss
                game_state.q_values_df.loc[len(game_state.q_values_df)] = np.max(Q_sa)

            # state transition
            s_t = initial_state if is_game_over else s_t1
            t = t + 1

            # save progress every 1000 iterations
            if t % 1000 == 0:
                print("Now we save model")
                game_state._game.pause()  # pause game while saving to filesystem
                model.save_weights("../model.h5", overwrite=True)
                save_logs(D, "deque")  # saving episodes
                save_logs(t, "time")  # caching time steps
                save_logs(epsilon, "epsilon")  # cache epsilon to avoid repeated randomness in actions
                game_state.loss_df.to_csv("../logs/game_state.loss_df.csv", index=False)
                game_state.scores_df.to_csv("../logs/game_state.scores_df.csv", index=False)
                game_state.actions_df.to_csv("../logs/game_state.actions_df.csv", index=False)
                game_state.q_values_df.to_csv(param.Q_VALUE_FILE_PATH, index=False)
                with open("../model.json", "w+") as outfile:
                    json.dump(model.to_json(), outfile)
                clear_output()
                game_state._game.resume()
            # print info
            state = ""
            if t <= OBSERVE:
                state = "observe"
            elif t > OBSERVE and t <= OBSERVE + param.EXPLORE:
                state = "explore"
            else:
                state = "train"

            print(
                "TIMESTEP: ", t,
                " / STATE: ", state,
                " / EPSILON: ", epsilon,
                " / ACTION: ", action_index,
                " / REWARD: ", reward_t,
                " / Q_MAX: ", np.max(Q_sa),
                " / Loss: ", loss
            )

        print("Episode finished!")
        print("************************")
