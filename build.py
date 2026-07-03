# -*- coding: utf-8 -*-
"""
Tamyr — генератор статического сайта (SEO-сборка).
Меняешь BASE при подключении домена tamyr.kg и запускаешь: python3 build.py
Все .html генерируются с едиными хедером/футером/schema и уникальными мета-тегами.
"""
import json, os, html, datetime
import product_meta as PM

TODAY = datetime.date.today().isoformat()

# RU → латиница для ЧПУ-слагов товарных страниц (НЧ-запросы)
_TR = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z',
    'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
    'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch',
    'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',' ':'-','(':'',')':'',
    ',':'','«':'','»':'','—':'-','/':'-','.':'',
}
def slugify(s):
    s = s.lower().strip()
    out = ''.join(_TR.get(ch, ch) for ch in s)
    while '--' in out:
        out = out.replace('--', '-')
    return out.strip('-')

# === ЕДИНСТВЕННОЕ, ЧТО МЕНЯЕМ ПРИ ПОДКЛЮЧЕНИИ ДОМЕНА ===
BASE = "https://green-market-blue.vercel.app"   # → "https://tamyr.kg"
PHONE = "+996500707111"
WA = "996500707111"
IG = "https://www.instagram.com/tamyr_flowers_bishkek"
OG_IMG = BASE + "/css/IMG_0352.jpg"
GSV = "qi2TNoqrFo1AulwhzlUSDewMKiUcjgn2CACSs36jldE"
# Яндекс.Вебмастер: вставьте сюда код подтверждения (webmaster.yandex.ru → Добавить сайт → Мета-тег) и запустите build.py
YANDEX_VERIFICATION = ""
# IndexNow: ключ для мгновенной индексации в Яндексе (файл {ключ}.txt лежит в корне сайта)
INDEXNOW_KEY = "a7f3c9e1b5d24086a1f0c3e7d9b52468"
ROOT = os.path.dirname(os.path.abspath(__file__))

def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"

# Общая навигация (важно для внутренней перелинковки)
NAV = [
    ("komnatnye-rasteniya.html", "Комнатные растения"),
    ("krupnye-rasteniya.html",   "Крупные и офисные"),
    ("tsvety.html",              "Цветы"),
    ("gorshki-kashpo.html",      "Горшки и кашпо"),
    ("grunt-dlya-rasteniy.html", "Грунты"),
    ("dostavka-i-oplata.html",   "Доставка"),
    ("kontakty.html",            "Контакты"),
]

WA_SVG = '<svg class="ico-wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 00-8.5 15.2L2 22l4.9-1.4A10 10 0 1012 2zm0 18a8 8 0 01-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1112 20zm4.4-6c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5 0a6.6 6.6 0 01-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.1 0-.3 0-.4l-.7-1.7c-.2-.5-.4-.4-.5-.4h-.5a1 1 0 00-.7.3c-.3.3-1 1-1 2.3s1 2.7 1.2 2.9a9 9 0 005.3 3.7c1.3.4 1.8.3 2.4.2s1.4-.6 1.6-1.1.2-1 .2-1.1-.2-.2-.4-.3z" fill="currentColor"/></svg>'
LEAF_MARK = '<svg viewBox="0 0 32 32" fill="none"><path d="M16 28C16 20 10 16 6 14c6-1 10 1 10 6 0-7 4-11 10-12-1 7-5 10-10 10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def head(title, desc, path, keywords, schema_blocks, prefix=""):
    canonical = BASE + "/" + path
    yv = f'\n<meta name="yandex-verification" content="{YANDEX_VERIFICATION}" />' if YANDEX_VERIFICATION else ""
    schema = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + '\n</script>'
        for b in schema_blocks
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(keywords)}">
<meta name="robots" content="index, follow">
<meta name="author" content="Tamyr">
<link rel="canonical" href="{canonical}">
<meta name="geo.region" content="KG">
<meta name="geo.placename" content="Бишкек">
<meta name="geo.position" content="42.829009;74.537612">
<meta name="ICBM" content="42.829009, 74.537612">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tamyr">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{OG_IMG}">
{schema}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/styles.css">
<link rel="icon" type="image/png" href="{prefix}img/favicon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="{prefix}img/favicon-192.png">
<meta name="google-site-verification" content="{GSV}" />{yv}
</head>
<body>"""

def header(active="", prefix=""):
    links = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links += f'      <a href="{prefix}{href}"{cur}>{label}</a>\n'
    return f"""
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="{prefix}index.html">
      <img class="brand-mark" src="{prefix}img/logo.png" alt="Tamyr — магазин растений в Бишкеке" width="30" height="30">
      <span class="brand-text">Tamyr</span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="head-nav">Меню</button>
    <nav class="head-nav" id="head-nav" aria-label="Каталог">
{links}    </nav>
    <a class="btn btn-sm" href="{wa_link('Здравствуйте! Пишу с сайта — хочу узнать про растения 🌿')}" target="_blank" rel="noopener">Написать нам</a>
  </div>
