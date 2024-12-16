from flask import Flask, request, abort
from markupsafe import escape
import json

class Task:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
    
    # Convert the object to a JSON representation.
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

app = Flask(__name__)

tasks = []

# When the API initializes, read the saved tasks into memory.
with app.app_context():
    with open('tasklist.json') as json_file:
        data = json.load(json_file)
        for item in data:
            tasks.append(Task(item['id'], item['title'], item['description']))


@app.route('/task', methods=['GET', 'POST'])
def get_all_or_post_task():
    
    # Return all the tasks in the list as JSON representations.
    if request.method == 'GET':
        return [task.to_json() for task in tasks]
    
    # Add an item to the list.
    elif request.method == 'POST':
        data = request.form

        # The following lines of code checks if an id is valid.
        # If no id is given, the program will generate a new unique id for the entry.
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
        
        # The following code checks if the POST request includes a title and then if the title is empty. 
        if 'title' not in data:         
            abort(400, description='Missing title') 
        else:
            title = data['title']
            if title == "":
                abort(400, description='Title is empty')
        
        # The following code checks if the POST request includes a description.
        if 'description' in data:
            description = data['description']
        else:
            description = ""

        tasks.append(Task(id,title,description))

        return "Added to list with id: " + str(tasks[len(tasks) - 1].id)


@app.route('/task/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_update_task(id):
    # Loop over the tasks until the one with the given id is selected.
    for task in tasks:
        if task.id == id:
            
            # Return the task as JSON representation.
            if request.method == 'GET':
                return [task.to_json()]
            
            # Remove the task.
            elif request.method == 'DELETE':
                tasks.remove(task)
                return "Task deleted"
            
            # Update the values submitted.
            elif request.method == 'PUT':
                data = request.form
                if 'title' in data:
                    task.title = data['title']
                if 'description' in data:
                    task.description = data['description']
                return "Task updated"
            
    return "Task not found"

# Create a new, unique id that is the lowest available integer not used by another item.
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

# Check if an id is unique.
def is_unique(id):
    for task in tasks:
        if task.id == id:
            return False
    return True