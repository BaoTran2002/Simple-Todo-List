from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    # flash('You were successfully logged in')
    todo_list = Todo.query.order_by(Todo.name)
    return render_template("index.html", message="Welcome", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    # flash('You were successfully added')
    name = request.form.get('name')
    new_todo = Todo(name=name, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:todo_id>")
def upadate(todo_id):
    # flash('You were successfully updated')
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # flash('You were successfully deleted')
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
