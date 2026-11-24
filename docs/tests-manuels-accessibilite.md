# Cahier de recette — Tests manuels d'accessibilité (TSP51 à TSP59)

> Source : onglet « Tests manuels » de `Matrice_tracabilite.xlsx`.
> ⚠️ Le cahier des charges (v1.0) ne contient **aucune exigence d'accessibilité** :
> ces tests sont hors spécification (référentiel retenu : **WCAG 2.1 niveau AA**).
> À signaler dans la revue des specs et dans le rapport.

## Conditions communes

| Élément | Valeur |
|---|---|
| Version testée | commit `a0d25ca` |
| Lancement | `python seed.py` puis backend (`uvicorn app.main:app --port 8000`) et frontend (`npm run dev`) |
| URL | http://localhost:5173 |
| Comptes (seed) | Admin : `admin@padel.com` / `Admin@2025!` — Joueur : `joueur@padel.com` / `Joueur@2025!` |
| Pages à couvrir | `/` (visiteur et connecté), `/login`, `/change-password`, `/planning`, `/matches`, `/results`, `/profile`, `/admin` (onglets Joueurs, Équipes, Poules, Comptes) |
| Testeur / date | Dario WEINBERGER / 2026-11-24 |
| Environnement | Firefox 160.0.1, Linux |

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
| TSP51-01 | Visiteur | 1. Ouvrir `/login`. 2. Avec la pipette de CCA, mesurer la couleur de la **bordure** du champ Email puis celle du fond de la page. | — | Ratio bordure / fond ≥ 3:1 | Bordure `rgb(209, 213, 219)` sur fond `rgb(255, 255, 255)` : **1,47:1** (WebAIM) | **KO** | ANO-001 |
| TSP51-02 | Admin connecté | Mesurer la bordure des champs des formulaires `/admin` (onglet Joueurs) et `/profile`. | — | ≥ 3:1 pour chaque champ | Tous les champs utilisent la classe `.input` : bordure `rgb(209, 213, 219)` sur fond `rgb(255, 255, 255)`, **1,47:1** (contour de la carte : `rgb(229, 231, 235)`, 1,24:1) | **KO** | ANO-001 (+ ANO-003 : champs `/admin` sans libellé) |
| TSP51-03 | Joueur connecté | Ouvrir `/planning`, mesurer la **pastille** qui marque un jour avec événement par rapport au fond de la case. | Un mois avec événements (seed) | ≥ 3:1 | Pastille `bg-orange-400` (`#fb923c`) sur fond blanc : **2,26:1** ; sur jour sélectionné (`#1e40af`) : 3,85:1. Pastille de 6 × 6 px | **KO** | ANO-004 |
| TSP51-04 | Joueur connecté | Sur `/planning`, mesurer l'indicateur du **jour sélectionné** et du jour courant. | — | ≥ 3:1 | Jour sélectionné `#1e40af` sur blanc : **8,72:1**. Remarque : le **jour courant n'est pas signalé** du tout (aucun style) | **OK** | — |
| TSP51-05 | Admin connecté | Sur `/admin` et `/results`, mesurer l'indicateur de l'**onglet actif** par rapport aux onglets inactifs et au fond. | — | ≥ 3:1 | `/admin` : soulignement de l'onglet actif `#1e40af` sur `#f9fafb` : **8,35:1** ; texte des onglets inactifs `#6b7280` : 4,63:1. `/results` n'a pas d'onglets (sans objet) | **OK** | — |
| TSP51-06 | Joueur connecté | Sur `/matches`, mesurer la bordure de la **case à cocher** « tous les matchs » (non cochée et cochée). | — | ≥ 3:1 dans les deux états | Case à cocher native (pas de style personnalisé) ; bordure Firefox par défaut ≈ `#8f8f9d` sur blanc : **3,19:1** (limite, dépend du navigateur). Visible seulement en rôle joueur | **OK** | — |
| TSP51-07 | Joueur connecté | Sur `/matches`, mesurer les **badges de statut** (A_VENIR, TERMINE, ANNULE) par rapport au fond. | — | ≥ 3:1 (et texte du badge ≥ 4,5:1) | Texte « Terminé » `#15803d` sur `#dcfce7` : **4,57:1** (limite) ; « À venir » `#1d4ed8` sur `#dbeafe` : **5,49:1**. Fond des badges / carte ≈ 1,1:1 mais l'information est portée par le texte (acceptable). ⚠️ Un match **ANNULE** est affiché « À venir » | **OK** (contraste) | ANO-005 (fonctionnel) |

