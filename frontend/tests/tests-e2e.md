# Cahier de recette — Tests manuels E2E & accessibilité (TSP25 à TSP50)

> Source : onglet « Tests manuels » de `Matrice_tracabilite.xlsx`.
> ⚠️ Les tests d'accessibilité (**TSP41 à TSP50**, référentiel **WCAG 2.1 niveau AA**) sont à exécuter manuellement dans le navigateur / DevTools (les références Cypress / `cypress-axe` / `cypress-real-events` de la matrice sont adaptées en vérification manuelle / inspection DOM). Les points « À vérifier » de la matrice signalent des anomalies ou comportements critiques à contrôler.

## Conditions communes

| Élément | Valeur |
|---|---|
| Version testée | commit `a0d25ca` |
| Lancement | `python seed.py` puis backend (`uvicorn app.main:app --port 8000`) et frontend (`npm run dev`) |
| URL | http://localhost:5173 |
| Comptes (seed) | Admin : `admin@padel.com` / `Admin@2025!` — Joueur : `joueur@padel.com` / `Joueur@2025!` |
| Pages à couvrir | `/` (visiteur et connecté), `/login`, `/change-password`, `/planning`, `/matches`, `/results`, `/profile`, `/admin` (onglets Joueurs, Équipes, Poules, Comptes) |
| Testeur / date | — / 2026-11-25 |
| Environnement | Navigateur web (Firefox / Chrome DevTools), Linux / Windows |

**Règle :** un cas est **OK** si le résultat attendu est obtenu sur **toutes** les pages / scénarios listés dans le cas. Sinon **KO** : noter la page et l'élément fautif, faire une capture d'écran et ouvrir une fiche `docs/anomalies/ANO-xxx.md` (une fiche par problème).

---

## TSP25 — Acces_Visiteur (E2E-01) · SP25 · Périmètre : Tout le site · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP25-01 | Visiteur non connecté | 1. Ouvrir `/`. 2. Vérifier l'affichage et le bouton « Se connecter ». | — | Page d'accueil affichée avec le bouton « Se connecter » | | | |
| TSP25-02 | Visiteur non connecté | Tenter d'accéder directement à `/planning`, `/matches` et `/results`. | — | Redirection vers `/login` pour chacune de ces pages protégées | | | |

---

## TSP26 — Connexion (E2E-02) · SP26 · Périmètre : Page /login · Criticité : Critique (100)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP26-01 | Visiteur, `/login` | Saisir des identifiants valides et valider. | Compte seed valide | Accueil personnalisé affiché | | | |
| TSP26-02 | Visiteur, `/login` | Saisir un mauvais mot de passe et valider. | Mauvais mot de passe | Message d'erreur et « Tentatives restantes : 4 » | | | |
| TSP26-03 | Visiteur, `/login` | Enchaîner 5 échecs de connexion de suite et observer l'écran. | 5 mauvais mots de passe | Message « Compte bloqué » ; vérifier si l'écran affiche une tentative de trop | | | |

---

## TSP27 — PremierLogin_ChangementMdp (E2E-03) · SP27 · Périmètre : Pages /login et /change-password · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP27-01 | Compte avec mot de passe temporaire | Se connecter sur `/login` avec le mot de passe temporaire. | Identifiants + mdp temporaire | Redirection vers `/change-password` | | | |
| TSP27-02 | Sur `/change-password` | Soumettre un changement de mot de passe invalide (erreurs), puis un changement valide. | Mdp invalide puis mdp valide | Erreurs affichées lors des saisies invalides, puis retour sur `/profile` après validation | | | |

---

## TSP28 — Deconnexion_SessionInvalide (E2E-04) · SP28 · Périmètre : Tout le site · Criticité : Grave (36)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP28-01 | Utilisateur connecté | Cliquer sur Déconnexion puis tenter d'accéder à `/matches` (et autres pages protégées). | — | Retour sur `/login`, pages protégées inaccessibles | | | |
| TSP28-02 | Session active | Placer un token invalide dans le navigateur et recharger/naviguer. | Token invalide | Redirection vers `/login` | | | |
| TSP28-03 | Session active | Placer un token expiré dans le navigateur et vérifier le comportement. | Token expiré | Redirection vers `/login` ; vérifier si un token expiré est rejeté ou accepté à tort | | | |

