from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from database import Todo, engine, load_todos_from_db, User
from forms import RegisterForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
Session = sessionmaker(bind=engine)
app.config['SECRET_KEY'] = '1ec2ca1dd7600a0ae6de1665'

@app.route("/", methods=['GET', 'POST'])
def todos_content():
    session = Session()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = Todo(title=title, description=description)
        session.add(task)
        session.commit()

    tasks = load_todos_from_db()  # Fetch todos after adding a new todo
    return render_template("index.html", tasks=tasks)

@app.route("/api/todos")
def list_todos():
    tasks = Session.query(Todo).all()
    todos = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    session = Session()

    if request.method == 'POST':
        todo = session.query(Todo).get(todo_id)

        if todo:
            session.delete(todo)
            session.commit()

    session.close()
    return redirect('/')
@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    session = Session()
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password_hash=form.password1.data
        )

        session.add(user_to_create)
        session.commit()
        return redirect(url_for('todos_content'))
    if form.errors != {}: #If there are not errors from the validations
          for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/todos/<int:todo_id>/edit', methods=['GET', 'POST'])
def edit_todo(todo_id):
    session = Session()

    if request.method == 'POST':
        # Code to handle todo update
        # Retrieve the todo with the given ID from the session
        todo = session.query(Todo).get(todo_id)

        # If the todo exists, update its title and description with the values from the request form
        if todo:
            todo.title = request.form['title']
            todo.description = request.form['description']
            session.commit()

    # Retrieve the updated todo from the session
    updated_todo = session.query(Todo).get(todo_id)

    # Close the session
    session.close()

    # Render the template and pass the updated todo
    return render_template("edit.html", todo=updated_todo)



if __name__ == "__main__":
   
    app.run(debug=True, port=8000)