*Anomalies suspectées : bordure des champs ≈ 1,5:1, pastille du calendrier ≈ 2,2:1.*

---

## TSP52 — Accessibilite_Agrandissement200 (ACC-04) · SP52 · WCAG 1.4.4 · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP52-01 | Fenêtre 1280 px de large, zoom 100 % | 1. Mettre le zoom du navigateur à **200 %** (`Ctrl` + `+`). 2. Parcourir chaque page de la liste. | — | Aucun texte coupé, superposé ou masqué ; toutes les fonctions restent accessibles (menu, boutons, formulaires) | Zoom 200 % sur `/`, `/login`, `/planning`, `/matches`, `/results`, `/profile`, `/admin` : aucun texte coupé ni superposé, menu et formulaires utilisables | **OK** | — |
| TSP52-02 | Zoom 100 % | 1. Paramètres du navigateur → Taille de police → **Très grande** (texte seul). 2. Parcourir chaque page. | — | Idem : le texte grossit sans casser la mise en page (pas de hauteurs fixes qui coupent le texte) | Firefox « Zoom texte seulement » à 200 % : toutes les pages OK, y compris les cases carrées de `/planning` et la liste à hauteur fixe de l'onglet Poules | **OK** | — |
| TSP52-03 | Zoom 200 %, joueur connecté | Sur `/planning`, ouvrir un jour avec événement. | — | Heure, pistes et équipes lisibles en entier | Détail du jour affiché en entier (texte à 200 %) | **OK** | — |
| TSP52-04 | Zoom 200 %, admin connecté | Sur `/matches`, créer un match puis saisir un score. | Données valides | Formulaires et boutons de validation atteignables et utilisables | Création d'un match et saisie du score `6-4, 6-3` réalisées sans gêne (texte à 200 %) | **OK** | — |

---

## TSP53 — Accessibilite_FocusVisible (ACC-06) · SP53 · WCAG 2.4.7 · Criticité : Critique (60)

Navigation **au clavier uniquement** (`Tab`, `Maj` + `Tab`, `Entrée`, `Espace`, flèches).

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP53-01 | Joueur connecté, page `/` | Appuyer sur `Tab` de façon répétée dans le **menu**. | — | Chaque lien du menu affiche un contour de focus visible, contrasté (≥ 3:1) | Contour de focus par défaut du navigateur visible sur chaque lien du menu | **OK** | — |
| TSP53-02 | Visiteur, `/login` | Tabuler sur les champs et le bouton « Se connecter ». | — | Focus visible sur chaque champ et sur le bouton | Champs : bordure bleue + liseré 1 px ; bouton « Se connecter » : contour visible | **OK** | — |
| TSP53-03 | Joueur connecté, `/planning` | Tabuler jusqu'aux boutons mois précédent / suivant, puis aux **jours du calendrier**. | — | Focus visible sur chaque bouton et chaque jour | Focus visible sur les flèches de navigation et sur chaque jour | **OK** | — |
| TSP53-04 | Admin connecté, `/admin` | Tabuler sur les **onglets** (Joueurs, Équipes, Poules, Comptes) et les boutons « Supprimer ». | — | Focus visible sur chaque onglet et chaque bouton, y compris les boutons d'apparence texte | Focus visible sur les 4 onglets et les boutons « Supprimer » | **OK** | — |
| TSP53-05 | Joueur connecté, `/matches` | Tabuler sur la case à cocher et le filtre de statut. | — | Focus visible | Focus visible sur le filtre de statut et les boutons d'action (testé en admin ; la case « tous les matchs », réservée au rôle joueur, utilise le style natif) | **OK** | — |
| TSP53-06 | Toutes pages | Vérifier qu'aucun élément focalisé n'est **masqué** (sous un en-tête fixe, hors écran). | — | L'élément focalisé reste visible à l'écran | Aucun en-tête fixe : l'élément focalisé n'est jamais masqué. Remarque : pas de lien d'évitement « Aller au contenu » (voir TSP49) | **OK** | — |

---

