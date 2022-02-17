# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

import pytest
from werkzeug.exceptions import HTTPException

from .models import Field, King, Pawn, Rook, Bishop, Queen, Knight
from .main import abort_if_field_doesnt_exist, abort_if_figure_doesnt_exist, app, change_to_numbers


class TestAbortMethods:
    def test_abort_if_field_exist(self):
        field = 'A1'

        abort, message = abort_if_field_doesnt_exist(field=field)
        assert abort != 409
        assert abort == 200
        assert message is None

    def test_abort_if_field_doesnt_exist(self):
        field = 'U1'

        abort, message = abort_if_field_doesnt_exist(field=field)
        assert abort == 409
        assert message == 'Field does not exist.'

    def test_abort_if_number_to_big(self):
        field = 'A99'

        abort, message = abort_if_field_doesnt_exist(field=field)
        assert abort == 409
        assert message == 'Field does not exist.'

    def test_abort_if_number_to_small(self):
        field = 'A-9'
        # with pytest.raises(HTTPException):
        abort, message = abort_if_field_doesnt_exist(field=field)
        assert abort == 409
        assert message == 'Field does not exist.'

    def test_abort_figure_exist(self):
        figure = 'king'

        abort, message = abort_if_figure_doesnt_exist(figure=figure)
        assert abort != 404
        assert abort == 200
        assert message is None

    def test_abort_figure_doesnt_exist(self):
        figure = 'pope'

        # with pytest.raises(HTTPException):
        abort, message = abort_if_figure_doesnt_exist(figure=figure)
        assert abort == 404
        assert message == "Bad figures."

    def test_change_to_number(self):
        letter = 'B'
        digit = change_to_numbers(letter)

        assert digit == 2

        letter = 'Z'
        with pytest.raises(KeyError):
            change_to_numbers(letter)


class TestChessMove:
    def test_get_ok(self):
        figure = 'queen'
        field = 'A1'

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field
            print('URL: {}'.format(url))
            response = client.get(url)
            assert response.status_code == 200

            assert response.get_json()['availableMoves'] != []

            assert 'H1' in response.get_json()['availableMoves']
            assert 'H8' in response.get_json()['availableMoves']
            assert 'A8' in response.get_json()['availableMoves']

    def test_get_move_bad_figure(self):
        figure = 'pope'
        field = 'A1'

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 404

            assert response.get_json()['availableMoves'] == []

    def test_get_move_bad_field(self):
        figure = 'king'
        field = 'Z9'

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 409

            assert response.get_json()['availableMoves'] == []

    def test_get_move_bad_both(self):
        figure = 'pope'
        field = 'Z9'

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 409

            assert response.get_json()['availableMoves'] == []


class TestChessCheck:
    def test_get_ok(self):
        figure = 'queen'
        field = 'A1'
        dest = "A3"

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field + '/' + dest
            print('URL: {}'.format(url))
            response = client.get(url)
            assert response.status_code == 200

            assert response.get_json()['move'] == 'valid'

    def test_get_check_bad_figure(self):
        figure = 'pope'
        field = 'A1'
        dest = "A3"

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field + '/' + dest
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 404

            assert response.get_json()['move'] == 'invalid'

    def test_get_check_bad_field(self):
        figure = 'queen'
        field = 'A1'
        dest = "U3"

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field + '/' + dest
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 409

            assert response.get_json()['move'] == 'invalid'

    def test_get_check_bad_dest_field(self):
        figure = 'queen'
        field = 'A1'
        dest = "G8"

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field + '/' + dest
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 200

            assert response.get_json()['move'] == 'invalid'

    def test_get_check_bad_both(self):
        figure = 'pope'
        field = 'A1'
        dest = "A3"

        with app.test_client() as client:
            url = '/api/v1/' + figure + '/' + field + '/' + dest
            print('URL: {}'.format(url))
            response = client.get(url)
            print(response.json)
            assert response.status_code == 404

            assert response.get_json()['move'] == 'invalid'


