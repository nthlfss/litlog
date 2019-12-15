"""

Executes initialization code for the package

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b684669c44c840b74452cc01fcb1a36c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booklog.db'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Initiate database
db = SQLAlchemy(app)
# Hashing tool (for passwords)
bcrypt = Bcrypt(app)
# User session management. Handles logging in and out, and remembering users' sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from litlog import routes