"""SP63 / TSP63 : secrets externalisés (paragraphe 3.1)."""

from app.config import Settings

from .outils import DEFAULT_SECRET_KEY


# Anomalie connue : sans .env, config.py retombe sur une clé secrète écrite en dur
def test_pas_de_cle_secrete_par_defaut(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    try:
        cle = Settings(_env_file=None).secret_key
    except Exception:
        return  # L'application refuse de démarrer sans clé : comportement attendu.
    assert cle != DEFAULT_SECRET_KEY


def test_cle_secrete_lue_depuis_l_environnement(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "cle-de-test-tres-longue-1234567890")
    assert Settings(_env_file=None).secret_key == "cle-de-test-tres-longue-1234567890"
