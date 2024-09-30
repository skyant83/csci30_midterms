#!/usr/bin/env python3

class RingBuffer:
    def __init__(self, capacity: int):
        '''
        Create an empty ring buffer, with given max capacity
        '''
        self.MAX_CAP = capacity
        self._front = 0
        self._rear = 0 
        self.buffer = [None] * self.MAX_CAP
        self._size = 0

    def size(self) -> int:
        '''
        Return number of items currently in the buffer
        '''
        return self._size

    def is_empty(self) -> bool:
        '''
        Is the buffer empty (size equals zero)?
        '''
        return self.size() == 0
        
    def is_full(self) -> bool:
        '''
        Is the buffer full (size equals capacity)?
        '''
        return self.size() == self.MAX_CAP

    def enqueue(self, x: float):
        '''
        Add item `x` to the end
        '''
        if (self.size() < self.MAX_CAP):
            self.buffer[self._rear] = x
            self._rear = (self._rear + 1) % self.MAX_CAP
            self._size += 1
        else:
            raise RingBufferFull

    def dequeue(self) -> float:
        '''
        Return and remove item from the front
        '''
        if (self.size() > 0):
            oldest_item = self.buffer[self._front]
            self.buffer[self._front] = None
            self._front = (self._front + 1) % self.MAX_CAP
            self._size -= 1
            return oldest_item
        else:
            raise RingBufferEmpty

    def peek(self) -> float:
        '''
        Return (but do not delete) item from the front
        '''
        reqItem = self.buffer[self._front]
        if (reqItem is not None):
            return self.buffer[self._front]
        else:
            raise RingBufferEmpty


class RingBufferFull(Exception):
    '''
    The exception raised when the ring buffer is full when attempting to
    enqueue.
    '''
    pass

class RingBufferEmpty(Exception):
    '''
    The exception raised when the ring buffer is empty when attempting to
    dequeue or peek.
    '''
    pass
