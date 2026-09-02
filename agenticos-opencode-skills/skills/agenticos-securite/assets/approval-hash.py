"""Validation humaine liée au hash de l'action — AgenticOS.

L'approbation porte sur l'EMPREINTE de l'action canonisée : toute
reformulation (même cosmétique) invalide l'approbation. C'est le
contre-mesure au contournement par reformulation détecté en audit.

Preuve de fin : approuver une action, modifier un seul caractère du
payload, vérifier que verify_approval() lève ApprovalMismatch.
"""

import hashlib
import hmac
import json
import time


class ApprovalMismatch(Exception):
    """L'action soumise ne correspond pas à l'action approuvée."""


def canonical_hash(action: dict) -> str:
    """Empreinte stable de l'action : sérialisation canonique (clés triées)."""
    blob = json.dumps(action, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


def request_approval(action: dict) -> dict:
    """Crée une demande d'approbation attachée au hash de l'action."""
    return {
        "action_hash": canonical_hash(action),
        "requested_at": time.time(),
        "status": "pending",  # pending → approved | rejected
    }


def verify_approval(approval: dict, action: dict) -> None:
    """Bloque l'exécution si l'action diffère de celle approuvée.

    Comparaison en temps constant pour éviter toute fuite par timing.
    Lève ApprovalMismatch si : non approuvée, hash différent, ou expirée.
    """
    if approval.get("status") != "approved":
        raise ApprovalMismatch("action non approuvée")
    if not hmac.compare_digest(approval["action_hash"], canonical_hash(action)):
        raise ApprovalMismatch(
            "l'action a été modifiée après approbation — exécution refusée"
        )
    if time.time() - approval["requested_at"] > 3600:
        raise ApprovalMismatch("approbation expirée (> 1 h)")


# Jamais d'--auto-approve sur ce chemin en prod : la validation humaine
# est le seul moyen de faire passer status à "approved".