---

## TSP29 — Cloisonnement_Roles (E2E-05) · SP29 · Périmètre : Menu, /admin et /matches · Criticité : Critique (100)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP29-01 | Joueur connecté | Consulter le menu de navigation. | Compte joueur | Lien « Administration » absent | | | |
| TSP29-02 | Joueur connecté | Saisir `/admin` directement dans l'URL. | `/admin` | Redirection vers l'accueil (accès refusé à `/admin`) | | | |
| TSP29-03 | Joueur connecté | Ouvrir `/matches` et inspecter les actions disponibles. | — | Aucun bouton d'administration visible | | | |

---

## TSP30 — Planning (E2E-06) · SP30 · Périmètre : Page /planning · Criticité : Grave (30)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP30-01 | Utilisateur connecté, `/planning` | Cliquer sur mois précédent puis mois suivant. | — | Libellé du mois mis à jour et cohérent | | | |
| TSP30-02 | Utilisateur connecté, `/planning` | Cliquer sur un jour contenant un événement. | Jour avec événement (seed) | Heure, pistes et équipes affichées | | | |

---

## TSP31 — Liste_Matchs (E2E-07) · SP31 · Périmètre : Page /matches · Criticité : Grave (30)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP31-01 | Joueur connecté, `/matches` | Observer l'affichage par défaut. | — | Seuls les matchs du joueur sont affichés | | | |
| TSP31-02 | Joueur connecté, `/matches` | Cocher « tous les matchs » puis utiliser le filtre de statut. | Filtre statut | Tous les matchs affichés, puis liste filtrée selon le statut choisi | | | |

---

## TSP32 — Creation_Match (E2E-08) · SP32 · Périmètre : Page /matches (admin) · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP32-01 | Admin connecté, `/matches` | Créer un match avec des données valides. | Créneau/piste libre | Match visible dans la liste avec le statut `A_VENIR` | | | |
| TSP32-02 | Admin connecté, `/matches` | Créer un match sur une piste déjà occupée au même créneau. | Même piste & créneau | Message de conflit ; vérifier si un doublon est créé sans erreur | | | |

---

## TSP33 — Saisie_Score (E2E-09) · SP33 · Périmètre : Pages /matches et /results · Criticité : Grave (36)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP33-01 | Admin connecté, `/matches` | Saisir un score valide sur un match. | Ex. `6-4, 6-3` | Statut du match passe à `TERMINE` | | | |
| TSP33-02 | Admin connecté, `/matches` | Saisir un score invalide. | Ex. `9-9` | Message d'erreur affiché, statut non validé | | | |
| TSP33-03 | Utilisateur connecté, `/results` | Ouvrir `/results` et vérifier le classement et les scores affichés. | — | Classement mis à jour ; vérifier si seul le score de l'équipe 1 est affiché | | | |

---

## TSP34 — Annulation_Suppression_Match (E2E-10) · SP34 · Périmètre : Page /matches (admin) · Criticité : Pas très grave (3)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP34-01 | Admin connecté, `/matches` | Annuler un match existant. | Match `A_VENIR` | Badge `ANNULE` visible sur le match | | | |
| TSP34-02 | Admin connecté, `/matches` | Supprimer un match. | Match ciblé | Match retiré de la liste | | | |

---

## TSP35 — Gestion_Joueurs_Ecran (E2E-11) · SP35 · Périmètre : Page /admin, onglet Joueurs · Criticité : Pas très grave (9)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP35-01 | Admin connecté, `/admin` (Joueurs) | Créer un joueur valide, tenter une licence invalide (`L123`), puis supprimer le joueur créé. | Licence valide, puis `L123` | Joueur ajouté, message « Format LXXXXXX attendu », puis joueur retiré | | | |

---

## TSP36 — Equipes_Poules_Ecran (E2E-12) · SP36 · Périmètre : Page /admin, onglets Équipes et Poules · Criticité : Pas très grave (3)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP36-01 | Admin connecté, `/admin` (Équipes / Poules) | Créer une équipe de 2 joueurs de la même entreprise, puis créer une poule de 6 équipes. | 2 joueurs même entreprise, 6 équipes | Équipe visible dans l'onglet Équipes et poule visible dans l'onglet Poules | | | |

