import uuid
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.secret_key = str(uuid.uuid4())
_login_manager = LoginManager()
_login_manager.init_app(app)

import foobar.views
