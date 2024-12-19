from flask import Flask, request, abort
from markupsafe import escape
import json

app = Flask(__name__)


# When the API initializes, read the saved tasks into memory.
with app.app_context():
    with open('tasklist.json') as json_file:
        tasks = json.load(json_file)


@app.route('/task', methods=['GET', 'POST'])
def get_all_or_post_task():
    
    # Return all the tasks in the list as JSON representations.
    if request.method == 'GET':
        return tasks
    
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

        tasks.append({'id': id, 'title': title, 'description': description})
        save()

        return "Item added to list: " + str(tasks[len(tasks) - 1])


@app.route('/task/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_update_task(id):
    # Loop over the tasks until the one with the given id is selected.
    for i in range(len(tasks)): 
        if tasks[i]['id'] == id:
            
            # Return the task as JSON representation.
            if request.method == 'GET':
                return tasks[i]
            
            # Remove the task.
            elif request.method == 'DELETE':
                delete_task = tasks[i]
                del tasks[i]
                #tasks.remove(task)
                save()
                return "Task deleted: " + delete_task
            
            # Update the values submitted.
            elif request.method == 'PUT':
                data = request.form
                if 'title' in data:
                    tasks[i]['title'] = data['title']
                if 'description' in data:
                    tasks[i]['description'] = data['description']
                save()
                return "Task updated"
            
    return "Task not found"

# Create a new, unique id that is the lowest available integer not used by another item.
def new_unique_id():
    list_of_ids = [task['id'] for task in tasks]
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
        if task['id'] == id:
            return False
    return True

def save():
    with open('tasklist.json', 'w') as file:
        json.dump(tasks, file)