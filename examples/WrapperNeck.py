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
from colorama import Fore, Back, Style


class WrapperNeck(gym.Env):
    def __init__(self,render):
        #self.state = None
        self.target =  np.random.uniform(low = -0.5, high= 0.5, size=(2,)) # Target objetivo
        self.steps = 8

        #? Create action space (Action -> pitch-roll // Observation -> pitch-roll)
        self.action_space = spaces.Box(low=np.array([-1,-1]), high=np.array([1,1]),dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([-0.5,-0.5]),high=np.array([0.5,0.5]), dtype=np.float32)

        self.render = render
        self.PathLocated = "/home/humasoft/Escritorio/Py-C/softNeck/build"

        #? Generation of all the paths to use ctypes ;)

            #* Start motors 
        self.StartMotors = self.PathLocated + "/startMotors"
        self.StopMotors = self.PathLocated + "/stopMotors"

            #* Go Homeimport os
        self.GoHome = self.PathLocated + "/goHome"

            #* Set Position
        self.SetPosition = self.PathLocated + "/setPosition"

        #? Create YARP communication
        yarp.Network.init()
        self.pin = yarp.BufferedPortBottle()
        self.pout = yarp.BufferedPortBottle()

        self.pin.open("/pin")
        self.pout.open("/pout")

        yarp.Network.connect("/pout", "/receiver")
        yarp.Network.connect("/sender", "/pin" )

        if not yarp.Network.isConnected("/pout", "/receiver"):
            print("Error connection witch /pout /receiver")
            exit()

        if not yarp.Network.isConnected("/sender", "/pin"):
            print("Error connection witch /pin, /sender")
            exit()

        self.bout = yarp.Bottle()
        self.bout = self.pout.prepare()
        self.bin = yarp.Bottle()
        
        


    
    #? Define the reward
    def rewardFunction(self,obs,target):
        # ver que función de reward le ponemos
        print(target)
        print(obs)
        reward = np.linalg.norm(target - obs)
        return reward

    #? Define the step
    def step(self,action):
        print(Fore.BLACK + Back.LIGHTYELLOW_EX)
        done = False
        reward=0
        Inpitch = str(action[0] * 40)
        Inroll = str(action[1] * 40)

        self.steps-=1
        print("STEP: {}".format(self.steps))

        print("Inpitch :{}".format(Inpitch))
        print("Inroll :{}".format(Inroll))

        # hacemos la llamada a la funció nque relaciona el motor 1 y 2 con el 3
        """ motor1, motor2, motor3 = self.motorEstimation(Inpitch,Inroll) """

        # Generamos la accion en el cuello
        os.system(self.SetPosition +" "+ Inpitch+ " "+ Inroll)
        time.sleep(2)
        obs = np.fromstring(self.message("sendme"),dtype=float, sep= ' ')
        #print(type(obs))

        # Enviamos los valores del motor al robot real
        """ obs = self.libc.funcion(motor1,motor2,motor3) # Devolvemos la observacion """
        
        reward = self.rewardFunction(obs,self.target)
        #self.reward = self.reward + reward_state
        print(">>>> Reward:{}".format(reward))

        if reward < 0.1: # errores en radianes
            done = True
            
        else:
            done = False

        if self.steps <=0:
            done= True
            
        else:
            done = False
        print(Style.RESET_ALL)
        return obs,reward,done,{}
    
    #? Define the target for each iteration
    def reset(self,initial = False):
        
        print("RESETTTTTTTTTTTTT")
        time.sleep(2)
        if initial:
            os.system(self.StartMotors)
            #os.system(self.GoHome)
            time.sleep(1)
            os.system(self.SetPosition +" "+ "0"+ " "+ "0")
        else:
            os.system(self.SetPosition +" "+ "0"+ " "+ "0")
            time.sleep(1)

        
        self.steps = 8
        self.target = np.random.uniform(low = -0.5, high= 0.5, size=(2,)) # Estimamos el punto target al que queremos ir   random.uniform(-45,45),random.uniform(-45,45)
        print("Target :{}".format(self.target))
        #print("Target type :{}".format(type(target)))
        observation = np.fromstring(self.message("sendme"),dtype=float, sep= ' ')
        return observation

    
    #? Define function that generates the message to YARP
    def message(self,message):
        self.bout = yarp.Bottle()
        self.bout = self.pout.prepare()
        self.bin.clear()
        time.sleep(1)
        self.bout.addString(message)
        self.pout.write()
        print("Sending [%s]"% self.bout.toString())
        self.bin = self.pin.read()
        print(self.bin.toString())
        valor = self.bin.toString()
        self.bout.clear()
        return valor




#? Register the environment 
register(
    id = 'WrapperNeck-v1',
    entry_point= 'WrapperNeck:WrapperNeck'
)