</header>
"""

def footer(prefix=""):
    cat_links = "".join(f'<a href="{prefix}{h}">{l}</a>' for h, l in NAV[:5])
    return f"""
  <footer id="contacts" class="site-foot">
    <div class="wrap foot-inner">
      <div class="foot-brand">
        <img class="brand-mark" src="{prefix}img/logo.png" alt="Tamyr — магазин растений в Бишкеке" width="30" height="30">
        <span class="brand-text">Tamyr</span>
        <p class="foot-tag">Комнатные, домашние и офисные растения в горшках. Цветы, горшки, кашпо и грунты. Доставка по Бишкеку.</p>
      </div>
      <div class="foot-col">
        <h4>Каталог</h4>
        {cat_links}
        <a href="{prefix}ozelenenie-ofisov.html">Озеленение офисов</a>
        <a href="{prefix}rasteniya-v-podarok.html">Растение в подарок</a>
        <a href="{prefix}blog.html">Блог об уходе</a>
      </div>
      <div class="foot-col">
        <h4>Связаться</h4>
        <a href="tel:{PHONE}">{PHONE[:4]} {PHONE[4:7]} {PHONE[7:10]} {PHONE[10:]}</a>
        <a href="{wa_link('Здравствуйте! Пишу с сайта 🌿')}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="{IG}" target="_blank" rel="noopener">Instagram</a>
        <div class="foot-sub">
          <p><a href="https://maps.app.goo.gl/Ho3o1xcf9eQN6PWe9?g_st=ic" target="_blank" rel="noopener">г.Бишкек, Киргизия 1, ул.Абдрахманова 118 / 7, дом 82</a></p>
          <p>Ежедневно, 10:00–19:00</p>
        </div>
      </div>
    </div>
    <div class="wrap foot-bottom">
      <span>© <span id="year"></span> Tamyr</span>
      <span>Бишкек · Кыргызстан</span>
    </div>
  </footer>
</main>

<a class="wa-widget" href="{wa_link('Здравствуйте! Пишу с сайта — хочу узнать про растения 🌿')}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">
  <span class="wa-pulse" aria-hidden="true"></span>
  <span class="wa-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 00-8.5 15.2L2 22l4.9-1.4A10 10 0 1012 2zm0 18a8 8 0 01-4.1-1.1l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1112 20zm4.4-6c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5 0a6.6 6.6 0 01-3.3-2.9c-.2-.4.2-.4.6-1.2.1-.1 0-.3 0-.4l-.7-1.7c-.2-.5-.4-.4-.5-.4h-.5a1 1 0 00-.7.3c-.3.3-1 1-1 2.3s1 2.7 1.2 2.9a9 9 0 005.3 3.7c1.3.4 1.8.3 2.4.2s1.4-.6 1.6-1.1.2-1 .2-1.1-.2-.2-.4-.3z" fill="currentColor"/></svg></span>
  <span class="wa-label">Напишите нам</span>
