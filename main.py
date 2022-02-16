from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


names = {
    'tim': {"age": 19, "gender": 'male'},
    'bill': {"age": 70, "gender": 'male'}
}


class HelloWorld(Resource):
    def get(self, name, test=0):
        # return {'data': name, "test": test}
        return names[name]

    def post(self):
        return {'data': "Posted"}


videos = {}


class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):

        pass


# api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
