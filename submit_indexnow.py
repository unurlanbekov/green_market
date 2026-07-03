# -*- coding: utf-8 -*-
"""
Отправка всех URL сайта в IndexNow (Яндекс индексирует за часы вместо недель).
Запускать ПОСЛЕ деплоя на Vercel: python3 submit_indexnow.py
При смене домена поменяй BASE в build.py, пересобери сайт и запусти снова.
"""
import json, re, urllib.request

BASE = "https://green-market-blue.vercel.app"   # должен совпадать с BASE в build.py
KEY = "a7f3c9e1b5d24086a1f0c3e7d9b52468"

urls = re.findall(r"<loc>(.*?)</loc>", open("sitemap.xml", encoding="utf-8").read())
payload = {
    "host": BASE.replace("https://", ""),
    "key": KEY,
    "keyLocation": f"{BASE}/{KEY}.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://yandex.com/indexnow",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow (Yandex):", r.status, "— отправлено URL:", len(urls))
except Exception as e:
    print("Ошибка IndexNow:", e)

# Пинг Google sitemap (официальный ping отключён, но GSC подтянет sitemap сам —
# главное, чтобы он был добавлен в Search Console)
print("Не забудь: Search Console → Файлы Sitemap → отправить", f"{BASE}/sitemap.xml")