</a>
<script src="{prefix}js/script.js"></script>
</body>
</html>"""

def crumbs(items, prefix=""):
    # items: list of (label, href|None)
    lis = ""
    for label, href in items:
        if href:
            lis += f'<li><a href="{prefix}{href}">{label}</a></li>'
        else:
            lis += f'<li aria-current="page">{label}</li>'
    return f'<nav class="crumbs wrap" aria-label="Хлебные крошки"><ol>{lis}</ol></nav>'

def breadcrumb_schema(items):
    el = []
    for i, (label, href) in enumerate(items, 1):
        url = BASE + "/" if href == "index.html" else BASE + "/" + href if href else BASE + "/" + items[-1][0]
        node = {"@type": "ListItem", "position": i, "name": label}
        if href:
            node["item"] = BASE + "/" + ("" if href == "index.html" else href)
        el.append(node)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}

def faq_schema(qa):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa
        ]
    }

def cat_pills(active, prefix=""):
    items = ""
    for href, label in NAV[:5]:
        cur = ' aria-current="true"' if href == active else ""
        items += f'<a class="cat-pill" href="{prefix}{href}"{cur}>{label}</a>'
    return f'<div class="cat-pills">{items}</div>'

def product_cards(products, mediaclass=""):
    out = ""
    for p in products:
        msg = f"Здравствуйте! Интересует «{p['name']}» — подскажите наличие и цену 🌿"
        slug = slugify(p['name'])
        _goods = PM.META.get(p['name'], {}).get("kind") == "goods"
        _more = "Подробнее →" if _goods else "Подробнее об уходе →"
        _imgpath = f"img/products/{slug}.jpg"
        _alt = f"{p['name']} — купить в Бишкеке, магазин растений Tamyr"
        if os.path.exists(_imgpath):
            _media = f'<a class="card-media has-photo {mediaclass}" href="p/{slug}.html"><img src="{_imgpath}" alt="{html.escape(_alt)}" loading="lazy" width="800" height="800"></a>'
        else:
            _media = f'<a class="card-media {mediaclass}" href="p/{slug}.html" aria-label="{html.escape(p["name"])} — подробнее">{p["emoji"]}</a>'
        out += f"""    <article class="card reveal">
      {_media}
      <div class="card-body">
        <h3 class="card-title"><a href="p/{slug}.html">{html.escape(p['name'])}</a></h3>
        <p class="card-desc">{html.escape(p['desc'])}</p>
        <div class="card-foot">
          <span class="card-price">{p['price']}<small>цена-ориентир</small></span>
          <a class="card-cta" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_SVG}<span>Заказать</span></a>
        </div>
        <a class="card-more" href="p/{slug}.html">{_more}</a>
      </div>
    </article>
