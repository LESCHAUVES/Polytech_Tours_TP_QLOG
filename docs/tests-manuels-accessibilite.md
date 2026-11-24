# Cahier de recette — Tests manuels d'accessibilité (TSP51 à TSP59)

> Source : onglet « Tests manuels » de `Matrice_tracabilite.xlsx`.
> ⚠️ Le cahier des charges (v1.0) ne contient **aucune exigence d'accessibilité** :
> ces tests sont hors spécification (référentiel retenu : **WCAG 2.1 niveau AA**).
> À signaler dans la revue des specs et dans le rapport.

## Conditions communes

| Élément | Valeur |
|---|---|
| Version testée | commit `_______` (renseigner `git rev-parse --short HEAD`) |
| Lancement | `python seed.py` puis backend (`uvicorn app.main:app --port 8000`) et frontend (`npm run dev`) |
| URL | http://localhost:5173 |
| Comptes (seed) | Admin : `admin@padel.com` / `Admin@2025!` — Joueur : `joueur@padel.com` / `Joueur@2025!` |
| Pages à couvrir | `/` (visiteur et connecté), `/login`, `/change-password`, `/planning`, `/matches`, `/results`, `/profile`, `/admin` (onglets Joueurs, Équipes, Poules, Comptes) |
| Testeur / date | `_______` / `_______` |

**Règle :** un cas est **OK** si le résultat attendu est obtenu sur **toutes** les pages listées
dans le cas. Sinon **KO** : noter la page et l'élément fautif, faire une capture d'écran et
ouvrir une fiche `docs/anomalies/ANO-xxx.md` (une fiche par problème).

**Outils** (gratuits) :

| Besoin | Windows | Linux / macOS |
|---|---|---|
| Mesure de contraste | Colour Contrast Analyser (TPGi) | CCA (macOS) · pipette de contraste de Chrome DevTools · WebAIM Contrast Checker |
| Lecteur d'écran | NVDA + Firefox, Narrateur + Edge | Orca + Firefox (Linux) · VoiceOver + Safari (macOS) |
| Loupe | Loupe Windows (`Win` + `+`) | Zoom GNOME (Accessibilité) · Zoom macOS |
| Contraste élevé | Paramètres → Accessibilité → Thèmes de contraste | Thème « Contraste élevé » GNOME · Chrome : `forced-colors` émulé dans DevTools (Rendering) |
| Daltonisme | Chrome DevTools → Rendering → *Emulate vision deficiencies* | idem |

---

## TSP51 — Accessibilite_ContrasteElements (ACC-03) · SP51 · WCAG 1.4.11 · Criticité : Critique (60)

Ratio de contraste attendu **≥ 3:1** entre l'élément graphique et le fond adjacent.

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP51-01 | Visiteur | 1. Ouvrir `/login`. 2. Avec la pipette de CCA, mesurer la couleur de la **bordure** du champ Email puis celle du fond de la page. | — | Ratio bordure / fond ≥ 3:1 | | | |
| TSP51-02 | Admin connecté | Mesurer la bordure des champs des formulaires `/admin` (onglet Joueurs) et `/profile`. | — | ≥ 3:1 pour chaque champ | | | |
| TSP51-03 | Joueur connecté | Ouvrir `/planning`, mesurer la **pastille** qui marque un jour avec événement par rapport au fond de la case. | Un mois avec événements (seed) | ≥ 3:1 | | | |
| TSP51-04 | Joueur connecté | Sur `/planning`, mesurer l'indicateur du **jour sélectionné** et du jour courant. | — | ≥ 3:1 | | | |
| TSP51-05 | Admin connecté | Sur `/admin` et `/results`, mesurer l'indicateur de l'**onglet actif** par rapport aux onglets inactifs et au fond. | — | ≥ 3:1 | | | |
| TSP51-06 | Joueur connecté | Sur `/matches`, mesurer la bordure de la **case à cocher** « tous les matchs » (non cochée et cochée). | — | ≥ 3:1 dans les deux états | | | |
| TSP51-07 | Joueur connecté | Sur `/matches`, mesurer les **badges de statut** (A_VENIR, TERMINE, ANNULE) par rapport au fond. | — | ≥ 3:1 (et texte du badge ≥ 4,5:1) | | | |

*Anomalies suspectées : bordure des champs ≈ 1,5:1, pastille du calendrier ≈ 2,2:1.*

---

