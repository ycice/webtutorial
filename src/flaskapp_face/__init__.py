import os
from flask import Flask

app = Flask(__name__)
USER_IMG_DIR = os.path.join(os.path.dirname(__file__), 'user_imgs')


import flaskapp_face.views
