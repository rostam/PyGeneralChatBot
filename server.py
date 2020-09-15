from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import fasttext as ft
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': 'möööääßß'},
    'todo3': {'task': 'profit!'},
}

intents = []
with open('intents', 'r') as f:
    for d in f.read().split("\n"):
        if d != "":
            intents.append(d)

model = ft.load_model('tvmodel.bin')


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class Predict(Resource):
    def get(self, utt):
        res = model.predict(utt, k=3)
        arr = []

        for i, r in enumerate(res[0]):
            index_ = int(r[r.rindex('_') + 1:])
            # print(index_ - 1)
            arr.append({intents[index_ - 1]: res[1][i]})
        return arr


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Predict, '/predict/<utt>')

if __name__ == '__main__':
    app.run(debug=True)
