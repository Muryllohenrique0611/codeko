# -*- coding: utf-8 -*-
"""
Sistema de Desafio de Ressurreição e Disputa pelo Cinturão.
"""

from datetime import datetime, timedelta
from app import db


class ResurrectionChallenge:
    """Gerencia o Desafio de Ressurreição (recuperar dias perdidos)."""

    # Configurações
    QUESTIONS_COUNT = 15
    PASSING_THRESHOLD = 0.6  # 60%
    BONUS_XP = 250
    PENALTY_XP = -100

    @staticmethod
    def can_use_resurrection(user):
        """Verifica se o usuário pode usar o Desafio de Ressurreição."""
        if not user.resurrection_used_week:
            return True
        return False

    @staticmethod
    def activate_resurrection(user):
        """Ativa o Desafio de Ressurreição para o usuário."""
        if not ResurrectionChallenge.can_use_resurrection(user):
            return {"success": False, "error": "Já usou o desafio esta semana"}

        user.resurrection_used_week = True
        db.session.commit()

        return {
            "success": True,
            "message": f"Desafio de Ressurreição ativado! Responda {ResurrectionChallenge.QUESTIONS_COUNT} questões.",
            "questions_needed": ResurrectionChallenge.QUESTIONS_COUNT,
        }

    @staticmethod
    def process_resurrection_result(user, score):
        """Processa o resultado do Desafio de Ressurreição."""
        passed = score >= ResurrectionChallenge.PASSING_THRESHOLD

        if passed:
            # Ressurreição aprovada: mata 2 dias, +250 XP
            user.xp += ResurrectionChallenge.BONUS_XP
            user.streak += 2
            message = f"[RESSURREICAO APROVADA] +{ResurrectionChallenge.BONUS_XP} XP! Combo +2 dias."
        else:
            # Ressurreição reprovada: perde o dobro
            user.xp += ResurrectionChallenge.PENALTY_XP
            message = f"[RESSURREICAO REPROVADA] {ResurrectionChallenge.PENALTY_XP} XP"

        # Perde direito ao desafio do cinturão esta semana
        user.champion_challenge_used_week = True

        db.session.commit()

        return {
            "success": passed,
            "passed": passed,
            "message": message,
            "xp_change": ResurrectionChallenge.BONUS_XP if passed else ResurrectionChallenge.PENALTY_XP,
            "total_xp": user.xp,
        }


class BeltChampion:
    """Gerencia o sistema do Cinturão (disputa pelo título)."""

    # Configurações
    QUESTIONS_COUNT = 10
    TIME_PER_QUESTION = 15  # segundos
    TOP_ELIGIBLE = 3  # Top 3 pode desafiar
    CHAMPION_XP = 500
    LOSER_XP = -150
    SOLO_DEFENSE_THRESHOLD = 0.7  # 70% para defender solo

    @staticmethod
    def is_eligible_to_challenge(user):
        """Verifica se o usuário pode desafiar o campeão."""
        if user.category != "pro":
            return False

        if user.ranking_position > BeltChampion.TOP_ELIGIBLE:
            return False

        if user.champion_challenge_used_week:
            return False

        return True

    @staticmethod
    def get_champion(category):
        """Retorna o campeão atual de uma categoria."""
        from app.models import User
        return User.query.filter_by(category=category, is_champion=True).first()

    @staticmethod
    def initiate_challenge(challenger, champion):
        """Inicia uma disputa entre desafiante e campeão."""
        if not BeltChampion.is_eligible_to_challenge(challenger):
            return {"success": False, "error": "Nao apto a desafiar"}

        challenger.champion_challenge_used_week = True
        db.session.commit()

        return {
            "success": True,
            "challenger": challenger.name,
            "champion": champion.name,
            "questions_count": BeltChampion.QUESTIONS_COUNT,
            "time_per_question": BeltChampion.TIME_PER_QUESTION,
        }

    @staticmethod
    def process_challenge_result(challenger_score, champion_score, challenger, champion):
        """Processa o resultado da disputa pelo cinturão."""
        challenger_correct = int(challenger_score * BeltChampion.QUESTIONS_COUNT)
        champion_correct = int(champion_score * BeltChampion.QUESTIONS_COUNT)

        if challenger_correct > champion_correct:
            # Desafiante vence
            challenger.is_champion = True
            champion.is_champion = False
            challenger.xp += BeltChampion.CHAMPION_XP
            result = "challenger_wins"
            message = f"[NOVO CAMPEAO] Venceu o cinturao! +{BeltChampion.CHAMPION_XP} XP"
        else:
            # Campeão defende
            champion.xp += BeltChampion.CHAMPION_XP // 2  # Bônus menor por defender
            challenger.xp += BeltChampion.LOSER_XP
            result = "champion_defends"
            message = f"[DERROTA] Nao conseguiu o titulo. {BeltChampion.LOSER_XP} XP"

        db.session.commit()

        return {
            "success": True,
            "result": result,
            "challenger_correct": challenger_correct,
            "champion_correct": champion_correct,
            "message": message,
            "new_champion": challenger.name if result == "challenger_wins" else champion.name,
        }

    @staticmethod
    def champion_solo_defense(champion):
        """Defesa solo do campeão (quando ninguém desafia)."""
        return {
            "champion": champion.name,
            "questions_count": BeltChampion.QUESTIONS_COUNT,
            "passing_threshold": BeltChampion.SOLO_DEFENSE_THRESHOLD,
            "message": f"Campeao deve acertar {int(BeltChampion.SOLO_DEFENSE_THRESHOLD * 100)}% para manter o cinturao",
        }

    @staticmethod
    def process_solo_defense(champion, score):
        """Processa defesa solo do campeão."""
        if score >= BeltChampion.SOLO_DEFENSE_THRESHOLD:
            champion.xp += BeltChampion.CHAMPION_XP // 2
            return {
                "success": True,
                "defended": True,
                "message": f"[DEFESA SUCESSO] Manteu o cinturao! +{BeltChampion.CHAMPION_XP // 2} XP",
            }
        else:
            # Cinturão fica vago
            champion.is_champion = False
            db.session.commit()

            return {
                "success": True,
                "defended": False,
                "message": "[CINTURAO VAGO] Qualquer Top 3 pode assumir o titulo!",
            }
