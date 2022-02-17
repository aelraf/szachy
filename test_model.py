# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

import pytest

from .models import Field, King, Pawn, Rook, Bishop


def get_starting_chessboard(fields: list[Field]) -> list:
    for i in range(0, 16):
        fields[i].is_empty = False
        if i == 0 or i == 7:
            fields[i].figure_code = 5
        if i == 1 or i == 6:
            fields[i].figure_code = 3
        if i == 2 or i == 5:
            fields[i].figure_code = 3
        if i == 3:
            fields[i].figure_code = 10
        if i == 4:
            fields[i].figure_code = 100
        if i in range(8, 16):
            fields[i].figure_code = 1

    for i in range(48, 64):
        fields[i].is_empty = False
        fields[i].is_black = True
        if i == 56 or i == 63:
            fields[i].figure_code = 5
        if i == 57 or i == 62:
            fields[i].figure_code = 3
        if i == 58 or i == 61:
            fields[i].figure_code = 3
        if i == 59:
            fields[i].figure_code = 10
        if i == 60:
            fields[i].figure_code = 100
        if i in range(48, 56):
            fields[i].figure_code = 1

    return fields


def get_fieldset() -> list:
    """
    zwraca zainicjowaną planszę pól, na której możemy modyfikować figury zajmujące okreslone miejsca
    """
    fieldset = []
    for i in range(1, 9):
        for j in range(1, 9):
            fieldset.append(Field(i, j))
    return fieldset


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

        assert king.validate_move(dest_field=field)

    def test_king_validate_not_straight_field(self):
        king = self.get_king()
        field = Field(4, 3, is_empty=True)

        assert not king.validate_move(dest_field=field)

    def test_king_validate_move_bad_field(self):
        king = self.get_king()
        field = Field(10, 12, is_empty=True)

        assert not king.validate_move(dest_field=field)

    def test_king_validate_move_not_empty_field(self):
        king = self.get_king()
        field = Field(4, 2, is_empty=False)

        assert not king.validate_move(dest_field=field)

    def test_king_validate_move_bad_not_empty_field(self):
        king = self.get_king()
        field = Field(34, 34, is_empty=False)

        assert not king.validate_move(dest_field=field)


class TestModelPawn:
    def get_pawn(self, is_black=False) -> Pawn:
        field = Field(1, 2, is_empty=False, figure_code=1, is_black=is_black)
        pawn = Pawn(field)

        return pawn

    def test_pawn_white_init(self):
        pawn = self.get_pawn()

        assert pawn.value == 1
        assert not pawn.field.is_empty
        assert pawn.field.field_name == 'B1'
        assert not pawn.field.is_black

    def test_pawn_white_list_available_moves(self):
        pawn = self.get_pawn()

        list_moves = pawn.list_available_moves()
        assert list_moves != []

        assert len(list_moves) == 1
        assert list_moves[0].field_name == 'C1'

    def test_pawn_black_list_available_moves(self):
        pawn = self.get_pawn(is_black=True)

        list_moves = pawn.list_available_moves()
        assert list_moves != []

        assert len(list_moves) == 1
        assert list_moves[0].field_name == 'A1'

    def test_pawn_white_available_moves_in_corner(self):
        field = Field(8, 8, is_empty=False, figure_code=1, is_black=False)
        pawn = Pawn(field)

        list_moves = pawn.list_available_moves()
        assert list_moves == []

    def test_pawn_white_available_moves_on_middle(self):
        field = Field(4, 4, is_empty=False, figure_code=1, is_black=False)
        pawn = Pawn(field)

        list_moves = pawn.list_available_moves()
        assert list_moves != []

        assert len(list_moves) == 1
        assert list_moves[0].field_name == 'E4'

    def test_pawn_black_available_moves_on_middle(self):
        field = Field(4, 4, is_empty=False, figure_code=1, is_black=True)
        pawn = Pawn(field)

        list_moves = pawn.list_available_moves()
        assert list_moves != []

        assert len(list_moves) == 1
        assert list_moves[0].field_name == 'C4'

    def test_pawn_moves_with_bad_parameter(self):
        pawn = self.get_pawn()
        fieldset = [Field(1, 3, is_empty=False), Field(1, 4, is_empty=False)]

        with pytest.raises(IndexError):
            pawn.list_available_moves(fields=fieldset)

    def test_pawn_validate_move_good_field(self):
        pawn = self.get_pawn()
        field = Field(1, 3, is_empty=True)

        assert pawn.validate_move(dest_field=field)

    def test_pawn_validate_not_straight_field(self):
        pawn = self.get_pawn()
        field = Field(2, 3, is_empty=True)

        assert not pawn.validate_move(dest_field=field)

    def test_pawn_validate_move_bad_field(self):
        pawn = self.get_pawn()
        field = Field(10, 12, is_empty=True)

        assert not pawn.validate_move(dest_field=field)

    def test_pawn_validate_move_not_empty_field(self):
        pawn = self.get_pawn()
        field = Field(4, 2, is_empty=False)

        assert not pawn.validate_move(dest_field=field)

    def test_pawn_validate_move_bad_not_empty_field(self):
        pawn = self.get_pawn()
        field = Field(34, 34, is_empty=False)

        assert not pawn.validate_move(dest_field=field)