## TSP54 — Accessibilite_LoupeEcran (ACC-07) · SP54 · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP54-01 | Loupe à **300 %**, visiteur, `/login` | Saisir un mauvais mot de passe et valider. | `joueur@padel.com` / `faux` | Le message d'erreur apparaît **à côté du champ** concerné, visible sans déplacer la loupe loin du formulaire | *Non exécuté à la loupe — analyse du code :* message placé juste sous le champ Mot de passe, au-dessus du bouton (`LoginView.vue`). Même disposition sur `/profile` et `/change-password` | **OK** (analyse) | — |
| TSP54-02 | Loupe 300 %, admin, `/admin` onglet Joueurs | Créer un joueur avec une licence invalide. | Licence `L123` | Message « Format LXXXXXX attendu » affiché près du champ Licence | *Non exécuté à la loupe — analyse du code :* message unique affiché **en haut de la page**, sous les onglets (`AdminView.vue` l.143), loin du champ Licence et du bouton « Ajouter ». Même schéma sur `/matches` (message au-dessus du formulaire de création) | **KO** (analyse) | ANO-006 |
| TSP54-03 | Loupe 300 % en mode « suivre le focus » | Tabuler dans un formulaire. | — | La loupe suit le focus clavier | *Non exécuté.* Dépend surtout de l'outil de loupe ; le site utilise les éléments natifs (focus visible confirmé en TSP53), ce qui permet le suivi | **Non exécuté** | — |
| TSP54-04 | Loupe 300 %, joueur, `/matches` | Parcourir la liste des matchs. | — | Les informations d'un match (date, piste, équipes, statut) sont regroupées et lisibles sans aller-retour horizontal important | *Non exécuté à la loupe — analyse du code :* sur écran large, date / piste / équipes sont à gauche de la carte et le statut + score + actions **à l'extrême droite** (`justify-between`), soit jusqu'à ~1 100 px d'écart | **À confirmer** | — |

*Anomalie suspectée : messages d'erreur éloignés des champs.*

---

## TSP55 — Accessibilite_ContrasteEleve (ACC-08) · SP55 · Criticité : Grave (36)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP55-01 | Thème de contraste élevé activé (Windows) ou `forced-colors: active` émulé | Parcourir chaque page. | — | Boutons et champs gardent un contour visible | Firefox « Remplacer les couleurs de la page : Toujours » (blanc sur noir) : contours des boutons et des champs visibles | **OK** | — |
| TSP55-02 | Idem, joueur, `/planning` | Sélectionner un jour avec événement. | — | Le **jour sélectionné** et les **pastilles** d'événement restent visibles | Les **pastilles d'événement disparaissent** : impossible de savoir quels jours ont un événement | **KO** | ANO-007 |
| TSP55-03 | Idem, admin, `/admin` | Changer d'onglet. | — | L'onglet actif reste identifiable | **Aucun onglet n'est souligné**, y compris l'onglet actif : impossible de savoir lequel est sélectionné | **KO** | ANO-008 |
| TSP55-04 | Idem | Vérifier les icônes et badges de statut sur `/matches`. | — | Pas d'information disparue (pas d'icône invisible) | Les badges perdent leur fond mais le texte (« À venir », « Terminé ») reste lisible | **OK** | — |

*Anomalie suspectée : le jour sélectionné et les pastilles disparaissent.*

---

## TSP56 — Accessibilite_EspacementTexte (ACC-09) · SP56 · WCAG 1.4.12 · Criticité : Pas très grave (3)

