# -*- coding: utf-8 -*-

import abc


class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.letter_dictionary = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
        self.is_empty = True
        self.figure_code = 0
        self.field_name = self.count_field_name()

    def check_is_correct(self) -> bool:
        if 0 <= self.x <= 8 and 0 <= self.y <= 8:
            return True
        else:
            return False

    def change_to_numbers(self, letter):
        return self.letter_dictionary[letter]

    def change_to_letters(self, number):
        number += 65
        letter = chr(number)
        return letter

    def count_field_name(self):
        letter = self.change_to_letters(self.y)
        return letter + self.x


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


class King(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 100

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass


class Queen(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 10

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass


class Rook(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 5

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass


class Bishop(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 4

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass


class Knight(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 3

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass


class Pawn(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 1

    def list_available_moves(self):
        pass

    def validate_move(self):
        pass
