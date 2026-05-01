from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Pengundi

# from flask_login import login_required (UNCOMMENT ONCE AUTH ADDED)
# from .routes import require_admin (UNCOMMENT ONCE AUTH ADDED)

pengundi_bp = Blueprint("pengundi", __name__, url_prefix="/pengundi")


@pengundi_bp.get("/senarai")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_senarai():
    pengundi_list = Pengundi.query.all()
    return render_template(
        "pengundi/pengundi_senarai.html", pengundi_list=pengundi_list
    )


@pengundi_bp.route("/insert", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_insert():
    if request.method == "POST":
        idPengundi = request.form.get("idPengundi")
        namaPengundi = request.form.get("namaPengundi")
        password = request.form.get("password")
        if not idPengundi or not namaPengundi or not password:
            return render_template(
                "pengundi_insert.html", error="Sila isi semua medan."
            )
        new_pengundi = Pengundi(
            idPengundi=idPengundi,
            namaPengundi=namaPengundi,
            password=password,
            idCalon="C00",
        )
        db.session.add(new_pengundi)
        db.session.commit()
        flash("Berjaya tambah", "success")
        return redirect(url_for("pengundi.pengundi_insert"))
    return render_template("pengundi/pengundi_insert.html")


@pengundi_bp.route("/update/<idpengundi>", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_update(idpengundi):
    pengundi = Pengundi.query.get(idpengundi)
    if not pengundi:
        return "Pengundi not found", 404

    if request.method == "POST":
        idPengundi = request.form.get("idPengundi")
        namaPengundi = request.form.get("namaPengundi")
        password = request.form.get("password")

        if idPengundi:
            pengundi.idPengundi = idPengundi
        if namaPengundi:
            pengundi.namaPengundi = namaPengundi
        if password:
            pengundi.password = password
        db.session.commit()
        flash("Berjaya kemaskini", "success")
        return redirect(
            url_for("pengundi.pengundi_update", idpengundi=pengundi.idPengundi)
        )

    return render_template("pengundi/pengundi_update.html", pengundi=pengundi)


@pengundi_bp.delete("/delete/<idpengundi>")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_delete(idpengundi):
    pengundi = Pengundi.query.get(idpengundi)
    if not pengundi:
        return {"error": "Pengundi not found"}, 404
    db.session.delete(pengundi)
    db.session.commit()
    return {"message": "Deleted successfully"}, 200


@pengundi_bp.route("/carian")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_carian():
    pengundi_list = Pengundi.query.all()
    return render_template("pengundi/pengundi_carian.html", pengundi_list=pengundi_list)


@pengundi_bp.post("/maklumat")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def pengundi_maklumat():
    idpengundi = request.form.get("idPengundi")
    pengundi = Pengundi.query.get(idpengundi)
    if not pengundi:
        return "Pengundi not found", 404
    return render_template("pengundi/pengundi_maklumat.html", pengundi=pengundi)


@pengundi_bp.post("/undi")
def pengundi_undi():
    idpengundi = request.form.get("idPengundi")
    idcalon = request.form.get("idCalon")
    sudah_undi = False
    pengundi = Pengundi.query.get(idpengundi)
    if not pengundi:
        return "Pengundi not found", 404
    if pengundi.idCalon != "C00":
        sudah_undi = True
    if not sudah_undi:
        pengundi.idCalon = idcalon
        db.session.commit()
        flash("Berjaya undi", "success")
    else:
        flash("Anda sudah mengundi", "error")
    return redirect(url_for("index"))