## TSP52 — Accessibilite_Agrandissement200 (ACC-04) · SP52 · WCAG 1.4.4 · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP52-01 | Fenêtre 1280 px de large, zoom 100 % | 1. Mettre le zoom du navigateur à **200 %** (`Ctrl` + `+`). 2. Parcourir chaque page de la liste. | — | Aucun texte coupé, superposé ou masqué ; toutes les fonctions restent accessibles (menu, boutons, formulaires) | | | |
| TSP52-02 | Zoom 100 % | 1. Paramètres du navigateur → Taille de police → **Très grande** (texte seul). 2. Parcourir chaque page. | — | Idem : le texte grossit sans casser la mise en page (pas de hauteurs fixes qui coupent le texte) | | | |
| TSP52-03 | Zoom 200 %, joueur connecté | Sur `/planning`, ouvrir un jour avec événement. | — | Heure, pistes et équipes lisibles en entier | | | |
| TSP52-04 | Zoom 200 %, admin connecté | Sur `/matches`, créer un match puis saisir un score. | Données valides | Formulaires et boutons de validation atteignables et utilisables | | | |

---

## TSP53 — Accessibilite_FocusVisible (ACC-06) · SP53 · WCAG 2.4.7 · Criticité : Critique (60)

Navigation **au clavier uniquement** (`Tab`, `Maj` + `Tab`, `Entrée`, `Espace`, flèches).

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP53-01 | Joueur connecté, page `/` | Appuyer sur `Tab` de façon répétée dans le **menu**. | — | Chaque lien du menu affiche un contour de focus visible, contrasté (≥ 3:1) | | | |
| TSP53-02 | Visiteur, `/login` | Tabuler sur les champs et le bouton « Se connecter ». | — | Focus visible sur chaque champ et sur le bouton | | | |
| TSP53-03 | Joueur connecté, `/planning` | Tabuler jusqu'aux boutons mois précédent / suivant, puis aux **jours du calendrier**. | — | Focus visible sur chaque bouton et chaque jour | | | |
| TSP53-04 | Admin connecté, `/admin` | Tabuler sur les **onglets** (Joueurs, Équipes, Poules, Comptes) et les boutons « Supprimer ». | — | Focus visible sur chaque onglet et chaque bouton, y compris les boutons d'apparence texte | | | |
| TSP53-05 | Joueur connecté, `/matches` | Tabuler sur la case à cocher et le filtre de statut. | — | Focus visible | | | |
| TSP53-06 | Toutes pages | Vérifier qu'aucun élément focalisé n'est **masqué** (sous un en-tête fixe, hors écran). | — | L'élément focalisé reste visible à l'écran | | | |

---

## TSP54 — Accessibilite_LoupeEcran (ACC-07) · SP54 · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP54-01 | Loupe à **300 %**, visiteur, `/login` | Saisir un mauvais mot de passe et valider. | `joueur@padel.com` / `faux` | Le message d'erreur apparaît **à côté du champ** concerné, visible sans déplacer la loupe loin du formulaire | | | |
| TSP54-02 | Loupe 300 %, admin, `/admin` onglet Joueurs | Créer un joueur avec une licence invalide. | Licence `L123` | Message « Format LXXXXXX attendu » affiché près du champ Licence | | | |
| TSP54-03 | Loupe 300 % en mode « suivre le focus » | Tabuler dans un formulaire. | — | La loupe suit le focus clavier | | | |
| TSP54-04 | Loupe 300 %, joueur, `/matches` | Parcourir la liste des matchs. | — | Les informations d'un match (date, piste, équipes, statut) sont regroupées et lisibles sans aller-retour horizontal important | | | |

*Anomalie suspectée : messages d'erreur éloignés des champs.*

---

## TSP55 — Accessibilite_ContrasteEleve (ACC-08) · SP55 · Criticité : Grave (36)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP55-01 | Thème de contraste élevé activé (Windows) ou `forced-colors: active` émulé | Parcourir chaque page. | — | Boutons et champs gardent un contour visible | | | |
| TSP55-02 | Idem, joueur, `/planning` | Sélectionner un jour avec événement. | — | Le **jour sélectionné** et les **pastilles** d'événement restent visibles | | | |
| TSP55-03 | Idem, admin, `/admin` | Changer d'onglet. | — | L'onglet actif reste identifiable | | | |
| TSP55-04 | Idem | Vérifier les icônes et badges de statut sur `/matches`. | — | Pas d'information disparue (pas d'icône invisible) | | | |

*Anomalie suspectée : le jour sélectionné et les pastilles disparaissent.*

---

## TSP56 — Accessibilite_EspacementTexte (ACC-09) · SP56 · WCAG 1.4.12 · Criticité : Pas très grave (3)

