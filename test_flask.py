# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

import pytest
from werkzeug.exceptions import HTTPException

from .models import Field, King, Pawn, Rook, Bishop, Queen, Knight
from .main import abort_if_field_doesnt_exist, abort_if_figure_doesnt_exist, app


class TestAbortMethods:
    def test_abort_if_field_exist(self):
        field = 'A1'

        abort = abort_if_field_doesnt_exist(field=field)
        assert abort != 409

    def test_abort_if_field_doesnt_exist(self):
        field = 'U1'

        with pytest.raises(HTTPException):
            abort = abort_if_field_doesnt_exist(field=field)
            assert abort == 409

    def test_abort_if_number_to_big(self):
        field = 'A99'
        with pytest.raises(HTTPException):
            abort = abort_if_field_doesnt_exist(field=field)
            assert abort == 409

    def test_abort_if_number_to_small(self):
        field = 'A-9'
        with pytest.raises(HTTPException):
            abort = abort_if_field_doesnt_exist(field=field)
            assert abort == 409

            # def abort_if_figure_doesnt_exist(figure: str):
            #     figures = {'king', 'queen', 'bishop', 'knight', 'rook', 'pawn'}
            #     if figure not in figures:
            #         abort(404, message="Bad figures.")
    def test_abort_figure_exist(self):
        figure = 'king'

        abort = abort_if_figure_doesnt_exist(figure=figure)
        assert abort != 404
        assert abort is None

    def test_abort_figure_doesnt_exist(self):
        figure = 'pope'

        with pytest.raises(HTTPException):
            abort = abort_if_figure_doesnt_exist(figure=figure)
            assert abort == 404


class TestChessMove:
    def test_get_ok(self):
        pass

    def test_get_move_bad_figure(self):
        pass

    def test_get_move_bad_field(self):
        pass

    def test_get_move_bad_both(self):
        pass


class TestChessCheck:
    def test_get_ok(self):
        pass

    def test_get_check_bad_figure(self):
        pass

    def test_get_check_bad_field(self):
        pass

    def test_get_check_bad_dest_field(self):
        pass

    def test_get_check_bad_both(self):
        pass


