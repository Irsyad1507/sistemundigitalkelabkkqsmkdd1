from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager
from app.models import Admin, Calon, Pengundi
from flask_login import current_user, login_user, logout_user
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
    return dict(
        is_admin=current_user.is_authenticated and isinstance(current_user, Admin)
    )


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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        idPengundi = request.form.get("idPengundi")
        namaPengundi = request.form.get("namaPengundi")
        password = request.form.get("password")

        existing_pengundi = Pengundi.query.filter_by(idPengundi=idPengundi).first()
        if existing_pengundi:
            flash("ID Pengundi sudah digunakan. Sila pilih ID lain.", "danger")
            return render_template("signup.html", error="ID Pengundi sudah digunakan.")
        new_pengundi = Pengundi(
            idPengundi=idPengundi,
            namaPengundi=namaPengundi,
            password=password,
            idCalon="C00",
        )
        db.session.add(new_pengundi)
        db.session.commit()
        flash("Pengguna berjaya didaftar.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        idPengguna = request.form.get("idPengguna")
        password = request.form.get("password")

        user = (
            Admin.query.filter_by(idAdmin=idPengguna).first()
            or Pengundi.query.filter_by(idPengundi=idPengguna).first()
        )
        if user and user.verify_password(password):
            login_user(user)
            flash("Berjaya log masuk.", "success")
            if isinstance(user, Admin):
                return redirect(url_for("calon.calon_senarai"))
            return redirect(url_for("index"))
        else:
            flash("ID Pengguna atau kata laluan salah.", "danger")
            return render_template(
                "login.html", error="ID Pengguna atau kata laluan salah."
            )
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Berjaya log keluar.", "success")
    return redirect(url_for("index"))
