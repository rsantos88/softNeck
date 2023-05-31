import gym
import numpy as np
from WrapperNeck import WrapperNeck

from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy

# Generation of the environment
env = gym.make('WrapperNeck-v1',render='human')
model = PPO(MlpPolicy,env,verbose = 1, n_epochs=2)
#reset = env.reset(initial=True) # El resto de Reset initial = False
model.learn(total_timesteps=10,progress_bar=True)

#mean_reward,std_reward = evaluate_policy(model, model.get_env(),n_eval_episodes=10)

""" action = (20,20)
env.step(action) """