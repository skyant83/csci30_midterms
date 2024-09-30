#!/usr/bin/env python3
from ringbuffer import *
import numpy as np
import random

class GuitarString:
    FADE_SECONDS = 4
    FADE_TICK_THRESHOLD = FADE_SECONDS * 44100

    def __init__(self, frequency: float):
        '''
        Create a guitar string of the given frequency, using a sampling rate of 44100 Hz
        '''
        # computes the max capacity of the ring buffer based on the frequency
        self.capacity = int(-(-44100 // frequency))
        # constructs the ring buffer object
        self.buffer = RingBuffer(self.capacity)
        # intializes counter for tick activations and sets the isVibrating to false
        self.tickTime = 0
        self.isVibrating = False
        for _ in range(self.capacity):
            self.buffer.enqueue(0)

    @classmethod
    def make_from_array(cls, init: list[int]):
        '''
        Create a guitar string whose size and initial values are given by the array `init`
        '''
        # create GuitarString object with placeholder freq
        stg = cls(1000)

        stg.capacity = len(init)
        stg.buffer = RingBuffer(stg.capacity)
        for x in init:
            stg.buffer.enqueue(x)
        return stg

    def pluck(self):
        '''
        Set the buffer to white noise
        '''
        self.tickTime = 0
        self.isVibrating = True
        for _ in range(self.capacity):
            self.buffer.dequeue()
            self.buffer.enqueue(random.uniform(-0.5, 0.5))

    def tick(self):
        '''
        Advance the simulation one time step by applying the Karplus--Strong update
        '''
        tick_1 = self.buffer.dequeue()
        tick_2 = self.buffer.peek()
        curSample = 0.996 * 0.5 * (tick_1 + tick_2)
        self.buffer.enqueue(curSample)
        self.tickTime += 1
        if self.time() > self.FADE_TICK_THRESHOLD:
            self.is_active = False

    def sample(self) -> float:
        '''
        Return the current sample
        '''
        return self.buffer.peek()
    
    def time(self) -> int:
        '''
        Return the number of ticks so far
        '''
        return self.tickTime