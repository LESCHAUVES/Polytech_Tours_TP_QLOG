"""SP68 / TSP68 : envoi de fichiers malveillants."""
import os

import pytest

from app.config import settings

from .outils import API

PNG_MINIMAL = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
               b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx\x9cc\xf8\x0f"
               b"\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82")


def envoyer(client, headers, nom, contenu, type_mime="image/png"):
    return client.post(f"{API}/profile/me/photo", headers=headers,
                       files={"file": (nom, contenu, type_mime)})


def test_vraie_image_acceptee(client, player_headers):
    assert envoyer(client, player_headers, "photo.png", PNG_MINIMAL).status_code == 200


# Anomalie connue : seule l'extension est vérifiée, pas le contenu du fichier
@pytest.mark.parametrize("contenu", [
    b"<html><script>alert(1)</script></html>",
    b"<svg xmlns='http://www.w3.org/2000/svg' onload='alert(1)'/>",
])
def test_script_deguise_en_png_refuse(client, player_headers, contenu):
    assert envoyer(client, player_headers, "photo.png", contenu).status_code == 400


def test_extension_non_autorisee_refusee(client, player_headers):
    r = envoyer(client, player_headers, "page.html", b"<html></html>", "text/html")
    assert r.status_code == 400


def test_fichier_trop_gros_refuse(client, player_headers):
    contenu = PNG_MINIMAL + b"\x00" * (settings.max_upload_size + 1)
    assert envoyer(client, player_headers, "grosse.png", contenu).status_code == 400


def test_nom_de_fichier_avec_parcours_de_dossier(client, player_headers):
    r = envoyer(client, player_headers, "../../evil.png", PNG_MINIMAL)
    assert r.status_code == 200
    url = r.json()["photo_url"]
    assert ".." not in url
    nom = url.rsplit("/", 1)[-1]
    assert os.path.exists(os.path.join(settings.upload_dir, nom))
