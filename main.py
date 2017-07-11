from flask import request, redirect, render_template, session, flash
from app import app, db
from model import Blog, User
from flask_sqlalchemy import SQLAlchemy
from hashutil import check_hash
from datetime import datetime


@app.route("/")
def index():
    blogs = Blog.query.order_by(Blog.pubdate.desc()).all()
    return render_template('bloglist.html', title = "Build a Blog", blogs=blogs)


"""
@app.before_request
def require_login():
    allowed_endpoints = ['register', 'login', 'blog', 'index', 'users']
    if (request.endpoint not in allowed_endpoints) and ('username' not in session):
        return redirect('/login')
"""

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if not username or not password or not verify:
            flash('Please input information!')
        elif password != verify:
            flash('Passwords do not match!')
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('User already exists!')
            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
    else:
        return render_template('register.html')



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        blogs = Blog.query.filter_by(owner=user.id).all()
        if user and check_hash(password, user.password):
            session['username'] = username
            flash("You've logged in successfully")
            return render_template('singleuser.html', user = user, blogs=blogs)
        elif user and not check_hash(password, user.password):
            flash('Password incorrect!')
        else:
            flash('User does not exist!')
    return render_template('login.html')


@app.route('/newpost', methods=['POST', 'GET'])
def addpost():
    if request.method == "GET":
        return render_template('newpost.html', title="Add a Blog Entry")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_pubdate = datetime.now()
        owner = User.query.filter_by(username=session['username']).first().id
        if len(blog_title)>0 and len(blog_body)>0:
            new_blog = Blog(blog_title, blog_body, blog_pubdate, owner)
            db.session.add(new_blog)
            db.session.commit() 
            return render_template('singlepost.html', blog=new_blog)
        else:
            flash('Blog title or body is empty')
            redirect('/newpost')


@app.route('/blog', methods=['GET'])
def showpost():
    if request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template('singlepost.html', blog=blog)
    elif request.args.get('user'):
        return redirect('/singleuser', current_user=user.username, blogs=blogs)
    else:
        return redirect('/')


@app.route('/singleuser', methods=['GET'])
def showuser():
    if request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner=user_id).all()
        return render_template('singleuser.html', user=user, blogs=blogs)
    else:
        return redirect('/userlist')


@app.route('/userlist', methods=['GET'])
def getusers():
    users = User.query.all()
    if not users:
        flash('User list empty, please register!')
        return('/register')
    else:
        return render_template('userlist.html', users=users)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        del session['username']
        flash("You logged out")
    else:
        flash("You haven't logged in")
    return redirect('/')


if __name__ == '__main__':
    app.run()