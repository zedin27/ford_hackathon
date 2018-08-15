import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder="resources")
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, "database.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize DB
    from vehicle_client.models import db
    db.init_app(app)
    db.create_all(app=app)

    # Initialize Blueprints
    from . import local
    app.register_blueprint(local.bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app