---

## TSP37 — Creation_Compte_Ecran (E2E-13) · SP37 · Périmètre : Page /admin, onglet Comptes · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP37-01 | Admin connecté, `/admin` (Comptes) | Créer le compte d'un joueur et recharger/quitter la vue. | Joueur existant | Mot de passe temporaire affiché une seule fois | | | |

---

## TSP38 — Affichage_NomMalveillant (E2E-14) · SP38 · Périmètre : Page /matches · Criticité : Critique (100)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP38-01 | Admin / joueur, `/admin` & `/matches` | Nommer une équipe avec une balise HTML `img onerror` puis ouvrir `/matches`. | `<img src=x onerror=alert(1)>` | Aucune alerte JS exécutée (pas de XSS `v-html`), texte affiché tel quel | | | |

---

## TSP39 — Resultats_Ecran (E2E-15) · SP39 · Périmètre : Page /results · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP39-01 | Joueur connecté, `/results` | Ouvrir `/results` et comparer avec les réponses API. | — | Statistiques, résultats et classement cohérents avec l'API | | | |

---

## TSP40 — Profil_Ecran (E2E-16) · SP40 · Périmètre : Page /profile · Criticité : Pas très grave (9)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP40-01 | Utilisateur connecté, `/profile` | Modifier le prénom et enregistrer. | Prénom valide | Message « Profil mis à jour. » | | | |
| TSP40-02 | Utilisateur connecté, `/profile` | Saisir une date de naissance (< 16 ans) et vérifier le champ licence. | Date < 16 ans | Message d'erreur sur l'âge ; champ licence non modifiable | | | |

---

## TSP41 — Accessibilite_ScanAutomatique (ACC-01) · SP41 · Périmètre : Tout le site · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP41-01 | Visiteur puis connecté (joueur & admin) | Inspecter chaque page et chaque onglet `/admin` (contrôle manuel / DevTools inspiré `wcag2a`, `wcag2aa`, `wcag21aa`). | Toutes pages & onglets | Aucune violation d'accessibilité détectée | | | |

---

## TSP42 — Accessibilite_ContrasteTexte (ACC-02) · SP42 · Périmètre : Tout le site · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP42-01 | Toutes pages | Mesurer le contraste des textes (notamment « vs » et le bouton « Annuler »). | Pipette contraste | Contraste texte ≥ 4,5:1 ; vérifier « vs » (~2,5:1) et « Annuler » (~3,2:1) | | | |

---

## TSP43 — Accessibilite_Reflow (ACC-05) · SP43 · Périmètre : Tout le site · Criticité : Grave (30)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP43-01 | Toutes pages & onglets admin | Passer la largeur d'affichage à `320 × 640` px et parcourir les écrans. | Viewport `320×640` | Aucun défilement horizontal, largeur max 320 px ; vérifier menu non replié et tableaux admin | | | |

---

## TSP44 — Accessibilite_LibellesChamps (ACC-12) · SP44 · Périmètre : Tous les formulaires · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP44-01 | Tous les formulaires | Vérifier dans le DOM / inspecteur que chaque champ a un libellé visible relié (`<label>`). | Champs formulaires | Chaque champ est trouvé par son libellé visible ; vérifier labels non reliés et formulaires admin | | | |

---

## TSP45 — Accessibilite_AnnonceMessages (ACC-13) · SP45 · Périmètre : Tous les formulaires · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP45-01 | Tous les formulaires | Déclencher des messages d'erreur/succès et inspecter le DOM. | Erreurs & succès | Attributs `role="alert"` / `aria-live`, `aria-invalid` et `aria-describedby` présents et reliés | | | |

---

## TSP46 — Accessibilite_Calendrier (ACC-14) · SP46 · Périmètre : Page /planning · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP46-01 | Utilisateur connecté, `/planning` | Inspecter le nom accessible des jours du calendrier et du jour sélectionné. | Ex. 15 déc. 2026 | Nom accessible explicite (ex. « 15 décembre 2026, 2 événements ») et jour sélectionné annoncé | | | |

---

