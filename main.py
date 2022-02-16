from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


names = {
    'tim': {"age": 19, "gender": 'male'},
    'bill': {"age": 70, "gender": 'male'}
}


class HelloWorld(Resource):
    def get(self, name, test=0):
        return names[name]

    def post(self):
        return {'data': "Posted"}


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)


videos = {}


def abort_if_video_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Video id is not valid...")


class Video(Resource):
    def get(self, video_id: int):
        abort_if_video_doesnt_exist(video_id)
        return videos[video_id]

    def put(self, video_id: int):
        args = video_put_args.parse_args()
        videos[video_id] = args
        # return {video_id: args}
        return videos[video_id], 201


# api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
