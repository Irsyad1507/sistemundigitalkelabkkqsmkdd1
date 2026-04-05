from flask import render_template, redirect, url_for, request
from app import app, db, login_manager
from app.models import Admin, Calon, Pengundi
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id) or Pengundi.query.get(user_id)


@app.route("/")
def index():
    senarai_calon = Calon.query.all()
    sudah_mengundi = False
    namaCalon = "NaN"
    undian = (
        db.session.query(Pengundi, Calon)
        .join(Calon, Pengundi.idCalon == Calon.idCalon)
        .all()
    )
    for pengundi, calon in undian:
        if pengundi.idPengundi == current_user.idPengundi and pengundi.idCalon != "C00":
            namaCalon = calon.namaCalon
            sudah_mengundi = True
            break
    return render_template(
        "index.html",
        senarai_calon=senarai_calon,
        current_user=current_user,
        sudah_mengundi=sudah_mengundi,
        namaCalon=namaCalon,
    )