"""
    return out

def itemlist_schema(products, page_url):
    el = []
    for i, p in enumerate(products, 1):
        el.append({
            "@type": "ListItem", "position": i,
            "item": {
                "@type": "Product", "name": p["name"], "description": p["desc"],
                "category": p.get("category", ""),
                "brand": {"@type": "Brand", "name": "Tamyr"},
                "offers": {
                    "@type": "Offer", "priceCurrency": "KGS",
                    "price": str(p["price_num"]), "availability": "https://schema.org/InStock",
                    "url": page_url, "seller": {"@type": "Organization", "name": "Tamyr"}
                }
            }
        })
    return {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": el}

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("written:", path)

# ====================================================================
#  КОНТЕНТ КАТЕГОРИЙ
# ====================================================================

import content_data as C
C.build_all(globals())

# ====================================================================
#  ОТДЕЛЬНЫЕ СТРАНИЦЫ ТОВАРОВ (НЧ-запросы: «{товар} купить бишкек»)
# ====================================================================
CAT_MAP = {
    "komnatnye": ("komnatnye-rasteniya.html", "Комнатные растения"),
    "krupnye":   ("krupnye-rasteniya.html",   "Крупные и офисные растения"),
    "tsvety":    ("tsvety.html",              "Цветы"),
    "gorshki":   ("gorshki-kashpo.html",      "Горшки и кашпо"),
    "grunt":     ("grunt-dlya-rasteniy.html", "Грунты"),
}
PRODUCT_URLS = []

def facts_table(m):
    rows = []
    if m.get("kind") != "goods":
        rows = [("☀️ Свет", m.get("light","—")), ("💧 Полив", m.get("water","—")),
                ("🌱 Сложность", m.get("difficulty","—")), ("📏 Высота", m.get("height","—"))]
        if m.get("lat"):
            rows.append(("🔖 Вид", "<em>" + html.escape(m["lat"]) + "</em>"))
    else:
        if m.get("height") and m["height"] != "—":
            rows = [("📏 Размер", m["height"])]
    if not rows:
        return ""
    cells = "".join(f'<div class="fact"><span class="fact-k">{k}</span><span class="fact-v">{v}</span></div>' for k, v in rows)
    return f'<div class="facts">{cells}</div>'

def product_page(catkey, p):
    cat_href, cat_label = CAT_MAP[catkey]
    m = PM.META.get(p["name"], {})
    slug = slugify(p["name"])
    path = f"p/{slug}.html"
    page_url = BASE + "/" + path
    name = p["name"]
    is_goods = m.get("kind") == "goods"

    title = f"{name} в Бишкеке — купить с доставкой | Tamyr"
    desc = (f"{name}: {p['desc']} {p['price'].capitalize()}. "
            f"Доставка по Бишкеку, подбор и консультация. Заказ в WhatsApp — магазин растений Tamyr.")[:300]
    keywords = f"{name.lower()} бишкек, купить {name.lower()}, {name.lower()} цена, {cat_label.lower()} бишкек"
    msg = f"Здравствуйте! Интересует «{name}» — подскажите наличие и цену 🌿"

    product_schema = {
        "@context": "https://schema.org", "@type": "Product",
        "name": name, "description": p["desc"], "category": cat_label,
        "brand": {"@type": "Brand", "name": "Tamyr"},
        "offers": {"@type": "Offer", "priceCurrency": "KGS", "price": str(p["price_num"]),
                   "availability": "https://schema.org/InStock", "url": page_url,
                   "areaServed": {"@type": "City", "name": "Бишкек"},
                   "seller": {"@type": "Organization", "name": "Tamyr"}},
    }
    if not is_goods:
        qa = [
            (f"Как ухаживать за «{name}»?", m.get("care", "Подскажем уход под ваши условия в WhatsApp.")),
            (f"Можно купить «{name}» с доставкой по Бишкеку?", f"Да. Доставляем по всему Бишкеку, оплата переводом или при получении. {p['price'].capitalize()} — точную цену и наличие пришлём в WhatsApp."),
        ]
    else:
        qa = [
            (f"Как выбрать «{name}»?", m.get("care", "Поможем подобрать под ваше растение в WhatsApp.")),
            ("Есть доставка по Бишкеку?", "Да, доставляем по всему городу. Наличие и цену пришлём в WhatsApp."),
        ]
    if os.path.exists(f"img/products/{slug}.jpg"):
        product_schema["image"] = BASE + "/img/products/" + slug + ".jpg"
    schema = [
        breadcrumb_schema([("Главная", "index.html"), (cat_label, cat_href), (name, None)]),
        product_schema, faq_schema(qa),
    ]

    body = head(title, desc, path, keywords, schema, prefix="../")
    body += header(cat_href, prefix="../")
    body += crumbs([("Главная", "index.html"), (cat_label, cat_href), (name, None)], prefix="../")

    facts = facts_table(m)
    about = html.escape(m.get("about", p["desc"]))
    care = html.escape(m.get("care", ""))

    _imgpath = f"img/products/{slug}.jpg"
    if os.path.exists(_imgpath):
        _alt = f"{name} — купить в Бишкеке, магазин растений Tamyr"
        ph_media = f'<div class="ph-media has-photo"><img src="../{_imgpath}" alt="{html.escape(_alt)}" width="800" height="800"></div>'
    else:
        ph_media = f'<div class="ph-media" role="img" aria-label="{html.escape(name)} — Tamyr, Бишкек">{p["emoji"]}</div>'

    sibs = [x for x in C.P(C.PRODUCTS[catkey]) if x["name"] != name][:3]
    rel_cards = ""
    for s in sibs:
        sslug = slugify(s["name"])
        rel_cards += f'<a class="cat-pill" href="{sslug}.html">{s["emoji"]} {html.escape(s["name"])}</a>'

    care_h2 = "Как выбрать" if is_goods else f"Как ухаживать за «{html.escape(name)}»"
    care_eyebrow = "Как выбрать" if is_goods else "Уход"
    care_block = f"""
  <section class="section seo-prose reveal">
    <header class="sec-head"><p class="eyebrow">{care_eyebrow}</p><h2>{care_h2}</h2></header>
    <p>{care}</p>
  </section>""" if care else ""

    body += f"""
