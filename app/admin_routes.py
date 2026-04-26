from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Admin

# from flask_login import login_required (UNCOMMENT ONCE AUTH ADDED)
# from .routes import require_admin (UNCOMMENT ONCE AUTH ADDED)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/senarai")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def admin_senarai():
    admins = Admin.query.all()
    return render_template("admin/admin_senarai.html", admins=admins)


@admin_bp.route("/insert", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def admin_insert():
    if request.method == "POST":
        idAdmin = request.form.get("idAdmin")
        namaAdmin = request.form.get("namaAdmin")
        password = request.form.get("password")
        if not idAdmin or not namaAdmin or not password:
            return render_template("admin_insert.html", error="Sila isi semua medan.")
        new_admin = Admin(idAdmin=idAdmin, namaAdmin=namaAdmin, password=password)
        db.session.add(new_admin)
        db.session.commit()
        flash("Berjaya tambah", "success")
        return redirect(url_for("admin.admin_insert"))
    return render_template("admin/admin_insert.html")


@admin_bp.route("/update/<idadmin>", methods=["GET", "POST"])
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def admin_update(idadmin):
    admin = Admin.query.get(idadmin)
    if not admin:
        return "Admin not found", 404

    if request.method == "POST":
        idAdmin = request.form.get("idAdmin")
        namaAdmin = request.form.get("namaAdmin")
        password = request.form.get("password")

        if idAdmin:
            admin.idAdmin = idAdmin
        if namaAdmin:
            admin.namaAdmin = namaAdmin
        if password:
            admin.password = password
        db.session.commit()
        flash("Berjaya kemaskini", "success")
        return redirect(url_for("admin.admin_update", idadmin=admin.idAdmin))

    return render_template("admin/admin_update.html", admin=admin)


@admin_bp.delete("/delete/<idadmin>")
# @login_required (UNCOMMENT ONCE AUTH ADDED)
# @require_admin (UNCOMMENT ONCE AUTH ADDED)
def admin_delete(idadmin):
    admin = Admin.query.get(idadmin)
    if not admin:
        return {"error": "Admin not found"}, 404
    db.session.delete(admin)
    db.session.commit()
    return {"message": "Deleted successfully"}, 200
