import requests
import subprocess
import os
from datetime import datetime

# =======================
# KONFIGURACJA
# =======================

ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = "156505540370768"
FILE_NAME = "facebook_archive.md"
API_VERSION = "v18.0"

if not ACCESS_TOKEN:
    raise RuntimeError("Brak FB_PAGE_ACCESS_TOKEN w GitHub Secrets")

# =======================
# POBIERANIE POSTÓW
# =======================

def fetch_posts():
    url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/feed"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,message,created_time,permalink_url"
    }

    posts = []

    while url:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        posts.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
        params = None

    return posts

# =======================
# ZAPIS DO MARKDOWN
# =======================

def save_posts(posts):
    added = 0

    with open(FILE_NAME, "a", encoding="utf-8") as f:
        for post in reversed(posts):
            created = datetime.fromisoformat(
                post["created_time"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M")

            message = post.get("message", "[Post bez treści – np. samo zdjęcie]")
            link = post.get("permalink_url", "")

            f.write(
                f"### 📌 Post z dnia {created}\n\n"
                f"{message}\n\n"
                f"[Link do posta]({link})\n\n"
                f"---\n\n"
            )

            added += 1

    return added

# =======================
# GIT PUSH
# =======================

def git_push():
    subprocess.run(["git", "add", FILE_NAME], check=True)

    subprocess.run(
        ["git", "commit", "-m", f"Auto-update FB (duplikaty): {datetime.now():%Y-%m-%d %H:%M}"],
        check=True
    )
    subprocess.run(["git", "push", "origin", "main"], check=True)

# =======================
# MAIN
# =======================

if _name_ == "_main_":
    print("➡️ Pobieranie postów z Facebooka...")
    posts = fetch_posts()

    print(f"📥 Pobrano {len(posts)} postów.")
    added = save_posts(posts)

    print(f"✅ Dopisano {added} postów (duplikaty dozwolone).")
    git_push()
