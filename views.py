# -*- coding: utf-8 -*-

import abc


class Figure(abc.ABC):
    """

    """

    @abc.abstractmethod
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abc.abstractmethod
    def list_available_moves(self):
        pass

    @abc.abstractmethod
    def validate_move(self):
        pass
