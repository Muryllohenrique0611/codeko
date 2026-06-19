from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("index.html")


@main_bp.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)


@main_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@main_bp.route("/ranking")
@login_required
def ranking():
    return render_template("ranking.html", user=current_user)


@main_bp.route("/modules")
@login_required
def modules():
    from app.models import Module
    modules = Module.query.filter_by(category=current_user.category).order_by(Module.order).all()
    return render_template("modules.html", user=current_user, modules=modules)


@main_bp.route("/quiz/<int:module_id>")
@login_required
def quiz(module_id):
    from app.models import Module
    module = Module.query.get_or_404(module_id)
    return render_template("quiz.html", user=current_user, module=module, module_id=module_id)


@main_bp.route("/code-executor")
@login_required
def code_executor():
    return render_template("code_executor.html", user=current_user)