<main id="top">
  <div class="wrap">
  <section class="product-hero reveal">
    {ph_media}
    <div class="ph-info">
      <p class="eyebrow">{cat_label} · Бишкек</p>
      <h1>{html.escape(name)} в Бишкеке</h1>
      <p class="lead">{html.escape(p['desc'])}</p>
      {facts}
      <div class="ph-buy">
        <span class="card-price ph-price">{p['price']}<small>цена-ориентир, уточним в WhatsApp</small></span>
        <a class="btn btn-wa btn-lg" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_SVG}Заказать в WhatsApp</a>
      </div>
    </div>
  </section>

  <section class="section seo-prose reveal">
    <header class="sec-head"><p class="eyebrow">О товаре</p><h2>{html.escape(name)}</h2></header>
    <p>{about}</p>
  </section>
{care_block}
  <section class="section reveal">
    <header class="sec-head"><p class="eyebrow">Смотрите также</p><h2>Похожие из раздела «{cat_label}»</h2></header>
    <div class="cat-pills">{rel_cards}<a class="cat-pill" href="../{cat_href}">Все: {cat_label} →</a></div>
  </section>

  <section id="faq" class="section">
    <header class="sec-head reveal"><p class="eyebrow">Частые вопросы</p><h2>Вопросы и ответы</h2></header>
    <div class="bento faq-bento">
"""
    for q, a in qa:
        body += f'      <article class="tile tile-faq reveal"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></article>\n'
    body += "    </div>\n  </section>\n  </div>\n"
    body += footer(prefix="../")
    write(path, body)
    PRODUCT_URLS.append(path)

for catkey in C.PRODUCTS:
    for p in C.P(C.PRODUCTS[catkey]):
        product_page(catkey, p)

# ====================================================================
#  КОММЕРЧЕСКИЕ ЛЕНДИНГИ (СЧ-запросы: озеленение офисов, растение в подарок)
# ====================================================================

def _cta_strip(h2, p, msg):
    return f"""
  <section class="section">
    <div class="tile cta-strip reveal">
      <div><h2>{h2}</h2><p>{p}</p></div>
      <a class="btn btn-wa btn-lg" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_SVG}Написать в WhatsApp</a>
    </div>
  </section>"""

def build_office_landing():
    path = "ozelenenie-ofisov.html"
    title = "Озеленение офисов в Бишкеке — растения для офиса под ключ | Tamyr"
    desc = ("Озеленение офисов, кафе и салонов в Бишкеке под ключ: подберём растения под освещение, "
            "привезём, посадим в кашпо и расскажем про уход. Крупные и неприхотливые офисные растения. Заказ в WhatsApp.")
    kw = "озеленение офиса бишкек, растения для офиса бишкек, цветы в офис, офисные растения купить бишкек, озеленение кафе"
    qa = [
        ("Сколько стоит озеленение офиса?", "Зависит от площади и количества растений. Базовый вариант — от нескольких крупных растений в кашпо от 3 500 сом за позицию. Пришлите фото помещения в WhatsApp — посчитаем смету бесплатно."),
        ("Какие растения подходят для офиса?", "Неприхотливые и теневыносливые: замиокулькас, сансевиерия, шеффлера, юкка, драцена, хамедорея. Они переносят офисное освещение, сухой воздух от кондиционера и полив раз в неделю."),
        ("Вы привозите и устанавливаете растения?", "Да. Привезём по Бишкеку, посадим в подходящие кашпо, расставим по помещению и оставим памятку по уходу для сотрудников."),
        ("Что делать, если растение погибнет?", "Даём консультации по уходу в WhatsApp бесплатно. Если растение болеет — напишите нам фото, подскажем, как спасти, или подберём замену."),
    ]
    office_plants = [x for x in C.P(C.PRODUCTS["krupnye"])]
    schema = [
        breadcrumb_schema([("Главная", "index.html"), ("Озеленение офисов", None)]),
        {"@context": "https://schema.org", "@type": "Service",
         "name": "Озеленение офисов в Бишкеке", "serviceType": "Озеленение помещений",
         "provider": {"@type": "Florist", "name": "Tamyr", "telephone": PHONE,
                      "address": {"@type": "PostalAddress", "addressLocality": "Бишкек", "addressCountry": "KG"}},
         "areaServed": {"@type": "City", "name": "Бишкек"},
         "description": desc},
        faq_schema(qa),
    ]
    b = head(title, desc, path, kw, schema)
    b += header("krupnye-rasteniya.html")
    b += crumbs([("Главная", "index.html"), ("Озеленение офисов", None)])
    cards = product_cards(office_plants)
    b += f"""
