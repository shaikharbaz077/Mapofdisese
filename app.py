import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h1>hello world</h1>"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port)
    #debug=True , port=port host='https://skindiseasepredictionbymohmmad.herokuapp.com/', 
