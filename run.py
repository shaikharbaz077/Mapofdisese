import os
from app import app

#app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(host='https://skindiseasepredictionbymohmmad.herokuapp.com/', debug=True , port=port)
