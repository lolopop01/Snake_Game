# Jeu de Snake avec manette Wii 🎮🐍

Bienvenue dans le jeu de Snake contrôlé par une manette Wii ! Suivez les étapes ci-dessous pour installer les dépendances, configurer votre environnement et commencer à jouer.

---

## Étapes d'installation et de jeu

### 1. Installer les bibliothèques Bluetooth
Avant tout, assurez-vous que les bibliothèques Bluetooth nécessaires sont installées. Sur un système Linux, exécutez la commande suivante dans votre terminal :  
```bash
sudo apt-get install bluetooth libbluetooth-dev
```
⚠️ Remarque : Assurez-vous que votre système dispose des privilèges root pour exécuter cette commande.


### 2. Installer pybluez
Avant tout, assurez-vous que pybluez est installées. Sur un système Linux, exécutez la commande suivante dans votre venv :  
- Si vous ne savez pas comment créer un environnement virtuel, utilisez cette commande pour en créer un :
- ```bash
  python -m venv venv
  source venv/bin/activate  # Sur Linux/MacOS
  venv\Scripts\activate     # Sur Windows
    ```
- ```bash
  pip install git+https://github.com/pybluez/pybluez.git
  ```
 - ⚠️ Remarque : Assurez-vous d'être toujours dans votre environnement virtuel activé pour éviter les conflits de dépendances.

   

### 3. Installer les dépendances
Le fichier `requirements.txt` contient toutes les dépendances nécessaires pour exécuter le jeu. Pour les installer, utilisez la commande suivante dans le terminal :
- ```bash
  pip install -r requirements.txt
  ```
 - ⚠️ Remarque : Assurez-vous d'être toujours dans votre environnement virtuel activé pour éviter les conflits de dépendances.

### 4. Lancer le jeu dans un terminal
Une fois les dépendances installées, vous pouvez lancer le jeu. Placez-vous dans le répertoire du projet contenant le fichier `SnakeGame.py` et exécutez :
- ```bash
  python SnakeGame.py
  ```
- Cette commande démarre le jeu et initialise la connexion Bluetooth


### 5. Connecter la manette de wii
Lorsque le jeu démarre, suivez les instructions affichées à l'écran pour connecter votre manette Wii.
- Activez le mode Bluetooth de votre manette Wii en appuyant sur le bouton `SYNC` de la manette.
- Votre manette devrait clignoter pour indiquer qu'elle est en mode appairage.
- Appuyer sur la touche `ENTER` dans le terminal pour commencer le appairage avec le jeu
- Le jeu devrait lancer si la manette est connectée.

### 6. Avoir du plaisir!
Une fois la manette connectée, amusez-vous en jouant au jeu Snake ! 🎮
- Déplacez le serpent à l’aide des boutons de la manette Wii.
- Mangez les fruits pour gagner des points et grandir.
- Évitez les obstacles et ne vous mordez pas la queue !
