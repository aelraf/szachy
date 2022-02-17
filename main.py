from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


def abort_if_field_doesnt_exist(field: str):
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}
    if field[0] not in letters or int(field[1]) > 8 or int(field[1]) < 1:
        abort(409, message="Field does not exist.")


def abort_if_figure_doesnt_exist(figure: str):
    figures = {'king', 'queen', 'bishop', 'knight', 'rook', 'pawn'}
    if figure not in figures:
        abort(404, message="Bad figures.")


class ChessMove(Resource):
    def get(self):
        pass


class ChessCheck(Resource):
    def get(self):
        pass


api.add_resource(ChessMove, "/api/v1/<str:figure>/<str:current_field>")
api.add_resource(ChessCheck, "/api/v1/<str:figure>/<str:current_field>/<str:dest_field>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
