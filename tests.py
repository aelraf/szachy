# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

from flask.testing import Client
import pytest

from .models import Field, King


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

    def test_king_validate_move_good_field(self):
        king = self.get_king()

    def test_king_validate_move_bad_field(self):
        king = self.get_king()
