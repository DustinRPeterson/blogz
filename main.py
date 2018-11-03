from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildingblogs@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog_main():
    posts = Blog.query.all()
    return render_template('blog.html', title="Blog", posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        add_post = Blog(blog_title, blog_post)
        db.session.add(add_post)
        db.session.commit()
    return redirect('/blog')





class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.Text)

    def __init__(self, title, post):
        self.title = title
        self.post = post


if __name__ == '__main__':
    app.run()

