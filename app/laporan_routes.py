from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Calon, Pengundi
from sqlalchemy import func, desc

from flask_login import login_required
from .routes import require_admin

laporan_bp = Blueprint("laporan", __name__, url_prefix="/laporan")


@laporan_bp.get("/pilih")
@login_required
@require_admin
def laporan_pilih():
    return render_template("laporan/laporan_pilih.html")


@laporan_bp.post("/cetak")
@login_required
@require_admin
def laporan_cetak():
    pilihan = request.form.get("pilih")
    keputusan = (
        db.session.query(
            Calon.idCalon,
            Calon.namaCalon,
            func.count(Pengundi.idPengundi).label("jum_ikut_calon"),
        )
        .join(Pengundi, Calon.idCalon == Pengundi.idCalon)
        .group_by(Calon.idCalon, Calon.namaCalon)
        .order_by(desc("jum_ikut_calon"))
        .all()
    )
    if pilihan == "1":
        return render_template(
            "laporan/laporan_cetak.html", keputusan=keputusan, pilihan=pilihan
        )
    elif pilihan == "2":
        jum_semua_undi = Pengundi.query.filter(Pengundi.idCalon != "C00").count()
        return render_template(
            "laporan/laporan_cetak.html",
            keputusan=keputusan,
            pilihan=pilihan,
            jum_semua_undi=jum_semua_undi,
        )
