# -*- coding: utf-8 -*-

import abc
from typing import List


class Field:
    def __init__(self, x: int, y: int, is_empty=True, figure_code=0, is_black=False):
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

    def change_to_numbers(self, letter: str) -> int:
        return self.letter_dictionary[letter]

    def change_to_letters(self, number: int) -> str:
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
    def __init__(self, field: Field):
        self.field = field

    @abc.abstractmethod
    def list_available_moves(self):
        pass

    @abc.abstractmethod
    def validate_move(self, dest_field: Field):
        pass


def moves_line(x: int, y: int, p1: int, p2: int, fields= None) -> list:
    """
    x i y to współrzędne sprawdzanego punku,
    p1 pilnuje x (-1 = lewo, 1 = prawo, 0 = góra-dół)
    p2 pilnuje y (-1 = dół, 1 = góra, 0 = prawo-lewo)

    zwraca listę możliwych do osiągnięcia pól z prostych
    """

    list_moves = []

    try:
        for i in range(1, 8):
            if 1 <= x + p1 * i <= 8 and 1 <= y + p2 * i <= 8:
                if fields is not None and fields[(x-1 + p1*i) + ((y-1) + p2*i) * 8].is_empty:
                    list_moves.append(Field(x + p1 * i, y + p2 * i).field_name)
                elif fields is None:
                    list_moves.append(Field(x + p1 * i, y + p2 * i).field_name)
                elif fields is not None and not fields[(x-1 + p1*i) + ((y - 1) + p2 * i) * 8].is_empty:
                    break
            else:
                break
    except IndexError as err:
        print('moves_line - Index Error: {}'.format(err))
        raise IndexError
    except TypeError as err:
        print('moves_line: TypeError: {}'.format(err))
        raise TypeError

    return list_moves


def moves_oblique(x: int, y: int, p1: int, p2: int, fields= None) -> list:
    """
    wszystkie ruchy skośne w jednej metodzie

    p1 - znak przy przesuwaniu y
    p2 - znak przy przesuwaniu x

    :return: listę pól osiągalnych ze startowego po skosach
    """
    list_moves = []

    try:
        for i in range(1, 8):
            yk = y + p1 * i
            xk = x + p2 * i
            if 1 <= xk <= 8 and 1 <= yk <= 8:
                if fields is not None and fields[(xk-1) + (yk-1) * 8].is_empty:
                    list_moves.append(Field(xk, yk).field_name)
                elif fields is None:
                    list_moves.append(Field(xk, yk).field_name)
                elif fields is not None and not fields[(xk-1) + (yk-1) * 8].is_empty:
                    break
            else:
                break
    except IndexError as err:
        print('moves_oblique - Index Error: {}'.format(err))
        raise IndexError
    except TypeError as err:
        print('moves_oblique: TypeError: {}'.format(err))
        raise TypeError

    return list_moves


class King(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 100

    def list_available_moves(self, fields: List[Field] = None) -> list:
        list_moves = []
        x = self.field.x
        y = self.field.y
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 1 <= i <= 8 and 1 <= j <= 8 and (i != x or j != y):
                    try:
                        if fields is not None and fields[i + j*8].is_empty:
                            list_moves.append(Field(i, j).field_name)
                        elif fields is None:
                            list_moves.append(Field(i, j).field_name)
                    except IndexError as err:
                        print('list_available_moves - Index Error: {}'.format(err))
                        raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields: List[Field] = None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False


class Queen(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 10

    def list_available_moves(self, fields= None) -> list:
        list_moves = []

        x = self.field.x
        y = self.field.y

        try:
            list_moves += moves_oblique(x=x, y=y, p1=1, p2=-1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=1, p2=1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=-1, p2=-1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=-1, p2=1, fields=fields)

            list_moves += moves_line(x=x, y=y, p1=-1, p2=0, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=1, p2=0, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=0, p2=-1, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=0, p2=1, fields=fields)

        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields: List[Field] = None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False


class Rook(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 5

    def list_available_moves(self, fields: List[Field] = None) -> list:
        list_moves = []
        x = self.field.x
        y = self.field.y

        try:
            list_moves += moves_line(x=x, y=y, p1=-1, p2=0, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=1, p2=0, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=0, p2=-1, fields=fields)
            list_moves += moves_line(x=x, y=y, p1=0, p2=1, fields=fields)

        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields: List[Field] = None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False


class Bishop(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 4

    def list_available_moves(self, fields: List[Field] = None) -> list:
        list_moves = []

        x = self.field.x
        y = self.field.y

        try:
            list_moves += moves_oblique(x=x, y=y, p1=1, p2=-1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=1, p2=1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=-1, p2=-1, fields=fields)
            list_moves += moves_oblique(x=x, y=y, p1=-1, p2=1, fields=fields)
        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields: List[Field] = None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False


class Knight(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 3

    def list_available_moves(self, fields: List[Field] = None) -> list:
        list_moves = []

        x = self.field.x
        y = self.field.y

        try:
            for ix in range(-1, 2, 2):
                for iy in range(-2, 3, 4):
                    if 0 < x + ix < 9 and 0 < y + iy < 9:
                        if fields is not None and fields[x-1 + ix + (y-1+iy) * 8].is_empty:
                            list_moves.append(Field(x + ix, y + iy).field_name)
                        elif fields is None:
                            list_moves.append(Field(x + ix, y + iy).field_name)

            for ix in range(-2, 3, 4):
                for iy in range(-1, 2, 2):
                    if 0 < x + ix < 9 and 0 < y + iy < 9:
                        if fields is not None and fields[x-1 + ix + (y-1+iy) * 8].is_empty:
                            list_moves.append(Field(x + ix, y + iy).field_name)
                        elif fields is None:
                            list_moves.append(Field(x + ix, y + iy).field_name)

        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields: List[Field] = None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False


class Pawn(Figure):
    def __init__(self, field: Field):
        super().__init__(field)
        self.value = 1

    def list_available_moves(self, fields=None) -> list:
        list_moves = []
        x = self.field.x
        y = self.field.y

        try:
            if 0 < x <= 8 and 0 < y < 8:
                if not self.field.is_black:
                    if fields is not None and fields[x + (y + 1) * 8].is_empty:
                        list_moves.append(Field(x, y + 1).field_name)
                    elif fields is None:
                        list_moves.append(Field(x, y + 1).field_name)
                else:
                    if fields is not None and fields[x + (y - 1) * 8].is_empty:
                        list_moves.append(Field(x, y - 1).field_name)
                    elif fields is None:
                        list_moves.append(Field(x, y - 1).field_name)
        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field: Field, fields=None) -> bool:
        if not dest_field.is_empty:
            return False

        moves = self.list_available_moves(fields=fields)

        for move in moves:
            if move == dest_field.field_name:
                return True
        return False