<main id="top">
  <div class="wrap">
  <section class="section reveal" style="margin-top:26px">
    <p class="eyebrow">Услуга · Бишкек</p>
    <h1>Озеленение офисов в Бишкеке</h1>
    <p class="lead">Подберём растения под освещение вашего офиса, кафе или салона, привезём, посадим в кашпо и расставим. Живые растения снижают стресс, глушат шум и делают пространство, куда приятно приходить — и сотрудникам, и клиентам.</p>
  </section>

  <section class="section seo-prose reveal">
    <header class="sec-head"><p class="eyebrow">Как это работает</p><h2>Озеленение под ключ — 4 шага</h2></header>
    <p><strong>1. Вы присылаете фото помещения</strong> в WhatsApp — достаточно пары кадров с окнами. <strong>2. Мы подбираем растения</strong> под ваше освещение и бюджет: от пары акцентных крупномеров до полного озеленения зала. <strong>3. Привозим и устанавливаем</strong>: растения уже в кашпо, с дренажом и подходящим грунтом. <strong>4. Оставляем памятку по уходу</strong> и остаёмся на связи — если что-то пойдёт не так, подскажем, как исправить.</p>
    <p>Работаем с офисами, кафе, салонами красоты, клиниками и коворкингами по всему Бишкеку. Для бизнеса возможна оплата по счёту.</p>
  </section>

  <section class="section reveal">
    <header class="sec-head"><p class="eyebrow">Каталог</p><h2>Растения, которые живут в офисе</h2></header>
    <div class="catalog">
{cards}
    </div>
    <article class="tile tile-faq reveal" style="margin-top:18px">
      <h3>Не нашли растение, которое искали?</h3>
      <p>Не проблема: в наличии больше, чем на сайте — каталог ещё пополняется. <a href="{wa_link('Здравствуйте! Ищу растение для офиса, которого нет на сайте — подскажите, есть ли в наличии 🌿')}" target="_blank" rel="noopener">Напишите в WhatsApp</a>, что нужно — найдём и привезём под заказ.</p>
    </article>
    <p style="margin-top:1rem"><a href="krupnye-rasteniya.html">Смотреть все крупные и офисные растения →</a></p>
  </section>

  <section class="section seo-prose reveal">
    <header class="sec-head"><p class="eyebrow">Почему это работает</p><h2>Зачем офису живые растения</h2></header>
    <p>Крупные растения зонируют open-space без перегородок, приглушают эхо и увлажняют воздух, пересушенный кондиционерами. Для приёмной и переговорной подойдут эффектные <a href="p/fikus-lirovidnyy.html">фикус лировидный</a> и <a href="p/monstera-krupnaya.html">монстера</a>, для рабочих зон — неубиваемые <a href="p/zamiokulkas.html">замиокулькас</a> и <a href="p/sansevieriya-teschin-yazyk.html">сансевиерия</a>, которым хватает полива раз в неделю силами офис-менеджера. К растениям сразу подберём <a href="gorshki-kashpo.html">напольные кашпо</a> в цвет интерьера и <a href="grunt-dlya-rasteniy.html">правильный грунт</a>.</p>
  </section>

  <section id="faq" class="section">
    <header class="sec-head reveal"><p class="eyebrow">Частые вопросы</p><h2>Вопросы и ответы</h2></header>
    <div class="bento faq-bento">
