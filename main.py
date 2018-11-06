from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzassignment@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post):
        self.title = title
        self.post = post
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner' )

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
        post_id = add_post.id
        return redirect('/blog?id={0}'.format(post_id))
    return redirect('/')


@app.route('/signup')
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']



        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            username_good = len(username) >=4
            pass_good = password == verify and len(password) > 4

            if email_good and pass_good:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/')
            return "<h1>Invalid Information</h1>"
        else:
        #TODO - user better response messaging
           return "<h1>Duplicate user</h1>"
    
    return render_template('register.html')

@app.route('/login')
def login():
    if request.method == "POST":
        emausernameil = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            #session['username'] = username
            #flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            

    return render_template('login.html')

#@app.route('index')

#def logout():
    #return redirect('/blog')




if __name__ == '__main__':
    app.run()

