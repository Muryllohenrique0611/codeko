from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Module, Question, UserProgress, BattleHistory
from app import db
from datetime import date

api_bp = Blueprint("api", __name__)


# --- Usuário ---

@api_bp.route("/user/profile")
@login_required
def get_profile():
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "avatar": current_user.avatar,
        "category": current_user.category,
        "xp": current_user.xp,
        "ranking_position": current_user.ranking_position,
        "is_champion": current_user.is_champion,
        "fights": current_user.fights,
        "wins": current_user.wins,
        "knockouts": current_user.knockouts,
        "losses": current_user.losses,
        "streak": current_user.streak,
    })


# --- Módulos ---

@api_bp.route("/modules")
@login_required
def get_modules():
    modules = Module.query.filter_by(category=current_user.category).order_by(Module.order).all()
    result = []
    for m in modules:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id, module_id=m.id
        ).first()
        result.append({
            "id": m.id,
            "number": m.number,
            "name": m.name,
            "description": m.description,
            "category": m.category,
            "completed": progress.completed if progress else False,
            "score": progress.score if progress else 0.0,
        })
    return jsonify(result)


# --- Questões ---

@api_bp.route("/questions")
@login_required
def get_questions():
    import json
    import random

    module_id = request.args.get("module_id", type=int)
    limit = request.args.get("limit", default=10, type=int)

    if not module_id:
        return jsonify({"error": "module_id is required"}), 400

    questions = Question.query.filter_by(module_id=module_id).limit(limit).all()

    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "type": q.type,
            "statement": q.statement,
            "code_snippet": q.code_snippet,
            "options": json.loads(q.options) if q.options else [],
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "level": q.level,
        })

    random.shuffle(result)
    return jsonify(result)
@login_required
def get_daily_questions():
    import random
    import json

    # 7 questões do módulo atual + 3 de módulos anteriores
    current_progress = UserProgress.query.filter_by(
        user_id=current_user.id, completed=False
    ).first()

    questions = []

    if current_progress:
        current_qs = Question.query.filter_by(module_id=current_progress.module_id).all()
        questions += random.sample(current_qs, min(7, len(current_qs)))

    previous_modules = Module.query.filter(
        Module.category == current_user.category,
        Module.order < (current_progress.module_id if current_progress else 99)
    ).all()

    if previous_modules:
        prev_ids = [m.id for m in previous_modules]
        prev_qs = Question.query.filter(Question.module_id.in_(prev_ids)).all()
        questions += random.sample(prev_qs, min(3, len(prev_qs)))

    random.shuffle(questions)

    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "type": q.type,
            "statement": q.statement,
            "code_snippet": q.code_snippet,
            "options": json.loads(q.options) if q.options else [],
            "level": q.level,
        })

    return jsonify(result)


# --- Progresso ---

@api_bp.route("/progress/submit", methods=["POST"])
@login_required
def submit_task():
    data = request.get_json()
    correct = data.get("correct", 0)
    total = data.get("total", 10)
    score = correct / total

    today = date.today()

    # Registrar resultado na ficha do lutador
    current_user.fights += 1
    current_user.last_task_date = today

    if score == 1.0:
        current_user.knockouts += 1
        current_user.xp += 150
        result = "knockout"
        xp_gained = 150
    else:
        current_user.wins += 1
        current_user.xp += 100
        result = "win"
        xp_gained = 100

    current_user.streak += 1

    battle = BattleHistory(
        user_id=current_user.id,
        type="daily_task",
        result=result,
        score=score,
        xp_gained=xp_gained,
    )
    db.session.add(battle)
    db.session.commit()

    return jsonify({
        "result": result,
        "xp_gained": xp_gained,
        "total_xp": current_user.xp,
        "streak": current_user.streak,
    })


# --- Ranking ---

@api_bp.route("/ranking/<category>")
@login_required
def get_ranking(category):
    from app.models import User
    users = User.query.filter_by(category=category).order_by(User.xp.desc()).limit(20).all()
    result = []
    for i, u in enumerate(users):
        result.append({
            "position": i + 1,
            "name": u.name,
            "avatar": u.avatar,
            "xp": u.xp,
            "knockouts": u.knockouts,
            "wins": u.wins,
            "is_champion": u.is_champion,
        })
    return jsonify(result)