Appliquer le bookmarklet *Text Spacing* (Steve Faulkner) ou le CSS suivant via DevTools :
`* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; } p { margin-bottom: 2em !important; }`

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP56-01 | Visiteur | Appliquer l'espacement sur `/` et `/login`. | — | Aucun texte tronqué, coupé ou superposé | *Non exécuté visuellement — analyse du code :* aucune hauteur ou largeur fixe sur du texte, aucun `truncate` / `overflow-hidden` / `whitespace-nowrap` : le texte peut s'étendre librement | **OK** (analyse) | — |
| TSP56-02 | Joueur connecté | Appliquer sur `/planning`, `/matches`, `/results`, `/profile`. | — | Idem (attention aux noms d'équipes et aux libellés de boutons) | *Non exécuté visuellement — analyse du code :* seules tailles fixes = pastille 6 × 6 px (sans texte) et cases carrées du calendrier (≈ 150 px, numéro de 2 chiffres) ; tableau du classement dans un conteneur à défilement horizontal (`overflow-x`) : pas de perte de contenu | **OK** (analyse) | — |
| TSP56-03 | Admin connecté | Appliquer sur `/admin` (4 onglets). | — | Idem, en-têtes de tableaux compris | *Non exécuté visuellement — analyse du code :* seule hauteur fixe = liste multiple des équipes (onglet Poules, `h-40`), qui défile : contenu accessible. Remarque : le menu (`flex` sans retour à la ligne) peut déborder sur écran étroit | **OK** (analyse) | — |

---

## TSP57 — Accessibilite_TailleCibles (ACC-10) · SP57 · WCAG 2.5.8 · Criticité : Pas très grave (6)

Mesure avec DevTools (survol de l'élément ou onglet *Computed* : largeur × hauteur).

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP57-01 | Joueur connecté | Mesurer les liens du **menu**. | — | Chaque cible ≥ 24 × 24 px (ou espacement suffisant autour) | *Analyse du code (`NavBar.vue`) :* liens `text-sm` + `px-3 py-1.5` → **32 px** de haut, > 60 px de large ; bouton Déconnexion `.btn` → 36 px | **OK** (analyse) | — |
| TSP57-02 | Joueur connecté | Mesurer les boutons mois précédent / suivant et les jours de `/planning`. | — | ≥ 24 × 24 px | *Analyse du code :* flèches `.btn` → **36 px** de haut ; jours carrés (`aspect-square`, 7 colonnes) → ≈ 40 px même à 320 px de large | **OK** (analyse) | — |
| TSP57-03 | Admin connecté | Mesurer les boutons texte « Supprimer », « Annuler », « Modifier » de `/matches` et `/admin`. | — | ≥ 24 × 24 px | *Analyse du code :* boutons texte sans marge interne → **20 px** de haut (< 24 px), mais espacés de 12 px (`gap-3`) et seuls sur leur ligne de tableau : conformes via l'**exception d'espacement** de WCAG 2.5.8. Zone de clic petite, amélioration recommandée | **OK** (analyse, limite) | — |
| TSP57-04 | Joueur connecté | Mesurer la case à cocher de `/matches`. | — | ≥ 24 × 24 px (zone cliquable label compris) | *Analyse du code :* case native (≈ 13 px) **englobée dans son `<label>`** : toute la ligne de texte est cliquable (≈ 20 px de haut, > 150 px de large), isolée → exception d'espacement | **OK** (analyse, limite) | — |

---

## TSP58 — Accessibilite_Daltonisme (ACC-11) · SP58 · WCAG 1.4.1 · Criticité : Grave (30)

DevTools → *Rendering* → *Emulate vision deficiencies* : faire chaque cas en **deutéranopie**,
**protanopie** et **achromatopsie**.

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP58-01 | Joueur connecté, `/planning` | Repérer les jours avec événement et le jour sélectionné. | — | Repérables autrement que par la couleur (icône, texte, forme, soulignement) | *Non exécuté en émulation — analyse du code :* un jour avec événement est signalé par la **présence d'une pastille** (forme), pas par une teinte ; jour sélectionné = fond plein foncé (8,72:1, visible en niveaux de gris). En achromatopsie la pastille reste visible mais très peu contrastée (voir ANO-004) | **OK** (analyse) | — |
| TSP58-02 | Joueur connecté, `/matches` | Distinguer les statuts A_VENIR / TERMINE / ANNULE. | — | Statut lisible en texte, pas seulement par la couleur du badge | *Non exécuté en émulation — analyse du code :* badges avec texte « À venir » / « Terminé ». Le statut ANNULE n'est pas affiché du tout (ANO-005, défaut fonctionnel, pas de couleur) | **OK** (analyse) | — |
| TSP58-03 | Joueur connecté, `/results` | Distinguer victoires et défaites. | — | Indiqué en texte (« Victoire » / « Défaite », V/D), pas uniquement vert/rouge | *Non exécuté en émulation — analyse du code :* badge texte « VICTOIRE » / « DEFAITE » ; statistiques avec libellés « Victoires » / « Défaites » sous les chiffres verts / rouges ; colonnes « V » / « D » dans le classement | **OK** (analyse) | — |
| TSP58-04 | Admin, `/admin` | Soumettre un formulaire avec une erreur. | Licence `L123` | Le champ en erreur est signalé par un message, pas seulement par une bordure rouge | *Non exécuté en émulation — analyse du code :* l'erreur est signalée par un **message texte** (aucune bordure rouge). Le message est cependant éloigné du champ (ANO-006) | **OK** (analyse) | — |
| TSP58-05 | Visiteur, `/login` | Distinguer un lien d'un texte normal. | — | Les liens sont soulignés ou identifiables sans la couleur | *Non exécuté en émulation — analyse du code :* aucun lien dans un bloc de texte sur `/login`. Seul lien « texte » du site : « Changer mon mot de passe » (`/profile`), isolé sur sa ligne, souligné au survol uniquement — critère 1.4.1 non applicable aux liens isolés | **OK** (analyse) | — |

*Anomalie suspectée : jours avec événement signalés uniquement par la couleur.*

---

## TSP59 — Accessibilite_ParcoursLecteurEcran (ACC-17) · SP59 · Criticité : Critique (60)

À réaliser **écran éteint ou sans regarder l'écran**, avec NVDA + Firefox, puis Narrateur + Edge
(ou Orca + Firefox sous Linux). Noter pour chaque étape ce qui est **annoncé**.

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP59-01 | Visiteur, `/` | 1. Écouter la page. 2. Atteindre « Se connecter » au clavier. 3. Se connecter. | Joueur (seed) | Titre de page annoncé, bouton annoncé « Se connecter, bouton », connexion réussie et nouvelle page annoncée | *Non exécuté au lecteur d'écran — analyse du code :* `lang="fr"` présent, boutons natifs (annoncés correctement). Mais le titre de l'onglet est **toujours « Corpo Padel »** et aucun changement de page n'est annoncé (navigation SPA sans mise à jour du titre ni du focus) | **KO** (analyse) | ANO-009 |
| TSP59-02 | Visiteur, `/login` | Se connecter avec un mauvais mot de passe. | `faux` | Le message d'erreur et les tentatives restantes sont **lus automatiquement** | *Non exécuté au lecteur d'écran — analyse du code :* **aucun attribut ARIA** dans tout le frontend (`role="alert"`, `aria-live` absents) : le message apparaît sans être annoncé | **KO** (analyse) | ANO-010 |
| TSP59-03 | Joueur connecté | Ouvrir `/planning`, naviguer vers le mois suivant, ouvrir un jour avec événement. | — | Chaque jour annonce sa date complète et ses événements ; le détail (heure, pistes, équipes) est lu | *Non exécuté au lecteur d'écran — analyse du code :* chaque jour est un `<button>` dont le seul contenu est le **numéro** (« 15 ») ; la pastille d'événement est un `<span>` vide sans texte : ni le mois ni la présence d'événements ne sont annoncés | **KO** (analyse) | ANO-011 |
| TSP59-04 | Joueur connecté | Ouvrir `/matches`, activer « tous les matchs », filtrer par statut. | — | Case à cocher et filtre annoncés avec leur état ; la liste est lisible (tableau ou liste structurée) | *Non exécuté au lecteur d'écran — analyse du code :* case à cocher englobée dans son `<label>` (annoncée correctement) ; le **filtre de statut n'a aucun nom** (ANO-003) ; liste = suite de `<div>` sans structure de liste | **KO** (analyse) | ANO-003 |
| TSP59-05 | Joueur connecté | Ouvrir `/results`, lire statistiques, résultats et classement. | — | Onglets annoncés comme onglets, tableaux lus avec leurs en-têtes | *Non exécuté au lecteur d'écran — analyse du code :* `/results` n'a pas d'onglets (sans objet) ; tableau du classement avec `<thead>` / `<th>` (en-têtes lus) ; statistiques avec libellés texte | **OK** (analyse) | — |
| TSP59-06 | Joueur connecté | Ouvrir `/profile`, modifier le prénom, enregistrer. | Prénom `Jean-Marc` | Champs annoncés avec leur libellé ; « Profil mis à jour. » est lu | *Non exécuté au lecteur d'écran — analyse du code :* libellés non reliés aux champs (ANO-002) et message de succès non annoncé (ANO-010) | **KO** (analyse) | ANO-002, ANO-010 |
| TSP59-07 | Admin connecté | Sur `/matches`, créer un match. | Données valides | Tous les champs ont un libellé annoncé ; succès annoncé | *Non exécuté au lecteur d'écran — analyse du code :* 5 libellés non reliés (ANO-002) ; aucune annonce du match créé | **KO** (analyse) | ANO-002, ANO-010 |
| TSP59-08 | Admin connecté | Saisir un score invalide puis un score valide. | `9-9` puis `6-4, 6-3` | L'erreur « Format de score invalide (ex : 6-4, 6-3) » est lue ; le passage en TERMINE est annoncé | *Non exécuté au lecteur d'écran — analyse du code :* la saisie passe par `window.prompt` (boîte native, lue correctement) ; le message d'erreur et le changement de statut s'affichent sans être annoncés (ANO-010) | **KO** (analyse) | ANO-010 |

---

## Synthèse d'exécution

**Méthode** : *exécuté* = test réalisé dans le navigateur par le testeur ; *analyse* = résultat
déduit du code source (couleurs Tailwind, structure HTML, attributs), le test n'ayant pas été
exécuté avec l'outil prévu. Les résultats « (analyse) » sont à confirmer par une exécution réelle.

| Test | Nb de cas | OK | KO | Autre | Méthode | Fiches ANO |
|---|---|---|---|---|---|---|
| TSP51 Contraste des éléments | 7 | 4 | 3 | — | 01-02 exécutés, 03-07 analyse | ANO-001, ANO-003, ANO-004, ANO-005 |
| TSP52 Agrandissement 200 % | 4 | 4 | 0 | — | exécuté | — |
| TSP53 Focus visible | 6 | 6 | 0 | — | exécuté | — |
| TSP54 Loupe d'écran | 4 | 1 | 1 | 1 non exécuté, 1 à confirmer | analyse | ANO-006 |
| TSP55 Contraste élevé | 4 | 2 | 2 | — | exécuté | ANO-007, ANO-008 |
| TSP56 Espacement du texte | 3 | 3 | 0 | — | analyse | — |
| TSP57 Taille des cibles | 4 | 4 | 0 | — | analyse | — |
| TSP58 Daltonisme | 5 | 5 | 0 | — | analyse | — |
| TSP59 Parcours lecteur d'écran | 8 | 1 | 7 | — | analyse | ANO-002, ANO-003, ANO-009, ANO-010, ANO-011 |
| **Total** | **45** | **30** | **13** | **2** | 16 exécutés · 29 analyse ou non exécutés | **11 fiches** |

### Fiches d'anomalies ouvertes

| ID | Titre | Type | Sévérité | Méthode |
|---|---|---|---|---|
| [ANO-001](anomalies/ANO-001.md) | Bordure des champs de saisie insuffisamment contrastée (1,47:1) | IHM | Majeur | exécuté |
| [ANO-002](anomalies/ANO-002.md) | Libellés visibles non reliés aux champs (15 champs) | IHM | Majeur | exécuté + analyse |
| [ANO-003](anomalies/ANO-003.md) | Champs des formulaires d'administration sans aucun libellé | IHM | Majeur | analyse |
| [ANO-004](anomalies/ANO-004.md) | Pastille « jour avec événement » insuffisamment contrastée (2,26:1) | IHM | Majeur | analyse |
| [ANO-005](anomalies/ANO-005.md) | Un match annulé est affiché « À venir » | Fonctionnel | Majeur | analyse |
| [ANO-006](anomalies/ANO-006.md) | Messages d'erreur admin affichés loin des champs | IHM | Mineur | analyse |
| [ANO-007](anomalies/ANO-007.md) | Jours avec événement invisibles en contraste élevé | IHM | Majeur | exécuté |
| [ANO-008](anomalies/ANO-008.md) | Onglet actif non identifiable en contraste élevé | IHM | Mineur | exécuté |
| [ANO-009](anomalies/ANO-009.md) | Titre de page identique partout, changement de page non annoncé | IHM | Mineur | analyse |
| [ANO-010](anomalies/ANO-010.md) | Messages d'erreur et de succès non annoncés (aucun ARIA) | IHM | Majeur | analyse |
| [ANO-011](anomalies/ANO-011.md) | Jours du calendrier sans date complète ni événements annoncés | IHM | Majeur | analyse |
