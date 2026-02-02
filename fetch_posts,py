import os
import requests
import json

# Dane pobierane z Twoich ustawień i Secretów
TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
PAGE_ID = '156505540370768' 

def fetch_fb_posts():
    # Definiujemy jakie pola chcemy pobrać: treść, data, id
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts?fields=message,created_time,id&access_token={TOKEN}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Sprawdza czy nie ma błędów połączenia
        posts_data = response.json()
        
        # Tworzymy plik raportu w formacie Markdown
        with open('POSTY_FACEBOOK.md', 'w', encoding='utf-8') as f:
            f.write(f"# 📜 Archiwum Postów: Akasha Chronicles\n")
            f.write(f"Ostatnia aktualizacja: {os.popen('date').read()}\n\n---\n\n")
            
            for post in posts_data.get('data', []):
                message = post.get('message', 'Post bez tekstu (grafika/link)')
                date = post.get('created_time', 'Brak daty').replace('T', ' ').split('+')[0]
                post_id = post.get('id')
                fb_link = f"https://www.facebook.com/{post_id}"
                
                f.write(f"### 🕒 Data: {date}\n")
                f.write(f"{message}\n\n")
                f.write(f"[🔗 Zobacz post na Facebooku]({fb_link})\n\n")
                f.write("---\n\n")
                
        print("Sukces! Plik POSTY_FACEBOOK.md został zaktualizowany.")
        
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania danych: {e}")

if _name_ == "_main_":
    fetch_fb_posts()