class TestModelRook:
    def get_rook(self) -> Rook:
        field = Field(1, 1, is_empty=False, figure_code=5, is_black=False)
        rook = Rook(field)

        return rook

    def test_rook_init(self):
        rook = self.get_rook()

        assert rook.value == 5
        assert not rook.field.is_empty
        assert rook.field.field_name == "A1"

    def test_rook_list_available_moves(self):
        rook = self.get_rook()

        list_moves = rook.list_available_moves()
        assert list_moves != []

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert "A1" not in list_fields
        assert 'C1' in list_fields
        assert 'A8' in list_fields
        assert 'H1' in list_fields

        assert len(list_fields) == 14

    def test_rook_available_moves_in_top_corner(self):
        rook = Rook(Field(8, 8, is_empty=False, figure_code=5))

        list_moves = rook.list_available_moves()
        assert list_moves != []

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'H8' not in list_fields
        assert 'D8' in list_fields
        assert 'A8' in list_fields
        assert 'H1' in list_fields

        assert len(list_fields) == 14

    def test_rook_list_available_moves_on_middle(self):
        rook = Rook(Field(4, 4, is_empty=False, figure_code=5))

        list_moves = rook.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'D4' not in list_fields
        assert 'A4' in list_fields
        assert 'H4' in list_fields
        assert 'D1' in list_fields
        assert 'D8' in list_fields

        assert len(list_fields) == 14

    def test_rook_list_moves_with_bad_parameter(self):
        rook = self.get_rook()
        fieldset = [Field(4, 1, is_empty=False), Field(6, 1, is_empty=False)]

        with pytest.raises(IndexError):
            list_moves = rook.list_available_moves(fields=fieldset)

            list_fields = []
            for field in list_moves:
                list_fields.append(field.field_name)

    def test_rook_validate_good_field(self):
        rook = self.get_rook()
        field = Field(1, 8, is_empty=True)

        assert rook.validate_move(dest_field=field)

    def test_rook_validate_not_straight_field(self):
        rook = self.get_rook()
        field = Field(2, 8, is_empty=True)

        assert not rook.validate_move(dest_field=field)

    def test_rook_validate_move_bad_field(self):
        rook = self.get_rook()
        field = Field(10, 12, is_empty=True)

        assert not rook.validate_move(dest_field=field)

    def test_pawn_validate_move_not_empty_field(self):
        rook = self.get_rook()
        field = Field(4, 2, is_empty=False)

        assert not rook.validate_move(dest_field=field)

    def test_pawn_validate_move_bad_not_empty_field(self):
        rook = self.get_rook()
        field = Field(34, 34, is_empty=False)

        assert not rook.validate_move(dest_field=field)


class TestModelBishop:
    def get_bishop(self, x, y) -> Bishop:
        field = Field(x=x, y=y, is_empty=False, figure_code=4)
        bishop = Bishop(field)

        return bishop

    def test_bishop_init(self):
        bishop = self.get_bishop(3, 1)

        assert bishop.value == 4
        assert not bishop.field.is_empty
        assert bishop.field.field_name == 'A3'

    def test_bishop_available_moves(self):
        bishop = self.get_bishop(3, 1)

        list_moves = bishop.list_available_moves()
        assert list_moves != []

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'C1' in list_fields
        assert 'B4' in list_fields
        assert 'F8' in list_fields

        assert len(list_fields) == 7

    def test_bishop_available_moves_in_corner(self):
        bishop = self.get_bishop(8, 8)
        list_moves = bishop.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'G7' in list_fields
        assert 'D4' in list_fields
        assert 'A1' in list_fields
        assert len(list_fields) == 7

        bishop = self.get_bishop(1, 8)
        list_moves = bishop.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'G2' in list_fields
        assert 'A8' in list_fields
        assert 'C6' in list_fields
        assert len(list_fields) == 7

    def test_bishop_available_moves_on_middle(self):
        bishop = self.get_bishop(4, 4)
        list_moves = bishop.list_available_moves()

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'G1' in list_fields
        assert 'D4' not in list_fields
        assert 'A7' in list_fields
        assert 'A1' in list_fields
        assert 'G7' in list_fields
        assert len(list_fields) == 13

    def test_bishop_list_moves_with_bad_parameter(self):
        bishop = self.get_bishop(3, 1)
        fieldset = [Field(4, 1, is_empty=False), Field(6, 1, is_empty=False)]

        with pytest.raises(IndexError):
            bishop.list_available_moves(fields=fieldset)

    def test_bishop_list_moves_with_good_parameter(self):
        bishop = self.get_bishop(1, 3)
        fieldset = get_starting_chessboard(get_fieldset())

        list_moves = bishop.list_available_moves(fields=fieldset)
        assert list_moves != []

        list_fields = []
        for field in list_moves:
            list_fields.append(field.field_name)

        assert 'G5' not in list_fields
        assert 'E3' in list_fields
        assert 'F4' in list_fields
        assert 'D2' in list_fields
        assert len(list_fields) == 3

    def test_bishop_validate_move_good_field(self):
        bishop = self.get_bishop(3, 1)
        field = Field(4, 2, is_empty=True)

        assert bishop.validate_move(dest_field=field)

    def test_bishop_validate_not_straight_field(self):
        bishop = self.get_bishop(3, 1)
        field = Field(4, 3, is_empty=True)

        assert not bishop.validate_move(dest_field=field)

    def test_bishop_validate_move_bad_field(self):
        bishop = self.get_bishop(3, 1)
        field = Field(10, 12, is_empty=True)

        assert not bishop.validate_move(dest_field=field)

    def test_bishop_validate_move_not_empty_field(self):
        bishop = self.get_bishop(3, 1)
        field = Field(4, 2, is_empty=False)

        assert not bishop.validate_move(dest_field=field)

    def test_bishop_validate_move_bad_not_empty_field(self):
        bishop = self.get_bishop(3, 1)
        field = Field(34, 34, is_empty=False)

        assert not bishop.validate_move(dest_field=field)

