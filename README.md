# Arena.ai CLI V2 - Remaster

Un wrapper CLI non-officiel premium pour [arena.ai](https://arena.ai), utilisant Playwright headless.

##  Fonctionnalités V2

- **UI Premium** : Rendu Markdown, panels pour les messages, tableaux, spinners, et interface en ligne de commande soignée grâce à `rich` et `prompt_toolkit`.
- **Navigation Intelligente** : Menu interactif pour changer de mode avec `questionary`.
- **Multilignes & Autocomplétion** : Appuie sur `Alt+Entrée` pour un saut de ligne. Tape `/` pour voir les commandes disponibles.
- **Sauvegarde d'historique** : Sauvegarde tes conversations en JSON et Markdown.
- **Mode Diagnostic** : Détection de l'état de connexion via signaux positifs, log des erreurs, et outil `/doctor` pour le debug.

---

##  Installation

**La V2 utilise des environnements virtuels (venv) pour isoler l'installation.**

### Windows
Double-clique sur `installer_windows.bat`

### Mac / Linux
```bash
chmod +x installer_mac_linux.sh
./installer_mac_linux.sh
```

---

##  Utilisation

Une fois installé, lance toujours les commandes à l'intérieur du `venv` (activé automatiquement par les scripts ou manuellement avec `source .venv/bin/activate` / `.venv\Scripts\activate`).

### Étape 1 — Connexion (première fois ou quand la session expire)
```bash
python arena.py --login
```
Un navigateur Chrome va s'ouvrir. Connecte-toi normalement sur Arena.ai (Google, Email, Discord...). Reviens sur le terminal et appuie sur Entrée. **Tes cookies seront sauvegardés (en clair, dans `~/.arena_cli/`).**

### Étape 2 — Chat
```bash
python arena.py
```

### Options utiles
```bash
python arena.py --visible   # Lance le navigateur en mode visible pour suivre ce qu'il fait
python arena.py --debug     # Active les logs complets et les captures d'écran en cas de problème
```

---

## ⌨️ Commandes dans le chat

| Commande | Action |
|----------|--------|
| `/mode` | Ouvrir le menu interactif pour changer de mode |
| `/models` | Voir les modèles disponibles pour le mode actuel |
| `/clear` | Démarrer une nouvelle conversation |
| `/save` | Sauvegarder la session courante (md + json) |
| `/history` | Lister l'historique des sessions récentes |
| `/doctor` | Lancer un diagnostic (utile avec `--debug`) |
| `/help` | Afficher l'aide |
| `/quit` | Quitter l'application |

---

##  Configuration et Fichiers

Les données locales sont stockées dans le dossier `~/.arena_cli/` de ton répertoire utilisateur.

| Fichier / Dossier | Rôle |
|-------------------|------|
| `config.json` | Préférences globales (dernier mode, etc) |
| `cookies.json` | Les cookies de session Arena (⚠️ en clair) |
| `history/` | Les conversations sauvegardées (`.md` et `.json`) |
| `diagnostics/` | Logs, captures d'écran et HTML lors des erreurs (si `--debug`) |
| `arena_cli.log` | Journal des logs techniques (si `--debug`) |

---

## ⚠️ Notes de sécurité et limites

- **Non-officiel** : Ce script pilote l'interface web de Arena. Il peut casser dès qu'ils modifient leur code HTML. Utilise l'option `--debug` et la commande `/doctor` si les choses ne répondent plus.
- **Cookies** : Les cookies de session sont sauvegardés en **clair** dans `~/.arena_cli/cookies.json` par commodité.
