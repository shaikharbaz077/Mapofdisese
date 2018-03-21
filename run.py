import os
from app import app

app = Flask(__name__)

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000)), port=port
    app.run(host='https://skindiseasepredictionbymohmmad.herokuapp.com/', debug=True)
