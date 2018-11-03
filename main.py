from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildingblogs@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.Text)

    def __init__(self, title, post):
        self.title = title
        self.post = post

def check_post(title, post):
    #Checks to verify if the post provided has a title and content
    if title == '' or post == '':
        return False
    else:
        return True

@app.route('/')
def index():
    #The main page will be the blog page that displays all posts
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog_main():
    posts = Blog.query.all()
    link_to_post = request.args.get('id')
    if link_to_post:
        posts = Blog.query.filter_by(id=link_to_post).all()
        return render_template('blog.html', title="Blog", posts=posts)
    return render_template('blog.html', title="Blog", posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    

    return render_template('newpost.html')

@app.route('/add-post', methods=['POST'])
def add_post():


    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        valid_post = check_post(blog_title, blog_post)
        if valid_post == False:
            #if post is invalid re-render newpost page with an error message
            return render_template('/newpost.html', valid_post=valid_post)
        add_post = Blog(blog_title, blog_post)
        db.session.add(add_post)
        db.session.commit()
        newest_post= Blog.query.filter_by(title=blog_title).first()
        post_id = newest_post.id
        return render_template('blog.html/?id={post_id}'.format(post_id))
    return redirect('/')







if __name__ == '__main__':
    app.run()

