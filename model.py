from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)

    reservations = db.relationship('Reservation', back_populates='user')

    def __repr__(self):
        return f'<User email={self.email}>'

class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    user = db.relationship('User', back_populates='reservations')

    def __repr__(self):
        return f'<Reservation user={self.user.email} time={self.time}>'

def connect_to_db(app):
    with app.app_context():
        POSTGRES_DB = os.environ["POSTGRES_DB"]
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{POSTGRES_DB}'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.app = app
        db.init_app(app)
        db.create_all()
        db.session.commit()
