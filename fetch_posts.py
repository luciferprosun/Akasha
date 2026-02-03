import os
import requests
import json
from datetime import datetime

# Poprawiona nazwa, aby pasowała do Twojego Secretu na GitHubie (z jednym 'S')
TOKEN = os.getenv('FB_PAGE_ACCES_TOKEN')
PAGE_ID = '15655540376768'

def fetch_fb_posts():
    # URL do API Facebooka
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=message,created_time,id&access_token={TOKEN}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        posts_data = response.json()

        with open('POSTY_FACEBOOK.md', 'w', encoding='utf-8') as f:
            f.write(f"# Archiwum Postów: Akasha Chronicles\n")
            
            # Czysty sposób na datę (bez używania os.popen, co jest bezpieczniejsze na Mint)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Ostatnia aktualizacja: {now}\n\n---\n\n")

            for post in posts_data.get('data', []):
                message = post.get('message', 'Post bez tekstu (grafika/link)')
                date = post.get('created_time', 'Brak daty').replace('T', ' ').split('+')[0]
                fb_link = f"https://www.facebook.com/{post.get('id')}"

                f.write(f"### Data: {date}\n")
                f.write(f"{message}\n\n")
                f.write(f"[Zobacz post na Facebooku]({fb_link})\n")
                f.write("---\n\n")

        print("Sukces! Plik POSTY_FACEBOOK.md został zaktualizowany.")
        
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych: {e}")

if _name_ == "_main_":
    fetch_fb_posts()
