from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100)) #max amount of characters is 100
    complete = db.Column(db.Boolean) #used to check if a task was completed


@app.route('/')
def index():
    #show all todos on index page
    todo_list = Todo.query.all()
    #print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False) # creates new item for todo list, set initially to false
    db.session.add(new_todo) # adds item to database
    db.session.commit() # sends/commits the information to the database
    return redirect(url_for("index")) # after adding something to the list, redirect to the "index" url to refresh page

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # update an existing item
    todo = Todo.query.filter_by(id=todo_id).first() # we query through our list/db by the todo_id, we only need to return the first one
    todo.complete = not todo.complete # we set this to the opposite so that we can go back to either complete or not complete
    db.session.commit() # sends/commits the information to the database
    return redirect(url_for("index")) # after adding something to the list, redirect to the "index" url to refresh page

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete an existing item
    todo = Todo.query.filter_by(id=todo_id).first() # we query through our list/db by the todo_id, we only need to return the first one
    db.session.delete(todo)
    db.session.commit() # sends/commits the information to the database
    return redirect(url_for("index")) # after adding something to the list, redirect to the "index" url to refresh page


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)

    #This is a test for the new branch
    #working on dark and light mode feature