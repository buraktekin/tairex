#! -*- coding: utf-8 -*-

from src.interface import Interface
from src.agent import Agent
from src.state import State
from src.model import NNModel

import os


def run(observe=False):
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    if not os.path.exists('./model'):
        os.makedirs('./model')

    interface = Interface()
    agent = Agent(interface)
    state = State(agent, interface)
    nn = NNModel()
    model = nn.build_model()

    try:
        nn.trainNetwork(model, state, observe=observe)
    except StopIteration:
        print("No model")
        interface.close()


run(False)
