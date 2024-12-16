from flask import Flask, request, abort
from markupsafe import escape
import json

class Task:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

app = Flask(__name__)

tasks = []

#tasks.append(Task(0,"First", "This is the first task"))
#tasks.append(Task(1,"Second", "This is the second task"))

with app.app_context():
    with open('tasklist.json') as json_file:
        data = json.load(json_file)
        for item in data:
            tasks.append(Task(item['id'], item['title'], item['description']))


@app.route('/task', methods=['GET', 'POST'])
def get_all_or_post_task():

    if request.method == 'GET':
        return [task.to_json() for task in tasks]
    
    elif request.method == 'POST':
        data = request.form

        if 'id' not in data:
            id = new_unique_id()
        else:
            try: 
                id = int(data['id'])
            except ValueError:
                abort(400, description='Id is not an integer')
            
            if not is_unique(int(id)):
                abort(400, description='Id is not unique')
            else:
                id = int(data['id'])

        if 'title' not in data:
            abort(400, description='Missing title')
        else:
            title = data['title']
            if title == "":
                abort(400, description='Title is empty')

        if 'description' in data:
            description = data['description']

        tasks.append(Task(id,title,description))

        return "Added to list with id: " + str(tasks[len(tasks) - 1].id)

@app.route('/task/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_update_task(id):
    for task in tasks:
        if task.id == id:
            
            if request.method == 'GET':
                return [task.to_json()]
            
            elif request.method == 'DELETE':
                task_to_delete = task
                tasks.remove(task)
                return "Task deleted"
            
            elif request.method == 'PUT':
                data = request.form
                if 'title' in data:
                    task.title = data['title']
                if 'description' in data:
                    task.description = data['description']
                return "Task updated"
            
    return "Task not found"

def new_unique_id():
    list_of_ids = [task.id for task in tasks]
    list_of_ids.sort()
    last_id = -1
    for id in list_of_ids:
        if id - last_id != 1:
            return id - 1
        else:
            last_id = id
    return last_id + 1

def is_unique(id):
    for task in tasks:
        if task.id == id:
            return False
    return True