"""
    for q, a in qa:
        b += f'      <article class="tile tile-faq reveal"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></article>\n'
    b += "    </div>\n  </section>\n"
    b += _cta_strip("Посчитаем смету бесплатно",
                    "Пришлите фото помещения — предложим варианты озеленения под ваш бюджет в тот же день.",
                    "Здравствуйте! Интересует озеленение офиса — посчитайте, пожалуйста, смету 🌿")
    b += "\n  </div>\n"
    b += footer()
    write(path, b)

def build_gift_landing():
    path = "rasteniya-v-podarok.html"
    title = "Растение в подарок в Бишкеке — живой подарок с доставкой | Tamyr"
    desc = ("Живое растение в подарок с доставкой по Бишкеку: орхидеи, антуриумы, фиалки и стильные крупномеры. "
            "Подберём под повод и бюджет, добавим кашпо и открытку. Заказ в WhatsApp — привезём в тот же день.")
    kw = "растение в подарок бишкек, цветы в подарок бишкек, орхидея в подарок, живой подарок, что подарить бишкек"
    qa = [
        ("Чем растение в горшке лучше букета?", "Букет живёт неделю, растение — годы и каждый день напоминает о дарителе. По цене сопоставимо: цветущая орхидея или антуриум стоят как средний букет, а радуют месяцами."),
        ("Успеете доставить сегодня?", "Обычно да: напишите в WhatsApp до обеда — привезём в тот же день по Бишкеку. Уточним наличие, пришлём фото конкретного растения перед доставкой."),
        ("Поможете выбрать, если я не разбираюсь?", "Конечно. Скажите повод, бюджет и пару слов о человеке — предложим 2–3 варианта с фото. Добавим красивое кашпо и открытку с вашим текстом."),
        ("А если получатель не умеет ухаживать за растениями?", "Подарим памятку по уходу и подберём неприхотливый вариант: замиокулькас, сансевиерию или каланхоэ сложно погубить даже новичку."),
    ]
    gift_plants = [x for x in C.P(C.PRODUCTS["tsvety"])]
    schema = [
        breadcrumb_schema([("Главная", "index.html"), ("Растение в подарок", None)]),
        itemlist_schema(gift_plants, BASE + "/" + path),
        faq_schema(qa),
    ]
    b = head(title, desc, path, kw, schema)
    b += header("tsvety.html")
    b += crumbs([("Главная", "index.html"), ("Растение в подарок", None)])
    cards = product_cards(gift_plants)
    b += f"""
<main id="top">
  <div class="wrap">
  <section class="section reveal" style="margin-top:26px">
    <p class="eyebrow">Подарки · Бишкек</p>
    <h1>Растение в подарок в Бишкеке</h1>
    <p class="lead">Живой подарок вместо букета: цветущие орхидеи, антуриумы и фиалки, стильные крупномеры для дома и офиса. Подберём под повод и бюджет, упакуем в красивое кашпо, привезём по Бишкеку — можно с открыткой от вашего имени.</p>
  </section>

  <section class="section seo-prose reveal">
    <header class="sec-head"><p class="eyebrow">По поводу</p><h2>Что подарить</h2></header>
    <p><strong>Девушке или маме</strong> — цветущую <a href="p/orhideya-falenopsis.html">орхидею фаленопсис</a> или нежную <a href="p/senpoliya-fialka.html">фиалку</a>. <strong>Мужчине</strong> — <a href="p/anturium.html">антуриум</a> («мужское счастье») или строгий <a href="p/zamiokulkas.html">замиокулькас</a>. <strong>Коллеге на день рождения</strong> — неприхотливый <a href="p/kalanhoe.html">каланхоэ</a> или <a href="p/spatifillum.html">спатифиллум</a>. <strong>На новоселье</strong> — эффектную <a href="p/monstera-krupnaya.html">монстеру</a> или <a href="p/fikus-lirovidnyy.html">фикус лировидный</a>, которые станут центром интерьера. <strong>Офису от партнёров</strong> — крупное растение в напольном кашпо: смотрите <a href="ozelenenie-ofisov.html">озеленение офисов</a>.</p>
  </section>

  <section class="section reveal">
    <header class="sec-head"><p class="eyebrow">Каталог</p><h2>Цветущие растения в подарок</h2></header>
    <div class="catalog">
{cards}
    </div>
    <article class="tile tile-faq reveal" style="margin-top:18px">
      <h3>Не нашли цветок, который хотели подарить?</h3>
      <p>Не проблема: в наличии больше, чем на сайте — каталог ещё пополняется. <a href="{wa_link('Здравствуйте! Хочу растение в подарок, которого нет на сайте — подскажите, сможете найти? 🎁🌿')}" target="_blank" rel="noopener">Напишите в WhatsApp</a> — найдём и привезём под заказ, с кашпо и открыткой.</p>
    </article>
    <p style="margin-top:1rem"><a href="tsvety.html">Смотреть все цветущие растения →</a></p>
  </section>

  <section id="faq" class="section">
    <header class="sec-head reveal"><p class="eyebrow">Частые вопросы</p><h2>Вопросы и ответы</h2></header>
    <div class="bento faq-bento">
