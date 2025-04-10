from flask import Flask, render_template

import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/start')
def start_virtual_mouse():
    subprocess.Popen(["python", "virtual_mouse.py"])
    return "Virtual Mouse Started"

if __name__ == '__main__':
    app.run(debug=True)