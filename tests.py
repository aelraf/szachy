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

        for i in range(1, 8):
            for j in range(1, 8):
                f2 = Field(i, j)

                assert f2.check_is_correct()
                assert f2.field_name == f2.change_to_letters(j) + str(i)
                assert f2.field_name == chr(j + 64) + str(i)


class TestModelKing:
    def test_king_init(self):
        field = Field(5, 1, is_empty=False, figure_code=100, is_black=False)
        king = King(field)

        assert king.value == 100
        assert not king.field.is_empty
        assert king.field.field_name == 'A5'
