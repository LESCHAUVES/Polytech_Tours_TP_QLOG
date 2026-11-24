"""SP66 et SP71 / TSP66 et TSP71 : force brute et énumération de comptes."""

from .outils import ADMIN_EMAIL, ADMIN_PASSWORD, PLAYER_EMAIL, login


# Anomalie connue : auth.py utilise > au lieu de >=, le blocage n'arrive qu'au 6e échec
def test_compte_bloque_au_cinquieme_echec(client):
    codes = [login(client, PLAYER_EMAIL, "mauvais").status_code for _ in range(5)]
    assert codes[:4] == [401, 401, 401, 401]
    assert codes[4] == 403


def test_compte_bloque_refuse_meme_le_bon_mot_de_passe(client):
    for _ in range(6):
        login(client, PLAYER_EMAIL, "mauvais")
    r = login(client, PLAYER_EMAIL, "Joueur@2025!x")
    assert r.status_code == 403


# Anomalie connue : le message diffère entre un email inconnu et un mauvais mot de passe
def test_meme_reponse_email_inconnu_et_mauvais_mot_de_passe(client):
    inconnu = login(client, "personne@test.fr", "mauvais").json()
    mauvais = login(client, PLAYER_EMAIL, "mauvais").json()
    assert inconnu == mauvais


def test_admin_peut_se_connecter_avec_le_bon_mot_de_passe(client):
    assert login(client, ADMIN_EMAIL, ADMIN_PASSWORD).status_code == 200
