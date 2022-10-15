from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.String(10))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=='POST':
        print("post")
        title = request.form['title']
        desc = request.form['desc']
        author = request.form['author']
        status = request.form.get('status')
        if status == None:
            status = "Pending"
        if status == "on":
            status = "Completed"
        todo = Todo(title=title, desc=desc,author=author,status=status)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route("/update/<int:sno>")
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo.status == "Pending":
        todo.status = "Completed"
    elif todo.status == "Completed":
        todo.status = "Pending"
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=8000)