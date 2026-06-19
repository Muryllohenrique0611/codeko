from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Module, Question, UserProgress, BattleHistory
from app.utils import CodeExecutor
from app.utils.belt_system import ResurrectionChallenge, BeltChampion
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
    from datetime import datetime, timedelta

    data = request.get_json()
    module_id = data.get("module_id")
    correct = data.get("correct", 0)
    total = data.get("total", 10)
    score = correct / total if total > 0 else 0

    today = date.today()

    # Verificar se já fez tarefa hoje
    last_fight = BattleHistory.query.filter_by(
        user_id=current_user.id,
        type="daily_task"
    ).order_by(BattleHistory.created_at.desc()).first()

    if last_fight and last_fight.created_at.date() == today:
        return jsonify({"error": "Você já completou sua tarefa de hoje!"}), 400

    # Registrar resultado na ficha do lutador
    current_user.fights += 1

    # Atualizar combo (streak)
    yesterday = today - timedelta(days=1)
    if last_fight and last_fight.created_at.date() == yesterday:
        # Mantém o combo
        current_user.streak += 1
    elif not last_fight or last_fight.created_at.date() < yesterday:
        # Reseta o combo
        current_user.streak = 1
    else:
        current_user.streak = 1

    current_user.last_task_date = today

    # Calcular XP baseado no resultado
    if score == 1.0:
        current_user.knockouts += 1
        xp_gained = 150  # Nocaute = perfeição
        result = "knockout"
    elif score >= 0.6:
        current_user.wins += 1
        xp_gained = 100  # Vitória
        result = "win"
    else:
        current_user.losses += 1
        xp_gained = -50  # Derrota
        result = "loss"

    # Adicionar combo bonus (5 XP por dia consecutivo)
    combo_bonus = current_user.streak * 5
    total_xp_gained = xp_gained + combo_bonus

    current_user.xp += total_xp_gained

    # Registrar na história de batalhas
    battle = BattleHistory(
        user_id=current_user.id,
        type="daily_task",
        result=result,
        score=score,
        xp_gained=total_xp_gained,
    )

    # Registrar progresso do módulo
    if module_id:
        module = Module.query.get(module_id)
        if module:
            progress = UserProgress.query.filter_by(
                user_id=current_user.id,
                module_id=module_id
            ).first()

            if not progress:
                progress = UserProgress(
                    user_id=current_user.id,
                    module_id=module_id,
                    completed=score >= 0.6,
                    score=score,
                    completed_at=datetime.utcnow() if score >= 0.6 else None
                )
                db.session.add(progress)
            else:
                progress.score = max(progress.score, score)
                if score >= 0.6:
                    progress.completed = True
                    progress.completed_at = datetime.utcnow()

    db.session.add(battle)
    db.session.commit()

    # Atualizar ranking
    update_ranking()

    return jsonify({
        "result": result,
        "xp_gained": total_xp_gained,
        "combo_bonus": combo_bonus,
        "total_xp": current_user.xp,
        "streak": current_user.streak,
        "ranking_position": current_user.ranking_position,
    })


# --- Execução de Código ---

@api_bp.route("/code/execute", methods=["POST"])
@login_required
def execute_code():
    """Executa código Python de forma segura."""
    data = request.get_json()
    code = data.get("code", "")
    test_input = data.get("input", "")

    if not code:
        return jsonify({"error": "Código vazio"}), 400

    # Validar código antes de executar
    validation = CodeExecutor.validate_code(code)
    if not validation["valid"]:
        return jsonify({
            "success": False,
            "error": "Código contém construções não permitidas",
            "warnings": validation["warnings"]
        }), 400

    # Executar código
    result = CodeExecutor.execute_with_input(code, test_input, timeout=5)

    return jsonify(result)


@api_bp.route("/code/validate", methods=["POST"])
@login_required
def validate_code():
    """Valida código sem executar."""
    data = request.get_json()
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Código vazio"}), 400

    validation = CodeExecutor.validate_code(code)

    return jsonify(validation)

def update_ranking():
    """Atualiza posições de ranking por categoria"""
    from app.models import User

    for category in ["iniciante", "intermediario", "pro"]:
        users = User.query.filter_by(category=category).order_by(User.xp.desc()).all()
        for position, user in enumerate(users, 1):
            user.ranking_position = position

    db.session.commit()


@api_bp.route("/ranking/<category>")
@login_required
def get_ranking(category):
    from app.models import User

    if category not in ["iniciante", "intermediario", "pro"]:
        return jsonify({"error": "Categoria inválida"}), 400

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
            "losses": u.losses,
            "streak": u.streak,
            "is_champion": u.is_champion,
            "is_current_user": u.id == current_user.id,
        })

    return jsonify(result)