"""
    for q, a in qa:
        b += f'      <article class="tile tile-faq reveal"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></article>\n'
    b += "    </div>\n  </section>\n"
    b += _cta_strip("Подберём подарок за 5 минут",
                    "Напишите повод и бюджет — пришлём варианты с фото. Доставим по Бишкеку в тот же день.",
                    "Здравствуйте! Хочу растение в подарок — помогите выбрать 🎁🌿")
    b += "\n  </div>\n"
    b += footer()
    write(path, b)

build_office_landing()
build_gift_landing()

# 404 для Vercel (отдаётся автоматически, снижает потери трафика)
def build_404():
    schema = [breadcrumb_schema([("Главная", "index.html")])]
    b = head("Страница не найдена — Tamyr, Бишкек", "Страница не найдена. Перейдите в каталог растений, цветов, горшков и грунтов магазина Tamyr в Бишкеке.", "404.html", "tamyr бишкек", schema)
    b = b.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">')
    b += header()
    b += """
<main id="top"><div class="wrap">
  <section class="section reveal" style="margin-top:26px;text-align:center">
    <p class="eyebrow">Ошибка 404</p>
    <h1>Такой страницы нет</h1>
    <p class="lead">Зато есть живые растения. Загляните в каталог:</p>
    <div class="cat-pills" style="justify-content:center;margin-top:1.2rem">
      <a class="cat-pill" href="komnatnye-rasteniya.html">🪴 Комнатные растения</a>
      <a class="cat-pill" href="krupnye-rasteniya.html">🌳 Крупные и офисные</a>
      <a class="cat-pill" href="tsvety.html">🌸 Цветы</a>
      <a class="cat-pill" href="gorshki-kashpo.html">🏺 Горшки и кашпо</a>
      <a class="cat-pill" href="grunt-dlya-rasteniy.html">🪨 Грунты</a>
    </div>
  </section>
</div>
"""
    b += footer()
    write("404.html", b)

build_404()

# Ключ IndexNow — мгновенная индексация в Яндексе (яндекс поддерживает IndexNow)
write(INDEXNOW_KEY + ".txt", INDEXNOW_KEY)

def rebuild_sitemap():
    urls = [("index.html", "1.0", "weekly"),
            ("komnatnye-rasteniya.html", "0.9", "weekly"),
            ("krupnye-rasteniya.html", "0.9", "weekly"),
            ("tsvety.html", "0.9", "weekly"),
            ("gorshki-kashpo.html", "0.8", "weekly"),
            ("grunt-dlya-rasteniy.html", "0.8", "weekly"),
            ("ozelenenie-ofisov.html", "0.9", "weekly"),
            ("rasteniya-v-podarok.html", "0.9", "weekly"),
            ("dostavka-i-oplata.html", "0.6", "monthly"),
            ("kontakty.html", "0.7", "monthly"),
            ("blog.html", "0.6", "weekly")]
    urls += [(u, "0.7", "monthly") for u in PRODUCT_URLS]
    urls += [("blog/uhod-za-komnatnymi-rasteniyami.html", "0.5", "monthly"),
             ("blog/neprihotlivye-komnatnye-rasteniya.html", "0.5", "monthly"),
             ("blog/kak-vybrat-gorshok-i-kashpo.html", "0.5", "monthly"),
             ("blog/kakoy-grunt-vybrat.html", "0.5", "monthly"),
             ("blog/gde-kupit-komnatnye-rasteniya-v-bishkeke.html", "0.6", "monthly"),
             ("blog/rasteniya-dlya-ofisa.html", "0.6", "monthly"),
             ("blog/kakoe-rastenie-podarit.html", "0.6", "monthly"),
             ("blog/rasteniya-dlya-spalni.html", "0.5", "monthly")]
    items = ""
    for u, pr, cf in urls:
        loc = BASE + "/" if u == "index.html" else BASE + "/" + u
        items += (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                  f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{items}</urlset>\n")
    write("sitemap.xml", sitemap)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

rebuild_sitemap()
print(f"\nИтого товарных страниц: {len(PRODUCT_URLS)}")
