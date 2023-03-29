from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return "<h1>Hello World</h1>"

@app.route('/hello')
@app.route('/hello/<name>')
def greating(name=None):
    return render_template('hello.html', name=name)

app.run()

