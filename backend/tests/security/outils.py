"""Constantes et fonctions utilitaires des tests de sécurité."""
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import settings

API = "/api/v1"
ADMIN_EMAIL = "admin@test.fr"
ADMIN_PASSWORD = "Admin@2025!xx"
PLAYER_EMAIL = "joueur@test.fr"
PLAYER_PASSWORD = "Joueur@2025!x"

# Clé écrite en dur dans app/config.py et dans .env.example.
DEFAULT_SECRET_KEY = "dev-secret-key-change-me-in-production"


def login(client, email, password):
    return client.post(f"{API}/auth/login", json={"email": email, "password": password})


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def make_token(user_id, role, key=None, minutes=60, algorithm="HS256", email="x@test.fr"):
    """Fabrique un JWT comme le ferait un attaquant (clé et expiration au choix)."""
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, key or settings.secret_key, algorithm=algorithm)
