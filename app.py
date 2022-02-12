from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


DEBUG = True


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///action-log.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    task = db.Column(db.String(30), nullable=False)
    tag = db.Column(db.String, nullable=False)
    duration = db.Column(db.Time)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = Post.query.order_by(Post.start_time).all()
        return render_template("index.html", posts=posts, today=datetime.today())
    
    else:
        task = request.form.get("task")
        tag = request.form.get("tag")
        date = request.form.get("date")
        time = request.form.get("time")
        duration = None
        
        start_time = datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
        
        before_task = Post.query.order_by(Post.start_time.desc()).filter(
            Post.start_time < start_time).first()
        if before_task:
            before_time = start_time - before_task.start_time
            before_task.duration = datetime.time(
                datetime.strptime(str(before_time), "%H:%M:%S"))
        
        next_task = Post.query.order_by(Post.start_time).filter(
            Post.start_time > start_time).first()
        if next_task:
            duration = next_task.start_time - start_time
            duration = datetime.time(
                datetime.strptime(str(duration), "%H:%M:%S"))
        
        new_post = Post(
            task=task, 
            tag=tag, 
            start_time=start_time, 
            duration=duration
            )
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    post = Post.query.get(id)
    if request.method == "GET":
        return render_template("update.html", post=post)
    
    else:
        date = request.form.get("date")
        time = request.form.get("time")
        start_time = datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
        
        post.task = request.form.get("task")
        post.tag = request.form.get("tag")
        post.start_time = start_time
        
        db.session.commit()
        return redirect("/")


@app.route("/tag/<int:id>")
def read(id):
    post = Post.query.get(id)
    return render_template('tag.html', post=post)


@app.route("/delete/<int:id>")
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=DEBUG)
