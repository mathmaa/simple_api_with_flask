#simple_api_with_flask
Get all tasks: Retrieve a list of all tasks.
Add a task: Add a new task with a unique id.
Get a specific task: Retrieve details of a task by its id.
Update a task: Modify the title and/or description of an existing task.
Delete a task: Remove a task by its id.

GET /task
- Gets all tasks as json
POST /task
- Adds a new task to the list
-- Request parameters (form-data): id (optional), title (required), description (optional)
GET /task/<id>
- Retrieves a task by its id
PUT /task/<id>
- Updates the title and/or description of a task by its id
-- Request parameters (form-data): title (optional), description (optional)
DELETE /task/<id>
- Deletes a task by its ID.