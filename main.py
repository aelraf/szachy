from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


names = {
    'tim': {"age": 19, "gender": 'male'},
    'bill': {"age": 70, "gender": 'male'}
}


class HelloWorld(Resource):
    def get(self, name, test):
        # return {'data': name, "test": test}
        return names[name]

    def post(self):
        return {'data': "Posted"}


#api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
api.add_resource(HelloWorld, "/helloworld/<string:name>")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
