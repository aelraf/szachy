from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse, abort

from .models import Field, King, Queen, Bishop, Knight, Rook, Pawn

app = Flask(__name__)
api = Api(app)


def abort_if_field_doesnt_exist(field: str):
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
    if field[0] not in letters or int(field[1:]) > 8 or int(field[1:]) < 1:
        # abort(409, error="Field does not exist.")
        return 409, "Field does not exist."
    return 200, None


def abort_if_figure_doesnt_exist(figure: str):
    figures = {'king', 'queen', 'bishop', 'knight', 'rook', 'pawn'}
    if figure not in figures:
        # abort(404, error="Bad figures.")
        return 404, "Bad figures."
    return 200, None


def change_to_numbers(letter: str) -> int:
    try:
        letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
        return letters[letter]
    except KeyError as err:
        print("change_to_number: {}, KeyError: {}".format(letter, err))
        raise KeyError


class ChessMove(Resource):
    def get(self, figure: str, current_field: str):
        error1_code, error1_message = abort_if_field_doesnt_exist(field=current_field)
        error2_code, error2_message = abort_if_figure_doesnt_exist(figure=figure)
        available_moves = []

        if error1_code == 200 and error2_code == 200:
            field = Field(int(current_field[1]), change_to_numbers(current_field[0]), is_empty=False)
            print(field.field_name)
            dict = {
                'king': King(field),
                'queen': Queen(field),
                'bishop': Bishop(field),
                'knight': Knight(field),
                'rook': Rook(field),
                'pawn': Pawn(field)
            }

            checking_figure = dict.get(figure, '')
            field.figure_code = checking_figure.value

            print('GET - figura: {}, pole: {},sprawdzane: {}'.format(
                checking_figure.value,
                checking_figure.field.field_name,
                field.field_name)
            )

            available_moves = checking_figure.list_available_moves()
            print(available_moves)

        error_code = error1_code if error1_code != 200 else error2_code if error2_code != 200 else None
        error_message = error1_message if error1_code else error2_message
        response_code = 200 if error1_code is None and error2_code is None else error_code

        return make_response(jsonify({
            'availableMoves': available_moves,
            'error': error_message,
            'figure': figure,
            'currentField': current_field
        }), response_code)


class ChessCheck(Resource):
    def get(self, figure: str, current_field: str, dest_field: str):
        pass


api.add_resource(ChessMove, "/api/v1/<string:figure>/<string:current_field>")
api.add_resource(ChessCheck, "/api/v1/<string:figure>/<string:current_field>/<string:dest_field>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
