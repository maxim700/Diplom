import numpy as np
import random
from collections import deque
from ExpBank import expline, ExpBank

from keras import Model, Sequential
from keras.layers import Dense, Embedding, Reshape
from keras.optimizers import Adam
from TAGS import TAGS


class Agent:
    def __init__(self, enviroment, optimizer, bank, key):

        # Initialize atributes
        self._state_size = 225*len(TAGS) #24*60/45*7 + 1 * TAGS
        self._action_size = 3 #Количество дней, на которое дается рекомендация
        self._optimizer = optimizer

        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.5

        #user id
        self.key = key

        #bank
        self.bank = bank

        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()

    def store(self, state, action, reward):#, next_state, terminated
        self.bank.add_exp(expline(self.key, 0.0, state, reward, action))#

    def _build_compile_model(self):
        model = Sequential()
        model.add(Embedding(self._state_size, 10, input_length=1))#Количество состояний среды сжимается до 10 (n) (А почему?)
        model.add(Reshape((10,)))
        model.add(Dense(50, activation='relu')) #Достаточноли 3х слоев?
        model.add(Dense(50, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))    

        model.compile(loss='mse', optimizer=self._optimizer)
        return model

    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def normal(self, state):
        norm = np.zeros(len(state)*len(TAGS))
        pos = 0
        for i,line in enumerate(state):
            if line == None:
                for tag in TAGS:
                    norm[pos] = 0
                    pos += 1
            else:
                print(line)
                for tag in TAGS:
                    if tag in line:
                        norm[pos] = 1
                    else:
                        norm[pos] = 0
                    pos += 1
                #norm[i] = np.array([1 if tag in line else 0 for tag in TAGS])
        return norm

    def balans_action(self, state):
        statepart = np.array_split(self.normal(state[:-1*len(TAGS)]),7)[4:]
        return np.argmin([np.sum(i) for i in statepart])#Где-то есть косяк в подсчетах todo поправить

    #В функции выбирается, делать действие рандомно или воспользоваться опытом
    #В нашем случае нужно будет воспользоваться опытом, если он есть
    #Если похожего нету, то мы делаем действие псевдорандомно, то бишь стремим его к балансу
    def act(self, state):
        exp = self.bank.find(self.key, state, self.epsilon)
        print(exp)
        if exp is None:
            action = 0#action = self.balans_action(state)
            newexp = expline(key = self.key,
                              data = state,
                              action = action,
                              priority = 0,
                              cost = 0
                              )
            self.bank.add_exp(newexp)
            return (action, newexp.id)
        action = np.argmax(self.q_network.predict(self.normal(state))[0])
        newexp = expline(key=self.key,
                          data=state,
                          action=action,
                          priority=expline.priority,
                          cost=0
                          )
        self.Bank.add_exp(newexp)
        expline.priority += 0.05
        return (action, newexp.id)


    def retrain(self,expid, user_reward):
        exp = self.bank.get(self.key,expid)
        key, state, action, priority, reward = exp.tuple()
        print(state)
        target = self.q_network.predict(self.normal(state))
        print("########TARGET############")
        print(target)
        target[0][action] = reward + user_reward*0.1
        self.q_network.fit(state, target, epochs=1, verbose=0)
        exp.priority += np.abs(user_reward - reward)

