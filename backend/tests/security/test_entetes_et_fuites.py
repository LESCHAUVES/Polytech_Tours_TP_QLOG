"""SP69 et SP72 / TSP69 et TSP72 : en-têtes, CORS et fuite d'informations."""
import pytest

from .outils import API, PLAYER_EMAIL, PLAYER_PASSWORD, login

ORIGINE_AUTORISEE = "http://localhost:5173"


def test_cors_origine_non_autorisee(client):
    r = client.options(f"{API}/health", headers={
        "Origin": "http://site-malveillant.com",
        "Access-Control-Request-Method": "GET",
    })
    assert r.headers.get("access-control-allow-origin") != "http://site-malveillant.com"
    assert r.headers.get("access-control-allow-origin") != "*"


def test_cors_origine_autorisee(client):
    r = client.options(f"{API}/health", headers={
        "Origin": ORIGINE_AUTORISEE,
        "Access-Control-Request-Method": "GET",
    })
    assert r.headers.get("access-control-allow-origin") == ORIGINE_AUTORISEE


@pytest.mark.parametrize("route", [f"{API}/health", f"{API}/events", "/uploads/inexistant.png"])
def test_en_tetes_de_securite(client, route):
    r = client.get(route)
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("x-frame-options") == "DENY"
    assert "content-security-policy" in r.headers


def test_aucun_hash_de_mot_de_passe_dans_les_reponses(client, admin_headers, player_headers):
    reponses = [
        login(client, PLAYER_EMAIL, PLAYER_PASSWORD).text,
        client.get(f"{API}/profile/me", headers=player_headers).text,
        client.get(f"{API}/players", headers=admin_headers).text,
    ]
    for texte in reponses:
        assert "password_hash" not in texte
        assert "$2b$" not in texte


# Anomalie connue : une poule inexistante provoque une erreur 500 au lieu d'un 404
def test_pas_d_erreur_500_sur_une_poule_inexistante(client, data, admin_headers):
    r = client.post(f"{API}/teams", headers=admin_headers, json={
        "company": "Acme", "player1_id": data["p3"], "player2_id": data["p4"],
        "pool_id": 9999,
    })
    assert r.status_code == 404
    assert "Traceback" not in r.text
