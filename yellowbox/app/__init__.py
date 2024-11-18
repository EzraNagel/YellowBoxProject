from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='config.Config'):
    app = Flask(__name__, static_folder='static', static_url_path='/static')


    app.config.from_object(config_name)

    db.init_app(app)


    from .base import base as base_blueprint
    from .customers import customers as customers_blueprint
    from .kiosks import kiosks as kiosks_blueprint
    from .orders import orders as orders_blueprint
    from .movies import movies as movies_blueprint

    app.register_blueprint(base_blueprint)
    app.register_blueprint(customers_blueprint)
    app.register_blueprint(kiosks_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(movies_blueprint)

    return app
