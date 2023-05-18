import gym
from gym import spaces
from gym.envs.registration import register
import numpy as np
import sys,platform
import ctypes, ctypes.util
import random
import yarp #! Include YARP for IMU constan comunication
import os
import time

class WrapperNeck(gym.Env):
    def __init__(self,render):
        self.state = None
        self.target = None # Target objetivo
        self.lengths = None
        self.lg0 = 0.003 # Pretension de los cables
        self.radio = 0.0075

        #? Create action space (Action -> pitch-roll // Observation -> pitch-roll)
        self.action_space = spaces.Box(low=np.array([-40,-40]), high=np.array([40,40]),dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([-np.inf]*2),high=np.array([np.inf]*2),shape=(2,), dtype=np.float32)

        self.render = render
        self.PathLocated = "/home/humasoft/Escritorio/Py-C/softNeck/build"

        #? Generation of all the paths to use ctypes ;)
            #* Prueba de la IMU (funciona bien jejejej)
        """ self.pathAdrian = ctypes.util.find_library(self.PathLocated + "/AdrianImu")
        self.AdriImu = ctypes.CDLL(self.pathAdrian) """

            #* Start motors 
        self.StartMotors = self.PathLocated + "/startMotors"

            #* Go Homeimport os

        self.GoHome = self.PathLocated + "/goHome"

            #* Set Position
        self.SetPosition = self.PathLocated + "/setPosition"

    
    #? Define the reward
    def reward(self,obs,target):
        # ver que función de reward le ponemos
        reward = np.linalg(target - obs)
        return reward

    #? Define the step
    def step(self,action):
        Inpitch = action[0]
        Inroll = action[1]

        # hacemos la llamada a la funció nque relaciona el motor 1 y 2 con el 3
        motor1, motor2, motor3 = self.motorEstimation(Inpitch,Inroll)

        # Enviamos los valores del motor al robot real
        obs = self.libc.funcion(motor1,motor2,motor3) # Devolvemos la observacion
        reward_state = self.reward(obs,self.target)
        reward: self.reward = self.reward + reward_state

        if self.reward >= 5  or reward_state < 0.01: # errores en radianes
            done = True
        else:
            done = False

        return obs,reward,done,{}
    
    #? Define the target for each iteration
    def reset(self,initial = True):
        if initial:
            os.system(self.StartMotors)
        else:
            os.system(self.SetPosition +" "+ "0"+ " "+ "0")

        os.system(self.GoHome)
        time.sleep(1)
        os.system(self.SetPosition +" "+ "0"+ " "+ "0")
        self.reward = 0
        target: self.target = (random.uniform(-45,45),random.uniform(-45,45)) # Estimamos el punto target al que queremos ir
        """ self.AdriImu.main() """
        return target
    
    #? Define function that estimate motor3

    def motorEstimation(self,pitch,roll):
        #Realizamos el proceso pertinente
        self.lengths[0] = -0.001* (pitch/1.5);
        self.lengths[1] =  0.001* (pitch/3 - roll/1.732);
        self.lengths[2] =  0.001* (pitch/3 + roll/1.732);
        
        # Trasnformation 
        m1: self.motor[0] = (self.lg0-self.lengths[0])/self.radio;
        m2: self.motor[1] = (self.lg0-self.lengths[1])/self.radio;
        m3: self.motor[2] = (self.lg0-self.lengths[2])/self.radio;
        return m1,m2,m3




#? Register the environment 
register(
    id = 'WrapperNeck-v1',
    entry_point= 'WrapperNeck:WrapperNeck'
)