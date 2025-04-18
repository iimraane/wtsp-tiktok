# Envoi Automatique de Vidéos WhatsApp

## Description

Ce script automatise WhatsApp Web pour surveiller une conversation, détecter les liens TikTok et Instagram Reels, télécharger la vidéo via **yt-dlp**, puis l’envoyer directement dans le même chat. Vous ne scannez le QR Code qu’une seule fois : la session est conservée grâce à un profil Chrome persistant (`--user-data-dir`).

### Fonctionnalités

- Surveillance en continu du dernier message d’une conversation WhatsApp Web  
- Détection de liens **tiktok.com** et **instagram.com/reel**  
- Téléchargement des vidéos avec **yt-dlp**  
- Envoi automatique de la vidéo via l’interface WhatsApp Web  
- Historique pour éviter les doublons (`envoyees.txt`)  
- Authentification unique : connexion QR Code une seule fois  

---

## Prérequis

- **Python 3.7+**  
- **Google Chrome** installé  
- **ChromeDriver** compatible (dans le PATH)  
- Modules Python :

```bash
pip install selenium yt-dlp
```

---

## Configuration

Dans `main.py` :

```python
options.add_argument("--user-data-dir=C:\\Temp\\chrome-data")
```

- **Chemin du profil Chrome** : modifiez `C:\\Temp\\chrome-data` pour stocker la session WhatsApp.  
- **Sélecteur du chat** : changez le titre du groupe dans :
  ```python
  driver.find_element(By.XPATH, '//span[@title="Groupe de famille😍😎😍"]').click()
  ```

---

## Structure

```
main.py           # Script principal
envoyees.txt      # Liste des vidéos déjà envoyées (généré à la volée)
chrome-data/      # Profil Chrome pour la session WhatsApp
```

---

## Utilisation

1. Lancez :
   ```bash
   python main.py
   ```
2. **Première exécution** : WhatsApp Web s’ouvre, scannez le QR Code.  
3. Une fois connecté, appuyez sur **Entrée** dans le terminal.  
4. Le script recherche le dernier message toutes les 5 secondes, télécharge et envoie la vidéo si un lien valide est détecté.  
5. Les vidéos déjà envoyées ne seront pas renvoyées.

---

## Explication du code

- **Session persistante**  
  `--user-data-dir` garde la session QR valide après la première connexion.  
- **Boucle de surveillance**  
  Extrait le dernier message via Selenium et vérifie la présence de liens.  
- **Téléchargement**  
  `yt-dlp` récupère la vidéo, le nom est nettoyé des emojis.  
- **Envoi**  
  Automatisation du menu « Joindre » et clic sur « Photos et vidéos » pour envoyer le fichier.  
- **Historique**  
  `envoyees.txt` stocke les noms des fichiers déjà partagés pour éviter les doublons.

---

## Personnalisation

- **Groupe cible** : modifiez le XPATH `//span[@title="…"]`  
- **Profil Chrome** : ajustez le chemin `--user-data-dir`  
- **Délais** : adaptez les `time.sleep()` si votre connexion est lente  

---

## Dépannage

- **Chrome/ChromeDriver** : versions compatibles requises  
- **Profil Chrome** : le dossier doit exister et être accessible  
- **yt-dlp** : mettez à jour si nécessaire :  
  ```bash
  pip install -U yt-dlp
  ```

---

## Sécurité

- Ne partagez pas votre dossier de session Chrome (`chrome-data`)  
- Protégez vos vidéos locales et ne versionnez pas `envoyees.txt` publiquement  

---

## Licence

Please just don't steal my code..
