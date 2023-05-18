import gym
import numpy as np
from WrapperNeck import WrapperNeck

# Generation of the environment
env = gym.make('WrapperNeck-v1',render='human')
reset = env.reset(initial=True) # El resto de Reset initial = False
print(reset)