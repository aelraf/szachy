# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

import pytest

from .models import Field, King


def get_starting_chess(fields: list[Field]) -> list:
    for i in range(1, 17):
        fields[i].is_empty = False
        if i == 1 or i == 8:
            fields[i].figure_code = 5
        if i == 2 or i == 7:
            fields[i].figure_code = 3
        if i == 3 or i == 6:
            fields[i].figure_code = 3
        if i == 4:
            fields[i].figure_code = 10
        if i == 5:
            fields[i].figure_code = 100
        if i in range(9, 17):
            fields[i].figure_code = 1

    for i in range(48, 65):
        fields[i].is_empty = False
        fields[i].is_black = True
        if i == 57 or i == 64:
            fields[i].figure_code = 5
        if i == 58 or i == 63:
            fields[i].figure_code = 3
        if i == 59 or i == 62:
            fields[i].figure_code = 3
        if i == 60:
            fields[i].figure_code = 10
        if i == 61:
            fields[i].figure_code = 100
        if i in range(48, 57):
            fields[i].figure_code = 1

    return fields


class TestsModelFields:
    def test_fields_init_only_cord(self):
        field = Field(2, 2)

        assert field.figure_code == 0
        assert field.is_empty
        assert field.field_name == 'B2'
        assert not field.is_black
        assert field.x == 2
        assert field.y == 2

    def test_fields_init_black_not_empty_with_figure(self):
        field = Field(3, 3, None, 100, True)

        assert field.figure_code == 100
        assert not field.is_empty
        assert field.field_name == 'C3'
        assert field.is_black
        assert field.x == 3
        assert field.y == 3

    def test_fields_functions(self):
        field = Field(1, 1)

        assert field.count_field_name() == 'A1'
        assert field.check_is_correct()
        assert field.change_to_numbers('H') == 8

        for i in range(1, 9):
            for j in range(1, 9):
                f2 = Field(i, j)

                assert f2.check_is_correct()
                assert f2.field_name == f2.change_to_letters(j) + str(i)
                assert f2.field_name == chr(j + 64) + str(i)


class TestModelKing:
    def get_king(self) -> King:
        field = Field(5, 1, is_empty=False, figure_code=100, is_black=False)
        king = King(field)

        return king

    def get_fieldset(self) -> list:
        """
        zwraca zainicjowaną planszę, na której możemy modyfikować figury zajmujące okreslone miejsca
        """
        fieldset = []
        for i in range(1, 9):
            for j in range(1, 9):
                fieldset.append(Field(i, j))
        return fieldset

    def test_king_init(self):
        king = self.get_king()

        assert king.value == 100
        assert not king.field.is_empty
        assert king.field.field_name == 'A5'

    def test_king_list_available_moves(self):
        king = self.get_king()

        list_moves = king.list_available_moves()
        assert list_moves != []

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'B5' in list_fields
        assert 'B4' in list_fields
        assert 'B6' in list_fields
        assert 'A4' in list_fields
        assert 'A6' in list_fields
        assert len(list_fields) == 5

    def test_king_list_available_moves_in_corner(self):
        field = Field(8, 8, is_empty=False, figure_code=100, is_black=False)
        king = King(field)

        list_moves = king.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'G7' in list_fields
        assert 'G8' in list_fields
        assert 'H7' in list_fields
        assert len(list_fields) == 3

    def test_king_list_available_moves_on_middle(self):
        field = Field(4, 4, is_empty=False, figure_code=100, is_black=False)
        king = King(field)

        list_moves = king.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'C3' in list_fields
        assert 'E4' in list_fields
        assert 'D5' in list_fields
        assert len(list_fields) == 8

    def test_king_list_moves_with_bad_parameter(self):
        king = self.get_king()
        fieldset = [Field(4, 1, is_empty=False), Field(6, 1, is_empty=False)]

        with pytest.raises(IndexError):
            list_moves = king.list_available_moves(fields=fieldset)

            list_fields = []
            for field in list_moves:
                list_fields.append(field.field_name)

    def test_king_validate_move_good_field(self):
        king = self.get_king()
        field = Field(4, 2, is_empty=True)

        assert king.validate_move(field=field)

    def test_king_validate_move_bad_field(self):
        king = self.get_king()

    def test_king_validate_move_not_empty_field(self):
        king = self.get_king()
