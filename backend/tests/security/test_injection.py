"""SP67 / TSP67 : injection SQL et XSS (OWASP A03)."""
import pytest

from .outils import API, login

CHARGES_SQL = [
    "' OR '1'='1",
    "admin@test.fr' --",
    "\" OR 1=1 --",
    "'; DROP TABLE users; --",
]

XSS = "<img src=x onerror=alert(1)>"


@pytest.mark.parametrize("charge", CHARGES_SQL)
def test_injection_sql_dans_le_login(client, charge):
    r = login(client, charge, charge)
    assert r.status_code in (400, 401, 422)


@pytest.mark.parametrize("param", ["month", "status", "team_id", "start_date"])
@pytest.mark.parametrize("charge", CHARGES_SQL)
def test_injection_sql_dans_les_parametres(client, player_headers, param, charge):
    route = "/events" if param in ("month", "start_date") else "/matches"
    r = client.get(f"{API}{route}", params={param: charge}, headers=player_headers)
    assert r.status_code != 500
    # La table users existe toujours après la charge DROP TABLE.
    assert client.get(f"{API}/profile/me", headers=player_headers).status_code == 200


# Anomalie connue : teams.py ne nettoie pas le nom d'entreprise, affiché ensuite en v-html
def test_xss_dans_le_nom_d_equipe(client, data, admin_headers):
    r = client.post(f"{API}/teams", headers=admin_headers, json={
        "company": f"Acme{XSS}", "player1_id": data["p3"], "player2_id": data["p4"],
    })
    assert r.status_code in (201, 400, 422)
    equipes = client.get(f"{API}/teams", headers=admin_headers).text
    assert "onerror" not in equipes


def test_xss_dans_le_nom_d_un_joueur_refuse(client, admin_headers):
    r = client.post(f"{API}/players", headers=admin_headers, json={
        "first_name": XSS, "last_name": "Test", "company": "Acme",
        "license_number": "L999999", "email": "xss@test.fr",
    })
    assert r.status_code in (400, 422)


def test_xss_dans_le_nom_de_poule_nettoye(client, admin_headers):
    r = client.post(f"{API}/pools", headers=admin_headers,
                    json={"name": f"Poule{XSS}", "team_ids": [1, 2, 3, 4, 5, 6]})
    assert "onerror" not in r.text
