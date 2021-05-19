from flask import Flask, render_template
from app.temp_data import people, block_files
app = Flask(__name__, static_url_path='/static')
# app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', people=people)


@app.route('/files')
def files():
    return render_template('files.html', block_files=block_files)

