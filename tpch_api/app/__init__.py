from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from .routes import region, nation, part, supplier, partsupp, customer, orders, lineitem
        app.register_blueprint(region.bp)
        app.register_blueprint(nation.bp)
        app.register_blueprint(part.bp)
        app.register_blueprint(supplier.bp)
        app.register_blueprint(partsupp.bp)
        app.register_blueprint(customer.bp)
        app.register_blueprint(orders.bp)
        app.register_blueprint(lineitem.bp)
        
        db.create_all()

    return app
