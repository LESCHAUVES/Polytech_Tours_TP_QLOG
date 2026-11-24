"""Fixtures communes aux tests de sécurité.

La base SQLite et le dossier d'upload sont redirigés vers un dossier
temporaire AVANT l'import de l'application : les tests ne touchent jamais
padel_corpo.db ni backend/uploads.
"""
import os
import tempfile

_TMP = tempfile.mkdtemp(prefix="padel-secu-")
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_TMP, 'test.db')}"
os.environ["UPLOAD_DIR"] = os.path.join(_TMP, "uploads")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Player, Pool, Team, User  # noqa: E402
from app.security import hash_password  # noqa: E402

from .outils import (  # noqa: E402
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    PLAYER_EMAIL,
    PLAYER_PASSWORD,
    login,
)


@pytest.fixture()
def data():
    """Base vide puis jeu de données minimal : 1 admin, 3 joueurs, 1 équipe, 1 poule."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin = User(email=ADMIN_EMAIL, password_hash=hash_password(ADMIN_PASSWORD),
                 role="ADMINISTRATEUR")
    joueur = User(email=PLAYER_EMAIL, password_hash=hash_password(PLAYER_PASSWORD),
                  role="JOUEUR")
    db.add_all([admin, joueur])
    db.flush()
    p1 = Player(first_name="Alice", last_name="Martin", company="Acme",
                license_number="L000001", email=PLAYER_EMAIL, user_id=joueur.id)
    p2 = Player(first_name="Bruno", last_name="Petit", company="Acme",
                license_number="L000002", email="bruno@test.fr")
    p3 = Player(first_name="Chloe", last_name="Roux", company="Acme",
                license_number="L000003", email="chloe@test.fr")
    p4 = Player(first_name="David", last_name="Noir", company="Acme",
                license_number="L000004", email="david@test.fr")
    db.add_all([p1, p2, p3, p4])
    db.flush()
    pool = Pool(name="Poule A")
    db.add(pool)
    db.flush()
    team = Team(company="Acme", player1_id=p1.id, player2_id=p2.id, pool_id=pool.id)
    db.add(team)
    db.commit()
    ids = {"admin": admin.id, "joueur": joueur.id, "p1": p1.id, "p2": p2.id,
           "p3": p3.id, "p4": p4.id, "team": team.id, "pool": pool.id}
    db.close()
    return ids


@pytest.fixture()
def client(data):
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture()
def admin_headers(client):
    token = login(client, ADMIN_EMAIL, ADMIN_PASSWORD).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def player_headers(client):
    token = login(client, PLAYER_EMAIL, PLAYER_PASSWORD).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
