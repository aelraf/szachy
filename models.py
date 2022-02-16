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
    def validate_move(self, dest_field):
        pass


def moves_left(x: int, y: int, fields=None) -> list:
    list_moves = []

    try:
        for i in range(x - 1, 0, -1):
            if 1 <= i <= 8 and 1 <= y <= 8:
                print("ruchy wieży w lewo: {} {}".format(i, y))
                if fields is not None and fields[i + y * 8].is_empty:
                    list_moves.append(Field(i, y))
                elif fields is None:
                    list_moves.append(Field(i, y))
                elif fields is not None and not fields[i + y * 8].is_empty:
                    break
    except IndexError as err:
        print('moves_left - Index Error: {}'.format(err))
        raise IndexError

    return list_moves


def moves_right(x: int, y: int, fields=None) -> list:
    list_moves = []

    try:
        for i in range(x + 1, 9):
            if 1 <= i <= 8 and 1 <= y <= 8:
                print("ruchy wieży w prawo: {} {}".format(i, y))
                if fields is not None and fields[i + y * 8].is_empty:
                    list_moves.append(Field(i, y))
                elif fields is None:
                    list_moves.append(Field(i, y))
                elif fields is not None and not fields[i + y * 8].is_empty:
                    break
    except IndexError as err:
        print('moves_right - Index Error: {}'.format(err))
        raise IndexError

    return list_moves


def moves_up(x: int, y: int, fields=None) -> list:
    list_moves = []

    try:
        for j in range(y + 1, 9):
            if 1 <= x <= 8 and 1 <= j <= 8:
                print("ruchy wieży w górę: {} {}".format(x, j))
                if fields is not None and fields[x + j * 8].is_empty:
                    list_moves.append(Field(x, j))
                elif fields is None:
                    list_moves.append(Field(x, j))
                elif fields is not None and not fields[x + j * 8].is_empty:
                    break
    except IndexError as err:
        print('moves_up - Index Error: {}'.format(err))
        raise IndexError

    return list_moves


def moves_down(x: int, y: int, fields=None) -> list:
    list_moves = []

    try:
        for j in range(y - 1, 0, -1):
            if 1 <= x <= 8 and 1 <= j <= 8:
                print("ruchy wieży w dół: {} {}".format(x, j))
                if fields is not None and fields[x + j * 8].is_empty:
                    list_moves.append(Field(x, j))
                elif fields is None:
                    list_moves.append(Field(x, j))
                elif fields is not None and not fields[x + j * 8].is_empty:
                    break
    except IndexError as err:
        print('moves_down - Index Error: {}'.format(err))
        raise IndexError

    return list_moves


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
                        if fields is not None and fields[i + j*8].is_empty:
                            list_moves.append(Field(i, j))
                        elif fields is None:
                            list_moves.append(Field(i, j))
                    except IndexError as err:
                        print('list_available_moves - Index Error: {}'.format(err))
                        raise IndexError

        return list_moves

    def validate_move(self, dest_field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        if not dest_field.is_empty:
            return False

        for move in moves:
            if move.field_name == dest_field.field_name:
                return True
        return False


class Queen(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 10

    def list_available_moves(self):
        pass

    def validate_move(self, dest_field):
        pass


class Rook(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 5

    def list_available_moves(self, fields=None) -> list:
        list_moves = []
        x = self.field.x
        y = self.field.y

        print("początkowa lokalizacja wieży: {}, {}".format(x, y))
        try:
            list_moves += moves_left(x=x, y=y, fields=fields)
            list_moves += moves_right(x=x, y=y, fields=fields)
            list_moves += moves_down(x=x, y=y, fields=fields)
            list_moves += moves_up(x=x, y=y, fields=fields)

        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        for move in list_moves:
            print(move.field_name)

        return list_moves

    def validate_move(self, dest_field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        if not dest_field.is_empty:
            return False

        for move in moves:
            if move.field_name == dest_field.field_name:
                return True
        return False


class Bishop(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 4

    def list_available_moves(self, fields=None) -> list:
        list_moves = []

        x = self.field.x
        y = self.field.y

        try:
            print('lewo góra: ')
            for i in range(1, 8):
                yk = y + i
                xk = x - i
                print("i: {}, xk: {}, yk: {}".format(i, xk, yk))
                if 1 <= xk <= 8 and 1 <= yk <= 8:
                    if fields is not None and fields[xk + yk * 8].is_empty:
                        list_moves.append(Field(xk, yk))
                    elif fields is None:
                        list_moves.append(Field(xk, yk))
                    elif fields is not None and not fields[xk + yk * 8].is_empty:
                        break
                if xk < 1 or yk < 1:
                    break

        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        for move in list_moves:
            print(move.field_name)

        return list_moves

    def validate_move(self, dest_field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        if not dest_field.is_empty:
            return False

        for move in moves:
            if move.field_name == dest_field.field_name:
                return True
        return False


class Knight(Figure):
    def __init__(self, field):
        super().__init__(field)
        self.value = 3

    def list_available_moves(self, fields=None) -> list:
        list_moves = []

        return list_moves

    def validate_move(self, dest_field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        if not dest_field.is_empty:
            return False

        for move in moves:
            if move.field_name == dest_field.field_name:
                return True
        return False


class Pawn(Figure):
    def __init__(self, field):
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
                        list_moves.append(Field(x, y + 1))
                    elif fields is None:
                        list_moves.append(Field(x, y + 1))
                else:
                    if fields is not None and fields[x + (y - 1) * 8].is_empty:
                        list_moves.append(Field(x, y - 1))
                    elif fields is None:
                        list_moves.append(Field(x, y - 1))
        except IndexError as err:
            print('list_available_moves - Index Error: {}'.format(err))
            raise IndexError

        return list_moves

    def validate_move(self, dest_field, fields=None) -> bool:
        moves = self.list_available_moves(fields=fields)

        if not dest_field.is_empty:
            return False

        for move in moves:
            if move.field_name == dest_field.field_name:
                return True
        return False
