from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    avatar = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.Column(db.String(20), default="iniciante")
    xp = db.Column(db.Integer, default=0)
    ranking_position = db.Column(db.Integer, default=0)
    is_champion = db.Column(db.Boolean, default=False)

    fights = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    knockouts = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    last_task_date = db.Column(db.Date)
    streak = db.Column(db.Integer, default=0)
    resurrection_used_week = db.Column(db.Boolean, default=False)
    champion_challenge_used_week = db.Column(db.Boolean, default=False)

    progress = db.relationship("UserProgress", backref="user", lazy=True)
    battles = db.relationship("BattleHistory", backref="user", lazy=True)


class Module(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(20), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    questions = db.relationship("Question", backref="module", lazy=True)


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    code_snippet = db.Column(db.Text)
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)
    explanation = db.Column(db.Text)


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float, default=0.0)
    completed_at = db.Column(db.DateTime)


class BattleHistory(db.Model):
    __tablename__ = "battle_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    result = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Float)
    xp_gained = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)