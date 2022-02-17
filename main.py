from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse, abort

from .models import Field, King, Queen, Bishop, Knight, Rook, Pawn

app = Flask(__name__)
api = Api(app)


def abort_if_field_doesnt_exist(field: str):
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
    if field[0] not in letters or int(field[1:]) > 8 or int(field[1:]) < 1:
        return 409, "Field does not exist."
    return 200, None


def abort_if_figure_doesnt_exist(figure: str):
    figures = {'king', 'queen', 'bishop', 'knight', 'rook', 'pawn'}
    if figure not in figures:
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
            diction = {
                'king': King(field),
                'queen': Queen(field),
                'bishop': Bishop(field),
                'knight': Knight(field),
                'rook': Rook(field),
                'pawn': Pawn(field)
            }

            checking_figure = diction.get(figure, '')
            field.figure_code = checking_figure.value

            available_moves = checking_figure.list_available_moves()

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
    def create_json(
            self,
            is_valid: str,
            figure: str,
            error: str,
            current_field: str,
            dest_field: str,
            response_code: int):
        return make_response(jsonify({
            "move": is_valid,
            "figure": figure,
            "error": error,
            "currentField": current_field,
            "destField": dest_field
        }), response_code)

    def get(self, figure: str, current_field: str, dest_field: str):
        error1_code, error1_message = abort_if_field_doesnt_exist(field=current_field)
        error2_code, error2_message = abort_if_figure_doesnt_exist(figure=figure)
        error3_code, error3_message = abort_if_field_doesnt_exist(field=dest_field)

        error_code = max(error1_code, error2_code, error3_code)
        if error_code > 200:
            return self.create_json(
                is_valid='invalid',
                figure=figure,
                error='',
                current_field=current_field,
                dest_field=dest_field,
                response_code=error_code
            )

        if error1_code == 200 and error2_code == 200 and error3_code == 200:
            field = Field(int(current_field[1]), change_to_numbers(current_field[0]), is_empty=False)
            dest_f = Field(int(dest_field[1]), change_to_numbers(dest_field[0]), is_empty=True)
            diction = {
                'king': King(field),
                'queen': Queen(field),
                'bishop': Bishop(field),
                'knight': Knight(field),
                'rook': Rook(field),
                'pawn': Pawn(field)
            }

            checking_figure = diction.get(figure, '')
            field.figure_code = checking_figure.value

            try:
                valid = checking_figure.validate_move(dest_field=dest_f)
                is_valid = 'valid' if valid else 'invalid'
                response_code = 200
            except:
                response_code = 500
                is_valid = 'invalid'

            return self.create_json(
                is_valid=is_valid,
                figure=figure,
                error='null',
                current_field=field.field_name,
                dest_field=dest_f.field_name,
                response_code=response_code
            )


api.add_resource(ChessMove, "/api/v1/<string:figure>/<string:current_field>")
api.add_resource(ChessCheck, "/api/v1/<string:figure>/<string:current_field>/<string:dest_field>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
