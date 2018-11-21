from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzassignment@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog_main', 'index']
    print(session)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner' )

    def __init__(self, username, password):
        self.username = username
        self.password = password

def check_post(title, post):
    #Checks to verify if the post provided has a title and content
    if title == '' or post == '':
        return False
    else:
        return True

@app.route('/')
def index():
    #The main page will be the blog page that displays all posts
    user_list = User.query.all()
    print(user_list)
    return render_template('index.html', user_list=user_list)

@app.route('/blog', methods=['POST', 'GET'])
def blog_main():
    posts = Blog.query.all()
    authors = User.query.all()
    link_to_post = request.args.get('id')
    by_user = request.args.get('user')
    if link_to_post:
        posts = Blog.query.filter_by(id=link_to_post).all()
        owner_id = posts[0].owner_id
        author = User.query.filter_by(id=owner_id).first()
        return render_template('blog.html', title="Blog", posts=posts, author=author)
    if by_user:
        user_id = User.query.filter_by(username = by_user).first()
        user_posts = Blog.query.filter_by(owner_id = user_id.id)
        return render_template('blog.html', title=by_user, posts=user_posts)
    return render_template('blog.html', title="Blog", posts=posts, authors=authors)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    

    return render_template('newpost.html')

@app.route('/add-post', methods=['POST'])
def add_post():

    owner = User.query.filter_by(username=session['username']).first()


    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        valid_post = check_post(blog_title, blog_post)
        if valid_post == False:
            #if post is invalid re-render newpost page with an error message
            return render_template('/newpost.html', valid_post=valid_post)
        add_post = Blog(blog_title, blog_post, owner)
        db.session.add(add_post)
        db.session.commit()
        post_id = add_post.id
        return redirect('/blog?id={0}'.format(post_id))
    return redirect('/')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username =='' or password == '' or verify == '':
            flash('One or more fields left blank')
            return render_template('signup.html')



        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            username_good = len(username) >=4
            pass_good = len(password) > 4

            if username_good and pass_good:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

            elif username_good == False:
                flash('Please provide a valid username')
                return render_template('signup.html')
            elif password != verify:
                flash('Password and confirmation do not match')
                return render_template('signup.html')
            elif pass_good == False:
                flash('Please provide a valid password')
                return render_template('signup.html')
        else:
            flash('Duplicate user')
    
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            #flash("Logged in")
            return redirect('/newpost')
        else:
            if user == None:
                flash('Invalid username')
            elif user.password != password:
                flash('The password provided is not valid')

    return render_template('login.html')

#@app.route('index')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')




if __name__ == '__main__':
    app.run()

