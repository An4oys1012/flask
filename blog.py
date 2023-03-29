import sqlite3
from flask import Flask, render_template, request, flash, url_for, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute("""SELECT * FROM posts WHERE id = ?""",
                        (post_id, )).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute("""SELECT * FROM posts;""").fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:post_id>')
def post(post_id):
    #return "THIS IS POST PAGE"
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content are both required')
        else:
            conn = get_db_connection()
            conn.execute("""UPDATE posts SET title = ?, content = ? WHERE id = ?""",
                        (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


# def create():
#     return "CREATE POST"
@app.route('/create-post', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content are both required')
        else:
            conn = get_db_connection()
            conn.execute("""INSERT INTO posts (title, content) VALUES (?,?)""",
                        (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:post_id>/delete', methods=['POST',])
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    conn.execute("""DELETE FROM posts WHERE id = ?""", (post_id, ))
    conn.commit()
    conn.close()
    flash(f"Post {post['title']} was successfully eleted")
    return redirect(url_for('index'))




app.run()