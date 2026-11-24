"""SP64 / TSP64 : falsification et réutilisation de jetons JWT."""
import base64
import json

from jose import JWTError, jwt

from .outils import API, DEFAULT_SECRET_KEY, bearer, make_token

ROUTE_ADMIN = f"{API}/players"  # GET /players est réservé à l'administrateur


def _b64(obj):
    raw = json.dumps(obj, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def test_jeton_alg_none_refuse(client, data):
    """Jeton non signé (alg=none) avec un rôle administrateur."""
    header = _b64({"alg": "none", "typ": "JWT"})
    payload = _b64({"sub": str(data["admin"]), "role": "ADMINISTRATEUR", "exp": 9999999999})
    r = client.get(ROUTE_ADMIN, headers=bearer(f"{header}.{payload}."))
    assert r.status_code == 401


def test_jeton_signe_avec_une_autre_cle_refuse(client, data):
    token = make_token(data["admin"], "ADMINISTRATEUR", key="cle-de-l-attaquant")
    r = client.get(ROUTE_ADMIN, headers=bearer(token))
    assert r.status_code == 401


def test_jeton_malforme_refuse(client):
    r = client.get(ROUTE_ADMIN, headers=bearer("abc.def.ghi"))
    assert r.status_code == 401


def test_role_modifie_sans_resignature_refuse(client, data, player_headers):
    """On change le rôle dans le payload d'un vrai jeton joueur sans pouvoir le signer."""
    token = player_headers["Authorization"].split()[1]
    header, _payload, signature = token.split(".")
    faux = _b64({"sub": str(data["joueur"]), "role": "ADMINISTRATEUR", "exp": 9999999999})
    r = client.get(ROUTE_ADMIN, headers=bearer(f"{header}.{faux}.{signature}"))
    assert r.status_code == 401


# Anomalie connue : security.py désactive verify_exp, un jeton expiré est accepté
def test_jeton_expire_refuse(client, data):
    token = make_token(data["admin"], "ADMINISTRATEUR", minutes=-60)
    r = client.get(ROUTE_ADMIN, headers=bearer(token))
    assert r.status_code == 401


# Anomalie connue : avec la clé par défaut du dépôt, un jeton admin peut être fabriqué
def test_jeton_fabrique_avec_la_cle_par_defaut_refuse(client, data):
    token = make_token(data["admin"], "ADMINISTRATEUR", key=DEFAULT_SECRET_KEY)
    r = client.get(ROUTE_ADMIN, headers=bearer(token))
    assert r.status_code == 401


# Anomalie connue : la clé de signature figure dans une liste de mots courante
def test_cle_secrete_introuvable_par_dictionnaire(player_headers):
    """Équivalent Python d'une attaque hashcat : on essaie des clés connues."""
    token = player_headers["Authorization"].split()[1]
    dictionnaire = ["secret", "changeme", "password", "dev-secret",
                    "secret-key", DEFAULT_SECRET_KEY, "padel", "corpo-padel"]
    trouvee = None
    for cle in dictionnaire:
        try:
            jwt.decode(token, cle, algorithms=["HS256"], options={"verify_exp": False})
            trouvee = cle
            break
        except JWTError:
            continue
    assert trouvee is None, f"Clé retrouvée : {trouvee}"
