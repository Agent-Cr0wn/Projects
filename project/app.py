from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

# Dummy data for blog posts
POSTS = [
    {
        'title': 'First post',
        'content': 'This is the content of the first post.',
        'author': 'John Doe',
        'timestamp': datetime.strptime('2022-01-01', '%Y-%m-%d')
    },
    {
        'title': 'Second post',
        'content': 'This is the content of the second post.',
        'author': 'Jane Doe',
        'timestamp': datetime.strptime('2022-01-02', '%Y-%m-%d')
    }
]

# Helper function to get a post by its title
def get_post(title):
    for post in POSTS:
        if post['title'] == title:
            return post
    return None

@app.route('/')
def index():
    return render_template('index.html', posts=POSTS)

@app.route('/post/<title>')
def post(title):
    post = get_post(title)
    if not post:
        flash('Post not found!')
        return redirect(url_for('index'))
    return render_template('post.html', post=post)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        timestamp = datetime.now()
        POSTS.append({
            'title': title,
            'content': content,
            'author': author,
            'timestamp': timestamp
        })
        flash('Post created successfully!')
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in USERS:
            if user['username'] == username and check_password_hash(user['password'], password):
                session['username'] = username
                session['logged_in'] = True
                flash('Logged in successfully!')
                return redirect(url_for('index'))
        flash('Incorrect username or password!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        USERS.append({'username': username, 'password': password_hash})
        flash('Registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('Logged out successfully!')
    return redirect(url_for('index'))
