# Arena.ai CLI V2 - Remaster

Un wrapper CLI non-officiel premium pour [arena.ai](https://arena.ai), utilisant Playwright headless.

##  Fonctionnalités V2

- **UI Premium** : Rendu Markdown, panels pour les messages, tableaux, spinners, et interface en ligne de commande soignée grâce à `rich` et `prompt_toolkit`.
- **Navigation Intelligente** : Menu interactif pour changer de mode avec `questionary`.
- **Multilignes & Autocomplétion** : Appuie sur **Esc puis Entrée** pour un saut de ligne. Tape `/` pour voir les commandes disponibles.
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

### Lancement (Connexion auto au premier run)
```bash
python arena.py
```
Lors de la première utilisation (ou quand ta session expire), le navigateur va s'ouvrir automatiquement. Connecte-toi normalement sur Arena.ai. Reviens sur le terminal et appuie sur Entrée. **Ta session Playwright sera sauvegardée (en clair, dans `~/.arena_cli/storage_state.json`).**
Les lancements suivants se feront en arrière-plan sans interface de connexion.

### Options utiles
```bash
python arena.py --visible   # Lance le navigateur en mode visible pour suivre ce qu'il fait
python arena.py --debug     # Active les logs complets et les captures d'écran en cas de problème
```

---

##  Commandes dans le chat

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
| `storage_state.json` | La session Playwright Arena (⚠️ en clair) |
| `history/` | Les conversations sauvegardées (`.md` et `.json`) |
| `diagnostics/` | Logs, captures d'écran et HTML lors des erreurs (si `--debug`) |
| `arena_cli.log` | Journal des logs techniques (si `--debug`) |

---

## ⚠️ Notes de sécurité et limites

- **Non-officiel** : Ce script pilote l'interface web de Arena. Il peut casser dès qu'ils modifient leur code HTML. Utilise l'option `--debug` et la commande `/doctor` si les choses ne répondent plus.
- **Session** : Les données de session (cookies, localStorage) sont sauvegardées en **clair** dans `~/.arena_cli/storage_state.json` par commodité.
