from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import app, db
from .models import Admin, Calon
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# from flask_login import login_required (UNCOMMENT ONCE AUTH ADDED)
# from .routes import require_admin (UNCOMMENT ONCE AUTH ADDED)

calon_bp = Blueprint("calon", __name__, url_prefix="/calon")


@calon_bp.get("/senarai")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def calon_senarai():
    senarai_calon = Calon.query.all()
    return render_template("calon/calon_senarai.html", senarai_calon=senarai_calon)


@calon_bp.route("/insert", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def calon_insert():
    admin = Admin.query.all()
    if request.method == "POST":
        idCalon = request.form.get("idCalon")
        namaCalon = request.form.get("namaCalon")
        moto = request.form.get("moto")
        idAdmin = request.form.get("idAdmin")
        if not idCalon or not namaCalon or not moto or not idAdmin:
            return render_template(
                "calon/calon_insert.html", admin=admin, error="Sila isi semua medan."
            )

        if request.files.get("gambar"):
            gambar_file = request.files.get("gambar")

            gambar_filename = secure_filename(gambar_file.filename)
            gambar = f"{uuid.uuid4().hex}_{gambar_filename}"
            saved = request.files.get("gambar")

            new_calon = Calon(
                idCalon=idCalon,
                namaCalon=namaCalon,
                gambar=gambar,
                moto=moto,
                idAdmin=idAdmin,
            )
            db.session.add(new_calon)
            try:
                db.session.commit()
                saved.save(os.path.join(app.config["UPLOAD_FOLDER"], gambar))
                flash("Berjaya tambah", "success")
                return redirect(url_for("calon.calon_insert"))
            except Exception as e:
                db.session.rollback()
                flash(f"Ralat: {str(e)}", "error")
                return render_template("calon/calon_insert.html", admin=admin)
        else:
            flash("Sila muat naik gambar", "error")
            return render_template("calon/calon_insert.html", admin=admin)
    else:
        return render_template("calon/calon_insert.html", admin=admin)


@calon_bp.route("/update/<idcalon>", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def calon_update(idcalon):
    calon = Calon.query.get(idcalon)
    if not calon:
        return "Calon not found", 404
    if request.method == "POST":
        idCalon = request.form.get("idCalon")
        namaCalon = request.form.get("namaCalon")
        moto = request.form.get("moto")
        if not idCalon or not namaCalon or not moto:
            return render_template(
                "calon/calon_update.html", calon=calon, error="Sila isi semua medan."
            )

        if request.files.get("gambar"):
            gambar_file = request.files.get("gambar")

            gambar_filename = secure_filename(gambar_file.filename)
            gambar = f"{uuid.uuid4().hex}_{gambar_filename}"
            saved = request.files.get("gambar")

            if idCalon:
                calon.idCalon = idCalon
            if namaCalon:
                calon.namaCalon = namaCalon
            if moto:
                calon.moto = moto
            calon.gambar = gambar
            try:
                db.session.commit()
                saved.save(os.path.join(app.config["UPLOAD_FOLDER"], gambar))
                flash("Berjaya kemaskini", "success")
                return redirect(url_for("calon.calon_update", idcalon=calon.idCalon))
            except Exception as e:
                db.session.rollback()
                flash(f"Ralat: {str(e)}", "error")
                return render_template("calon/calon_update.html", calon=calon)
        else:
            flash("Sila muat naik gambar", "error")
            return render_template("calon/calon_update.html", calon=calon)
    else:
        return render_template("calon/calon_update.html", calon=calon)


@calon_bp.delete("/delete/<idcalon>")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def calon_delete(idcalon):
    calon = Calon.query.get(idcalon)
    if not calon:
        return {"error": "Calon not found"}, 404
    db.session.delete(calon)
    db.session.commit()
    return {"message": "Deleted successfully"}, 200


@calon_bp.route("/profil")
def calon_profil():
    profil_calon = Calon.query.all()
    return render_template("calon/calon_profil.html", profil_calon=profil_calon)
