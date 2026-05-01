from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __abstract__ = True

    password_hash = db.Column(db.Text)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create String
    def __repr__(self):
        return "<Name %r>" % self.name


class Admin(User):
    __tablename__ = "admin"

    idAdmin = db.Column(db.String(3), primary_key=True)
    namaAdmin = db.Column(db.String(30))

    def get_id(self):
        return self.idAdmin


class Calon(db.Model):
    __tablename__ = "calon"

    idCalon = db.Column(db.String(3), primary_key=True)
    namaCalon = db.Column(db.String(20))
    gambar = db.Column(db.String(100))
    moto = db.Column(db.String(100))
    idAdmin = db.Column(db.String(3), db.ForeignKey("admin.idAdmin"))

    pengundi = db.relationship("Pengundi", backref="calon")


class Pengundi(User):
    __tablename__ = "pengundi"

    idPengundi = db.Column(db.String(4), primary_key=True)
    namaPengundi = db.Column(db.String(30))
    idCalon = db.Column(db.String(3), db.ForeignKey("calon.idCalon"))

    def get_id(self):
        return self.idPengundi
