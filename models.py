# -*- coding: utf-8 -*-

import abc


class Field:
    def __init__(self, x, y, is_empty=True, figure_code=0, is_black=False):
        """
        :param x: numer wiersza
        :param y: numer kolumny
        :param is_empty: czy pole jest zajęte
        :param figure_code: 1, 3, 4, 5, 10, 100
        :param is_black: czy figura zajmująca pole jest czarna
        """
        self.x = x
        self.y = y
        self.letter_dictionary = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
        self.field_name = self.count_field_name()

        self.is_empty = is_empty
        self.figure_code = figure_code

        self.is_black = is_black

    def check_is_correct(self) -> bool:
        if 1 <= self.x <= 8 and 1 <= self.y <= 8:
            return True
        else:
            return False

    def change_to_numbers(self, letter) -> int:
        return self.letter_dictionary[letter]

    def change_to_letters(self, number) -> str:
        number += 64
        letter = chr(number)
        return letter

    def count_field_name(self) -> str:
        letter = self.change_to_letters(self.y)
        return letter + str(self.x)


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
    def validate_move(self, field):
        pass


class King(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 100

    def list_available_moves(self, fields=None) -> list:
        list_moves = []
        x = self.field.x
        y = self.field.y
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 1 <= i <= 8 and 1 <= j <= 8 and (i != x or j != y):
                    try:
                        if fields is not None and fields[x + y*8].is_empty:
                            list_moves.append(Field(i, j))
                        else:
                            list_moves.append(Field(i, j))
                    except IndexError as err:
                        print('list_available_moves - Index Error: {}'.format(err))
                        raise IndexError

        return list_moves

    def validate_move(self, field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move.field_name == field.field_name:
                return True
        return False


class Queen(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 10

    def list_available_moves(self):
        pass

    def validate_move(self, field):
        pass


class Rook(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 5

    def list_available_moves(self):
        pass

    def validate_move(self, field):
        pass


class Bishop(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 4

    def list_available_moves(self):
        pass

    def validate_move(self, field):
        pass


class Knight(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 3

    def list_available_moves(self):
        pass

    def validate_move(self, field):
        pass


class Pawn(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 1

    def list_available_moves(self):
        pass

    def validate_move(self, field):
        pass
