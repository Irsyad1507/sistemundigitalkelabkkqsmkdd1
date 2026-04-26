from flask import render_template, redirect, url_for
from app import app, db, login_manager
from app.models import Admin, Calon, Pengundi
from flask_login import current_user
from functools import wraps


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id) or Pengundi.query.get(user_id)


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


@app.context_processor
def inject_admin():
    return dict(is_admin=isinstance(current_user, Admin))


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
    if current_user.is_authenticated and isinstance(current_user, Pengundi):
        for pengundi, calon in undian:
            if (
                pengundi.idPengundi == current_user.idPengundi
                and pengundi.idCalon != "C00"
            ):
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
