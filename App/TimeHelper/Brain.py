import numpy as np
import random
from collections import deque
from ExpBank import expline, ExpBank

from keras import Model, Sequential
from keras.layers import Dense, Embedding, Reshape
from keras.optimizers import Adam


class Agent:
    def __init__(self, enviroment, optimizer, bank, key):

        # Initialize atributes
        self._state_size = 96#len(enviroment)#Сюда подается количество состояний среды (как их получить)
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

    #В функции выбирается, делать действие рандомно или воспользоваться опытом
    #В нашем случае нужно будет воспользоваться опытом, если он есть
    #Если похожего нету, то мы делаем действие псевдорандомно, то бишь стремим его к балансу
    def act(self, state):
        if self.bank.find(self.key, state, self.epsilon) is None:
            return np.random.randint(3)#pass # todo действие по алгоритму # регрессионная модель

        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])


    def retrain(self, user_reward):
        minibatch = self.bank.get_exp(self.key)
        if not(minibatch is None):
            for exp in minibatch:
                key, priority, state, reward, action = exp.tuple()

                target = self.q_network.predict(state)
                target[0][action] = reward + user_reward*0.1
                self.q_network.fit(state, target, epochs=1, verbose=0)

                exp.priority += np.abs(user_reward - reward)

