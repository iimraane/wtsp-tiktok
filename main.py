from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp
import re


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\chrome-data")


# Démarrer le navigateur
driver = webdriver.Chrome(options=options)

# Ouvrir WhatsApp Web
driver.get("https://web.whatsapp.com/")
print("🕒 Scanne le QR Code sur WhatsApp pour te connecter...")
input("Appuie sur entrée une fois terminé")
driver.find_element(By.XPATH, '//span[@title="Groupe de famille😍😎😍"]').click()


def envoyer_video_whatsapp(driver, nom_fichier):
    try:
        wait = WebDriverWait(driver, 15)

        print("[INFO] 🟢 Ouverture du menu pièces jointes...")

        # 1. Cliquer sur le bouton "+" (Joindre)
        bouton_plus = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Joindre']")))
        bouton_plus.click()
        time.sleep(1)

        print("[INFO] 📎 Menu ouvert, recherche du bouton 'Photos et vidéos'...")

        # 2. Trouver l'élément contenant "Photos et vidéos"
        bouton_photo_video = wait.until(EC.presence_of_element_located((
            By.XPATH, "//span[contains(text(),'Photos et vidéos')]/ancestor::li"
        )))
        bouton_photo_video.click()
        time.sleep(1)

        print("[INFO] 📤 Envoi du chemin vers le fichier vidéo...")

        # 3. Localiser l'input de type file dans ce menu (celui qui accepte image et vidéo)
        input_file = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
        )))

        chemin_fichier = os.path.abspath(nom_fichier)
        input_file.send_keys(chemin_fichier)

        print(f"[INFO] 📁 Fichier sélectionné : {chemin_fichier}")
        time.sleep(2)  # Prévisualisation

        print("[INFO] 📤 Envoi de la vidéo...")

        # 4. Cliquer sur le bouton "Envoyer"
        bouton_envoyer = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']")))
        bouton_envoyer.click()

        print("✅ Vidéo envoyée avec succès !")
        

    except Exception as e:
        print(f"❌ Erreur pendant l’envoi de la vidéo : {e}")

def deja_envoyee(nom_fichier):
    if not os.path.exists("envoyees.txt"):
        return False
    with open("envoyees.txt", "r", encoding="utf-8") as f:
        return nom_fichier in f.read().splitlines()
    
def enregistrer_video_envoyee(nom_fichier):
    with open("envoyees.txt", "a", encoding="utf-8") as f:
        f.write(nom_fichier + "\n")


while True:

    

    # Attendre que les messages soient visibles
    print("🔍 Recherche du dernier message...")
    time.sleep(5)

    # Récupérer tous les messages de la dernière conversation
    messages = driver.find_elements(By.CSS_SELECTOR, "div.copyable-text")

    if not messages:
        print("❌ Aucun message trouvé.")
    else:
        # Prendre le dernier message (le plus récent)
        last_message = messages[-1].text
        print(f"📨 Dernier message detecté")


    # Vérifie si un lien est présent dans le message
    if messages:
        if "tiktok.com" in last_message or "instagram.com/reel" in last_message or "/reel/" in last_message:
            print("✅ Lien détecté dans le message.")
            
            # Extraction des URL dans le message
            urls = re.findall(r'(https?://[^\s]+)', last_message)
            for url in urls:
                if "tiktok.com" in url or "instagram.com/reel" in url:
                    print(f"🎯 Téléchargement de la vidéo depuis : {url}")

                    # Configuration yt-dlp
                    ydl_opts = {
                        'outtmpl': '%(title)s.%(ext)s',
                        'format': 'mp4',
                        'quiet': False
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info_dict = ydl.extract_info(url, download=True)
                            filename = ydl.prepare_filename(info_dict)
                            print(f"✅ Téléchargement terminé : {filename}")
                        
                        
                        # Vérifie que le fichier a bien été téléchargé
                        if os.path.exists(filename):
                            if not deja_envoyee(filename):
                                try:
                                    envoyer_video_whatsapp(driver, filename)
                                    enregistrer_video_envoyee(filename)
                                except Exception as e:
                                    print(f"❌ Erreur lors de l’envoi WhatsApp : {e}")
                            
                            else:
                                print("🔁 Vidéo déjà envoyée.")

                        else:
                            print(f"❌ Fichier non trouvé : {filename}")

                    except Exception as e:
                        print(f"❌ Erreur pendant le téléchargement : {e}")
        else:
            print("📭 Aucun lien TikTok ou Reels dans le dernier message.")
    else:
        pass

