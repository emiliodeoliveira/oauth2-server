from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder='static')

    # These variables will be removed in the v1.1
    app.config['SECRET_KEY'] = 'R0JHkAVv2gZbIREwpsErsRqEzJh'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print("*********** WARNING ***********")
            print("ERROR: The following exception occurred: ")
            print("Failure on attempting to run db.create_all() in __init__.py: " + str(exception))
        finally:
            print("SUCCESS! db.create_all() in __init__.py was successfully executed!")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):

        from .models import User
        return User.query.get(user_id)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
