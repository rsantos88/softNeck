import gym
import numpy as np
from WrapperNeck import WrapperNeck
from colorama import Fore, Back, Style

from stable_baselines3 import PPO
from stable_baselines3.ppo.policies import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
import os

# Generation of the environment

""" print(Fore.BLACK + Back.LIGHTYELLOW_EX)
Style.RESET_ALL"tmp/"
print(Style.RESET_ALL)
print("PRUEBA DESCOLORADO") """

env = gym.make('WrapperNeck-v1',render='human')
log_path =os.path.join("Training","Logs")
model = PPO(MlpPolicy,env,verbose = 1,n_steps=8,batch_size=2,tensorboard_log=log_path) # n_steps numero de steps para actualizar la politica del PPO (no hace reset del entorno)
reset = env.reset(initial=True) # El resto de Reset initial = False
model.learn(total_timesteps=16,progress_bar=True) # Numero de iteraciones = total_timesteps/n_steps


#print(training_logs_path)
#!tensorboard --logdir={training_logs_path}


#mean_reward,std_reward = evaluate_policy(model, model.get_env(),n_eval_episodes=10)

""" action = (20,20)
env.step(action) """