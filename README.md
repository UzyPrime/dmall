# Bot Discord Dmall

Bot Discord pour envoyer des messages privés à tous les membres d'un serveur.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurez le token du bot :
   - Ouvrez `config.py`
   - Remplacez `your_bot_token_here` par votre token de bot Discord

3. Lancez le bot :
```bash
python main.py
```

## Commandes

- `/dmall <message>` - Envoie un message privé à tous les membres en ligne
- `/dmallstatus` - Affiche les statistiques du serveur

## Permissions requises

- Le bot doit avoir les permissions "Envoyer des messages privés aux membres du serveur"
- Seuls les administrateurs peuvent utiliser les commandes

## Fonctionnalités

- Envoi rapide avec délai de 0.1 seconde entre chaque message
- Suivi de progression en temps réel
- Gestion des erreurs et des échecs
- Messages formatés avec embeds
- Statistiques détaillées