Appliquer le bookmarklet *Text Spacing* (Steve Faulkner) ou le CSS suivant via DevTools :
`* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; } p { margin-bottom: 2em !important; }`

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP56-01 | Visiteur | Appliquer l'espacement sur `/` et `/login`. | — | Aucun texte tronqué, coupé ou superposé | | | |
| TSP56-02 | Joueur connecté | Appliquer sur `/planning`, `/matches`, `/results`, `/profile`. | — | Idem (attention aux noms d'équipes et aux libellés de boutons) | | | |
| TSP56-03 | Admin connecté | Appliquer sur `/admin` (4 onglets). | — | Idem, en-têtes de tableaux compris | | | |

---

## TSP57 — Accessibilite_TailleCibles (ACC-10) · SP57 · WCAG 2.5.8 · Criticité : Pas très grave (6)

Mesure avec DevTools (survol de l'élément ou onglet *Computed* : largeur × hauteur).

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP57-01 | Joueur connecté | Mesurer les liens du **menu**. | — | Chaque cible ≥ 24 × 24 px (ou espacement suffisant autour) | | | |
| TSP57-02 | Joueur connecté | Mesurer les boutons mois précédent / suivant et les jours de `/planning`. | — | ≥ 24 × 24 px | | | |
| TSP57-03 | Admin connecté | Mesurer les boutons texte « Supprimer », « Annuler », « Modifier » de `/matches` et `/admin`. | — | ≥ 24 × 24 px | | | |
| TSP57-04 | Joueur connecté | Mesurer la case à cocher de `/matches`. | — | ≥ 24 × 24 px (zone cliquable label compris) | | | |

---

## TSP58 — Accessibilite_Daltonisme (ACC-11) · SP58 · WCAG 1.4.1 · Criticité : Grave (30)

DevTools → *Rendering* → *Emulate vision deficiencies* : faire chaque cas en **deutéranopie**,
**protanopie** et **achromatopsie**.

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP58-01 | Joueur connecté, `/planning` | Repérer les jours avec événement et le jour sélectionné. | — | Repérables autrement que par la couleur (icône, texte, forme, soulignement) | | | |
| TSP58-02 | Joueur connecté, `/matches` | Distinguer les statuts A_VENIR / TERMINE / ANNULE. | — | Statut lisible en texte, pas seulement par la couleur du badge | | | |
| TSP58-03 | Joueur connecté, `/results` | Distinguer victoires et défaites. | — | Indiqué en texte (« Victoire » / « Défaite », V/D), pas uniquement vert/rouge | | | |
| TSP58-04 | Admin, `/admin` | Soumettre un formulaire avec une erreur. | Licence `L123` | Le champ en erreur est signalé par un message, pas seulement par une bordure rouge | | | |
| TSP58-05 | Visiteur, `/login` | Distinguer un lien d'un texte normal. | — | Les liens sont soulignés ou identifiables sans la couleur | | | |

*Anomalie suspectée : jours avec événement signalés uniquement par la couleur.*

---

## TSP59 — Accessibilite_ParcoursLecteurEcran (ACC-17) · SP59 · Criticité : Critique (60)

À réaliser **écran éteint ou sans regarder l'écran**, avec NVDA + Firefox, puis Narrateur + Edge
(ou Orca + Firefox sous Linux). Noter pour chaque étape ce qui est **annoncé**.

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP59-01 | Visiteur, `/` | 1. Écouter la page. 2. Atteindre « Se connecter » au clavier. 3. Se connecter. | Joueur (seed) | Titre de page annoncé, bouton annoncé « Se connecter, bouton », connexion réussie et nouvelle page annoncée | | | |
| TSP59-02 | Visiteur, `/login` | Se connecter avec un mauvais mot de passe. | `faux` | Le message d'erreur et les tentatives restantes sont **lus automatiquement** | | | |
| TSP59-03 | Joueur connecté | Ouvrir `/planning`, naviguer vers le mois suivant, ouvrir un jour avec événement. | — | Chaque jour annonce sa date complète et ses événements ; le détail (heure, pistes, équipes) est lu | | | |
| TSP59-04 | Joueur connecté | Ouvrir `/matches`, activer « tous les matchs », filtrer par statut. | — | Case à cocher et filtre annoncés avec leur état ; la liste est lisible (tableau ou liste structurée) | | | |
| TSP59-05 | Joueur connecté | Ouvrir `/results`, lire statistiques, résultats et classement. | — | Onglets annoncés comme onglets, tableaux lus avec leurs en-têtes | | | |
| TSP59-06 | Joueur connecté | Ouvrir `/profile`, modifier le prénom, enregistrer. | Prénom `Jean-Marc` | Champs annoncés avec leur libellé ; « Profil mis à jour. » est lu | | | |
| TSP59-07 | Admin connecté | Sur `/matches`, créer un match. | Données valides | Tous les champs ont un libellé annoncé ; succès annoncé | | | |
| TSP59-08 | Admin connecté | Saisir un score invalide puis un score valide. | `9-9` puis `6-4, 6-3` | L'erreur « Format de score invalide (ex : 6-4, 6-3) » est lue ; le passage en TERMINE est annoncé | | | |

---

## Synthèse d'exécution

| Test | Nb de cas | OK | KO | Fiches ANO |
|---|---|---|---|---|
| TSP51 | 7 | | | |
| TSP52 | 4 | | | |
| TSP53 | 6 | | | |
| TSP54 | 4 | | | |
| TSP55 | 4 | | | |
| TSP56 | 3 | | | |
| TSP57 | 4 | | | |
| TSP58 | 5 | | | |
| TSP59 | 8 | | | |
| **Total** | **45** | | | |
