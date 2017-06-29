from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "my_secret_key"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)

    def __init__(self, title, body, pubdate):
        self.title = title
        self.body = body
        if pubdate is None:
            pubdate = datetime.utcnow()
        self.pubdate = pubdate


@app.route("/")
def index():
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()
    return render_template('bloglist.html', title = "Build a Blog", blogs=blogs)


@app.route('/blog', methods=['GET'])
def showpost():
    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('singlepost.html', blog=blog)
    else:
        blogs = Blog.query.order_by(Blog.pubdate.desc()).all()
        return render_template('bloglist.html', title = "Build a Blog", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def addpost():
    if request.method == "GET":
        return render_template('newpost.html', title="Add a Blog Entry")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if len(blog_title)>0 and len(blog_body)>0:
            new_blog = Blog(blog_title, blog_body, None)
            db.session.add(new_blog)
            db.session.commit() 
            return render_template('singlepost.html', blog=new_blog)
        else:
            flash('Blog title or body is empty')
            redirect('/newpost')

if __name__ == '__main__':
    app.run()