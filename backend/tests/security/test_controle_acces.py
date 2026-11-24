"""SP65 / TSP65 : contrôle d'accès (OWASP A01)."""
import pytest

from .outils import API, PLAYER_EMAIL


@pytest.mark.parametrize("methode, route", [
    ("get", "/players"),
    ("post", "/players"),
    ("post", "/teams"),
    ("post", "/pools"),
    ("post", "/events"),
    ("post", "/matches"),
])
def test_joueur_interdit_sur_les_routes_admin(client, player_headers, methode, route):
    r = client.request(methode.upper(), f"{API}{route}", headers=player_headers, json={})
    assert r.status_code == 403


# Anomalie connue : admin.py utilise get_current_user au lieu de require_admin
def test_joueur_ne_peut_pas_creer_de_compte(client, data, player_headers):
    r = client.post(f"{API}/admin/accounts/create", headers=player_headers,
                    json={"player_id": data["p3"], "role": "ADMINISTRATEUR"})
    assert r.status_code == 403


# Anomalie connue : un joueur réinitialise le mot de passe admin et le lit
def test_joueur_ne_peut_pas_reinitialiser_le_mot_de_passe_admin(client, data, player_headers):
    r = client.post(f"{API}/admin/accounts/{data['admin']}/reset-password",
                    headers=player_headers)
    assert r.status_code == 403
    assert "temporary_password" not in r.text


# Anomalie connue : GET /players/{id} est ouvert à tout utilisateur connecté
def test_joueur_ne_lit_pas_la_fiche_d_un_autre_joueur(client, data, player_headers):
    r = client.get(f"{API}/players/{data['p3']}", headers=player_headers)
    assert r.status_code == 403


def test_profil_ne_permet_pas_de_changer_son_role(client, player_headers):
    """Assignation de masse : les champs role et is_active doivent être ignorés."""
    r = client.put(f"{API}/profile/me", headers=player_headers, json={
        "first_name": "Alice", "last_name": "Martin", "email": PLAYER_EMAIL,
        "role": "ADMINISTRATEUR", "is_active": True,
    })
    assert r.status_code == 200
    me = client.get(f"{API}/profile/me", headers=player_headers).json()
    assert me["user"]["role"] == "JOUEUR"


def test_routes_protegees_sans_jeton(client):
    for route in ("/events", "/matches", "/results/rankings", "/profile/me"):
        assert client.get(f"{API}{route}").status_code == 401
