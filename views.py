# -*- coding: utf-8 -*-
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


import abc


class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_is_correct(self) -> bool:
        if 0 <= self.x <= 8 and 0 <= self.y <= 8:
            return True
        else:
            return False

    def change_to_numbers(self):
        dictionary = {''}


class Figure(abc.ABC):
    """
    metoda list_available_moves() zwraca dostęne ruchy
    metoda validate_move(dest_field) informuje, czy ruch na wskazane pole jest możliwy
    """

    @abc.abstractmethod
    def __init__(self, field):
        self.field = field

    @abc.abstractmethod
    def list_available_moves(self):
        pass

    @abc.abstractmethod
    def validate_move(self):
        pass