## TSP47 — Accessibilite_BoutonsOngletsTableaux (ACC-15) · SP47 · Périmètre : Pages /matches et /admin · Criticité : Pas très grave (18)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP47-01 | `/matches` et `/admin` | Inspecter les boutons « Supprimer », les onglets admin et les en-têtes de tableaux. | DOM / Accessibilité | Noms de boutons explicites, onglets avec `role="tab"`, en-têtes de tableaux balisés (`<th>`) | | | |

---

## TSP48 — Accessibilite_Structure (ACC-16) · SP48 · Périmètre : Tout le site · Criticité : Grave (30)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP48-01 | Toutes pages | Vérifier titres (`h1`–`h6`), `<nav>`, `<main>`, `lang="fr"`, emojis et `<title>` de chaque page. | Toutes routes | Pas de saut de niveau de titre, `lang="fr"`, emojis masqués si décoratifs, `<title>` unique par page | | | |

---

## TSP49 — Accessibilite_NavigationClavier (ACC-18) · SP49 · Périmètre : Tout le site · Criticité : Critique (60)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP49-01 | Toutes pages | Naviguer au clavier (`Tab` / `Maj+Tab`) et vérifier la présence d'un lien d'évitement. | Touche `Tab` | Ordre de focus logique sur toutes les fonctions ; lien « Aller au contenu » accessible en premier | | | |

---

## TSP50 — Accessibilite_Autocompletion (ACC-19) · SP50 · Périmètre : Login, profil, mot de passe · Criticité : Pas très grave (6)

| ID | Pré-requis | Étapes | Donnée | Résultat attendu | Résultat obtenu | OK/KO | ANO |
|---|---|---|---|---|---|---|---|
| TSP50-01 | `/login`, `/profile`, `/change-password` | Vérifier l'attribut `autocomplete` sur email, mots de passe, prénom, nom et date de naissance. | Attribut `autocomplete` | Attribut `autocomplete` présent et approprié sur chaque champ concerné | | | |

---

## Synthèse d'exécution

| Test | Nb de cas | OK | KO | Autre | Méthode | Fiches ANO |
|---|---|---|---|---|---|---|
| TSP25 Accès visiteur | 2 | | | | manuel | |
| TSP26 Connexion | 3 | | | | manuel | |
| TSP27 Premier login / changement mdp | 2 | | | | manuel | |
| TSP28 Déconnexion / session invalide | 3 | | | | manuel | |
| TSP29 Cloisonnement rôles | 3 | | | | manuel | |
| TSP30 Planning | 2 | | | | manuel | |
| TSP31 Liste matchs | 2 | | | | manuel | |
| TSP32 Création match | 2 | | | | manuel | |
| TSP33 Saisie score | 3 | | | | manuel | |
| TSP34 Annulation / suppression match | 2 | | | | manuel | |
| TSP35 Gestion joueurs écran | 1 | | | | manuel | |
| TSP36 Équipes et poules écran | 1 | | | | manuel | |
| TSP37 Création compte écran | 1 | | | | manuel | |
| TSP38 Affichage nom malveillant | 1 | | | | manuel | |
| TSP39 Résultats écran | 1 | | | | manuel | |
| TSP40 Profil écran | 2 | | | | manuel | |
| TSP41 Scan accessibilité | 1 | | | | manuel / DevTools | |
| TSP42 Contraste texte | 1 | | | | manuel / DevTools | |
| TSP43 Reflow 320 px | 1 | | | | manuel / DevTools | |
| TSP44 Libellés champs | 1 | | | | manuel / DevTools | |
| TSP45 Annonce messages | 1 | | | | manuel / DevTools | |
| TSP46 Calendrier accessible | 1 | | | | manuel / DevTools | |
| TSP47 Boutons, onglets, tableaux | 1 | | | | manuel / DevTools | |
| TSP48 Structure document | 1 | | | | manuel / DevTools | |
| TSP49 Navigation clavier | 1 | | | | manuel / DevTools | |
| TSP50 Autocomplétion | 1 | | | | manuel / DevTools | |
| **Total** | **39** | | | | | |

### Fiches d'anomalies ouvertes

| ID | Titre | Type | Sévérité | Méthode |
|---|---|---|---|---|
| | | | | |