#!/usr/bin/env python3
"""
export_static.py
Inoreader akışını ve açık veri kaynaklarını tarayıp 'dist/' dizinine:
- Türkçe gazete temalı 'Su Haber Bülteni' web portalını (dist/index.html)
- Türkçe gazete temalı 'Tarım Haber Bülteni' web portalını (dist/tarim.html)
- Su bülteni beslemeleri: dist/rss.xml, dist/atom.xml, dist/feed.json
- Tarım bülteni beslemeleri: dist/rss_tarim.xml, dist/atom_tarim.xml, dist/feed_tarim.json
dosyalarını üretir.
"""

import os
import sys
import json
import html
import re
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import config
from app.storage import Storage
from app.scraper import scrape_inoreader, scrape_turkey_water_news, scrape_academic_water_publications
from app.agriculture_scraper import (
    scrape_turkey_agriculture_news,
    scrape_global_agritech_news,
    scrape_academic_agriculture_publications
)
from app.feed import generate_rss_2_xml, generate_atom_xml, generate_json_feed
from app.translator import (
    batch_translate_articles,
    categorize_article,
    categorize_agriculture_article,
    translate_to_turkish,
    generate_turkish_editorial_summary,
    generate_agriculture_editorial_summary,
    is_genuinely_turkish
)
from app.image_enricher import resolve_article_image
from app.portal import generate_newspaper_portal_html

TURKEY_WATER_PAT = re.compile(
    r"\b(türkiye|turkey|türk su|türkiye'de|dsi|devlet su işleri|barajı|barajları|baraj doluluk|iski|aski|izsu|gap projesi|güneydoğu anadolu|fırat nehri|dicle nehri|kızılırmak|yeşilırmak|meriç nehri|gediz nehri|büyük menderes|küçük menderes|sakarya nehri|van gölü|tuz gölü|beyşehir gölü|eğirdir gölü|atatürk barajı|keban barajı|karakaya barajı|su verimliliği seferberliği)\b",
    re.IGNORECASE
)
FOREIGN_WATER_PAT = re.compile(
    r"\b(colorado|utah|california|arizona|nevada|mississippi|salt lake|texas|australia|murray-darling|yangtze|yellow river|mekong|ganges|indus|danube|rhine)\b",
    re.IGNORECASE
)

TURKEY_AGRI_PAT = re.compile(
    r"\b(türkiye|türk tarım|çiftçi|üretici|tmo|toprak mahsulleri|tarım kredi|tzob|çukurova|harran|konya ovası|bafra|çarşamba|gediz|menderes|buğday|arpa|mısır|ayçiçeği|pamuk|zeytin|fındık|çeltik|seracılık|antalya|mersin|adana|ege|anadolu|gübre|tohum|mazot desteği|çiğ süt|büyükbaş|küçükbaş)\b",
    re.IGNORECASE
)
FOREIGN_AGRI_PAT = re.compile(
    r"\b(colorado|california|texas|brazil|iowa|nebraska|kansas|australia|midwest)\b",
    re.IGNORECASE
)

def format_feed_items(items, channel="water"):
    rss_items = []
    default_cat = "Bitkisel Üretim" if channel == "agriculture" else "Su Kaynakları"
    for it in items:
        r_item = dict(it)
        title_tr = it.get("title_tr") or it["title"]
        category_tr = it.get("category_tr", default_cat)
        r_item["title"] = f"[{category_tr}] {title_tr}"

        desc_parts = []
        if it.get("image_url"):
            desc_parts.append(f'<p><img src="{html.escape(it["image_url"])}" alt="{html.escape(title_tr)}" style="max-width:100%; border-radius:6px;" /></p>')
        if it.get("category_tr"):
            desc_parts.append(f'<p><strong>Kategori:</strong> {html.escape(category_tr)}</p>')
        if it.get("source_feed"):
            desc_parts.append(f'<p><strong>Kaynak:</strong> {html.escape(it["source_feed"])}</p>')
        if it.get("title") and it.get("title") != title_tr:
            desc_parts.append(f'<p><strong>Orijinal Başlık:</strong> {html.escape(it["title"])}</p>')
        if it.get("summary_tr"):
            desc_parts.append(f'<p>{html.escape(it["summary_tr"])}</p>')
        desc_parts.append(f'<p><a href="{html.escape(it["link"])}" target="_blank" rel="noopener noreferrer">Makalenin Tamamını Oku &rarr;</a></p>')

        r_item["description"] = "\n".join(desc_parts)
        rss_items.append(r_item)
    return rss_items

def main():
    dist_dir = Path(os.getenv("DIST_DIR", config.BASE_DIR / "dist"))
    dist_dir.mkdir(parents=True, exist_ok=True)

    storage = Storage(config.DB_PATH)

    # ==========================================
    # 1. SU HABERLERİ TARAMA (WATER CHANNEL)
    # ==========================================
    print(f"[*] Inoreader akışı kontrol ediliyor: {config.INOREADER_URL}")
    data = scrape_inoreader(config.INOREADER_URL)
    raw_water_items = data.get("items", [])
    print(f"[+] Çekilen güncel makale sayısı: {len(raw_water_items)}")

    print("[*] Türkiye su haberleri taranıyor...")
    turkey_water_items = scrape_turkey_water_news(limit=25)
    print(f"[+] Çekilen güncel Türkiye su haberi sayısı: {len(turkey_water_items)}")

    print("[*] Yeni yayınlanan su yönetimi akademik yayınları Google Dorking ile taranıyor...")
    academic_water_items = scrape_academic_water_publications(limit_per_query=12, max_total=40)
    print(f"[+] Çekilen güncel akademik su yayını sayısı: {len(academic_water_items)}")

    print("[*] Güncel basın haber takibi kontrol ediliyor...")
    try:
        from app.sygm_scraper import scrape_sygm_daily_report
        sygm_items = scrape_sygm_daily_report()
        print(f"[+] Çekilen güncel ulusal basın haberi sayısı: {len(sygm_items)}")
    except Exception as sygm_err:
        print(f"[!] Basın haber takibi tarama hatası: {sygm_err}")
        sygm_items = []

    storage.save_items(raw_water_items, default_channel="water")
    storage.save_items(turkey_water_items, default_channel="water")
    storage.save_items(academic_water_items, default_channel="water")
    storage.save_items(sygm_items, default_channel="water")

    # ==========================================
    # 2. TARIM HABERLERİ TARAMA (AGRICULTURE CHANNEL)
    # ==========================================
    print("[*] Türkiye tarım haberleri taranıyor...")
    turkey_agri_items = scrape_turkey_agriculture_news(limit=25)
    print(f"[+] Çekilen güncel Türkiye tarım haberi sayısı: {len(turkey_agri_items)}")

    print("[*] Küresel akıllı tarım ve tarım teknolojileri haberleri taranıyor...")
    global_agri_items = scrape_global_agritech_news(limit=20)
    print(f"[+] Çekilen küresel agritech haber sayısı: {len(global_agri_items)}")

    print("[*] Yeni yayınlanan hakemli tarım & agronomi akademik yayınları taranıyor...")
    academic_agri_items = scrape_academic_agriculture_publications(limit_per_query=10, max_total=30)
    print(f"[+] Çekilen güncel akademik tarım yayını sayısı: {len(academic_agri_items)}")

    storage.save_items(turkey_agri_items, default_channel="agriculture")
    storage.save_items(global_agri_items, default_channel="agriculture")
    storage.save_items(academic_agri_items, default_channel="agriculture")

    # Veritabanı temizliği
    storage.prune_items(config.MAX_STORED_ITEMS)

    # ==========================================
    # 3. SU KANALINI İŞLEME (WATER ITEMS)
    # ==========================================
    water_items = storage.get_items(limit=200, channel="water")
    print(f"[+] Su kanalı toplam veritabanı kaydı: {len(water_items)}")
    water_items = batch_translate_articles(water_items)

    for idx, it in enumerate(water_items):
        title_tr = it.get("title_tr")
        if not title_tr or not is_genuinely_turkish(title_tr):
            title_tr = translate_to_turkish(it["title"])
        it["title_tr"] = title_tr

        source = it.get("source_feed") or ""
        desc = it.get("description") or ""
        full_text = title_tr + " " + it.get("title", "") + " " + desc + " " + source

        is_academic = 1 if (it.get("is_academic") or it.get("guid", "").startswith("academic:") or "🎓" in source) else 0
        it["is_academic"] = is_academic

        is_tr_scraped = bool(it.get("guid", "").startswith("tr_water:") or it.get("guid", "").startswith("sygm:") or "🇹🇷" in source)
        is_tr_match = bool(TURKEY_WATER_PAT.search(full_text) and not FOREIGN_WATER_PAT.search(full_text))
        is_turkey = 1 if (is_tr_scraped or is_tr_match) else 0
        it["is_turkey"] = is_turkey

        category_tr = it.get("category_tr")
        if is_turkey:
            category_tr = "Türkiye"
        elif not category_tr or category_tr == "Türkiye":
            category_tr = categorize_article(title_tr + " " + it["title"], desc)
        it["category_tr"] = category_tr

        summary_tr = it.get("summary_tr")
        if not summary_tr or not is_genuinely_turkish(summary_tr):
            summary_tr = generate_turkish_editorial_summary(title_tr, category_tr, source, "")
        it["summary_tr"] = summary_tr

        storage.update_item_translation(
            it["guid"],
            title_tr,
            summary_tr,
            category_tr,
            is_turkey,
            is_academic,
            channel="water"
        )
        resolved_img = resolve_article_image(it, idx, channel="water")
        it["image_url"] = resolved_img
        storage.update_item_image(it["guid"], resolved_img)

    now_ts = int(datetime.now(timezone.utc).timestamp())

    def turkey_water_headline_sort_key(x):
        guid = x.get("guid", "")
        source = x.get("source_feed", "")
        title = (x.get("title_tr", "") + " " + x.get("title", "")).lower()

        if any(bad in title for bad in ["colorado", "utah", "california", "arizona", "nevada", "mississippi", "salt lake"]):
            return (-999999999, 0)

        is_tr = bool(
            guid.startswith("tr_water:")
            or guid.startswith("sygm:")
            or "🇹🇷" in source
            or x.get("is_turkey")
            or x.get("category_tr") == "Türkiye"
        )
        if not is_tr:
            return (-999999999, 0)

        pub_ts = int(x.get("pub_date_ts") or 0)
        age_days = max(0.0, (now_ts - pub_ts) / 86400.0) if pub_ts > 0 else 5.0

        quality = 1000.0
        if any(k in title for k in ["baraj", "doluluk", "sulama", "su yönetimi", "kuraklık", "dsi", "su krizi", "su verimliliği", "göl", "akarsu"]):
            quality += 300.0
        if any(k in title for k in ["kesinti", "ihale", "personel", "kadro", "voleybol", "futbol"]):
            quality -= 800.0

        final_score = quality - (age_days * 500.0)
        return (final_score, pub_ts)

    tr_water_candidates = [it for it in water_items if turkey_water_headline_sort_key(it)[0] > -500000]
    tr_water_sorted = sorted(tr_water_candidates, key=turkey_water_headline_sort_key, reverse=True)
    if tr_water_sorted:
        top_water_tr = tr_water_sorted[0]
        water_items = [top_water_tr] + [it for it in water_items if it.get("guid") != top_water_tr.get("guid")]
        print(f"[+] Su Manşeti belirlendi: {top_water_tr.get('title_tr')} (Tarih: {top_water_tr.get('pub_date')})")

    # ==========================================
    # 4. TARIM KANALINI İŞLEME (AGRICULTURE ITEMS)
    # ==========================================
    agri_items = storage.get_items(limit=200, channel="agriculture")
    print(f"[+] Tarım kanalı toplam veritabanı kaydı: {len(agri_items)}")
    agri_items = batch_translate_articles(agri_items)

    for idx, it in enumerate(agri_items):
        title_tr = it.get("title_tr")
        if not title_tr or not is_genuinely_turkish(title_tr):
            title_tr = translate_to_turkish(it["title"])
        it["title_tr"] = title_tr

        source = it.get("source_feed") or ""
        desc = it.get("description") or ""
        full_text = title_tr + " " + it.get("title", "") + " " + desc + " " + source

        is_academic = 1 if (it.get("is_academic") or it.get("guid", "").startswith("academic_agri:") or "🎓" in source) else 0
        it["is_academic"] = is_academic

        is_tr_scraped = bool(it.get("guid", "").startswith("tr_agri:") or "🇹🇷" in source or "🌾" in source)
        is_tr_match = bool(TURKEY_AGRI_PAT.search(full_text) and not FOREIGN_AGRI_PAT.search(full_text))
        is_turkey = 1 if (is_tr_scraped or is_tr_match) else 0
        it["is_turkey"] = is_turkey

        category_tr = it.get("category_tr")
        if is_turkey:
            category_tr = "Türkiye"
        elif not category_tr or category_tr == "Türkiye":
            category_tr = categorize_agriculture_article(title_tr + " " + it["title"], desc)
        it["category_tr"] = category_tr

        summary_tr = it.get("summary_tr")
        if not summary_tr or not is_genuinely_turkish(summary_tr):
            summary_tr = generate_agriculture_editorial_summary(title_tr, category_tr, source, "")
        it["summary_tr"] = summary_tr

        storage.update_item_translation(
            it["guid"],
            title_tr,
            summary_tr,
            category_tr,
            is_turkey,
            is_academic,
            channel="agriculture"
        )
        resolved_img = resolve_article_image(it, idx, channel="agriculture")
        it["image_url"] = resolved_img
        storage.update_item_image(it["guid"], resolved_img)

    def turkey_agri_headline_sort_key(x):
        guid = x.get("guid", "")
        source = x.get("source_feed", "")
        title = (x.get("title_tr", "") + " " + x.get("title", "")).lower()

        if any(bad in title for bad in ["colorado", "california", "texas", "brazil"]):
            return (-999999999, 0)

        is_tr = bool(
            guid.startswith("tr_agri:")
            or "🌾" in source
            or "🇹🇷" in source
            or x.get("is_turkey")
            or x.get("category_tr") == "Türkiye"
        )
        if not is_tr:
            return (-999999999, 0)

        pub_ts = int(x.get("pub_date_ts") or 0)
        age_days = max(0.0, (now_ts - pub_ts) / 86400.0) if pub_ts > 0 else 5.0

        quality = 1000.0
        if any(k in title for k in ["çiftçi", "hasat", "üretim", "tohum", "gübre", "destek", "buğday", "tarım"]):
            quality += 300.0
        if any(k in title for k in ["personel", "kadro", "voleybol", "futbol"]):
            quality -= 800.0

        final_score = quality - (age_days * 500.0)
        return (final_score, pub_ts)

    tr_agri_candidates = [it for it in agri_items if turkey_agri_headline_sort_key(it)[0] > -500000]
    tr_agri_sorted = sorted(tr_agri_candidates, key=turkey_agri_headline_sort_key, reverse=True)
    if tr_agri_sorted:
        top_agri_tr = tr_agri_sorted[0]
        agri_items = [top_agri_tr] + [it for it in agri_items if it.get("guid") != top_agri_tr.get("guid")]
        print(f"[+] Tarım Manşeti belirlendi: {top_agri_tr.get('title_tr')} (Tarih: {top_agri_tr.get('pub_date')})")

    # ==========================================
    # 5. DOSYA VE BESLEME ÜRETİMLERİ
    # ==========================================
    public_url = config.PUBLIC_BASE_URL or "https://mserman90.github.io/suhaberportali"
    now_str = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")

    # --- A) SU HABER BÜLTENİ BESLEMELERİ & PORTALI ---
    rss_water_self = f"{public_url}/rss.xml"
    atom_water_self = f"{public_url}/atom.xml"
    json_water_self = f"{public_url}/feed.json"

    water_rss_items = format_feed_items(water_items, channel="water")

    # 1. Su RSS 2.0
    rss_content = generate_rss_2_xml(
        feed_title="Su Haber Bülteni - Su & Sulama Gazetesi",
        feed_description="Türkiye ve Dünya Su, Sulama, Çevre ve Hidroloji Araştırmaları Gazetesi",
        feed_link=public_url,
        self_rss_url=rss_water_self,
        items=water_rss_items,
        language="tr"
    )
    (dist_dir / "rss.xml").write_text(rss_content, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'rss.xml'}")

    # 2. Su Atom 1.0
    atom_content = generate_atom_xml(
        feed_title="Su Haber Bülteni",
        feed_description="Türkiye ve Dünya Su, Sulama, Çevre ve Hidroloji Araştırmaları Gazetesi",
        feed_link=public_url,
        self_atom_url=atom_water_self,
        items=water_rss_items
    )
    (dist_dir / "atom.xml").write_text(atom_content, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'atom.xml'}")

    # 3. Su JSON Feed
    json_data = generate_json_feed(
        feed_title="Su Haber Bülteni",
        feed_description="Türkiye ve Dünya Su, Sulama, Çevre ve Hidroloji Araştırmaları Gazetesi",
        feed_link=public_url,
        self_json_url=json_water_self,
        items=water_rss_items
    )
    (dist_dir / "feed.json").write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'feed.json'}")

    # 4. Su Portalı (index.html)
    portal_html = generate_newspaper_portal_html(
        water_items,
        now_str,
        rss_water_self,
        atom_water_self,
        json_water_self,
        channel="water",
        water_count=len(water_items),
        agri_count=len(agri_items)
    )
    (dist_dir / "index.html").write_text(portal_html, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'index.html'} ('Su Haber Bülteni' Modern Gazete Portalı)")

    # --- B) TARIM HABER BÜLTENİ BESLEMELERİ & PORTALI ---
    rss_agri_self = f"{public_url}/rss_tarim.xml"
    atom_agri_self = f"{public_url}/atom_tarim.xml"
    json_agri_self = f"{public_url}/feed_tarim.json"

    agri_rss_items = format_feed_items(agri_items, channel="agriculture")

    # 1. Tarım RSS 2.0
    rss_agri_content = generate_rss_2_xml(
        feed_title="Tarım Haber Bülteni - Tarım & Bitkisel Üretim Gazetesi",
        feed_description="Türkiye ve Dünya Tarım, Hayvancılık, Bitkisel Üretim ve Akıllı Tarım Gazetesi",
        feed_link=f"{public_url}/tarim.html",
        self_rss_url=rss_agri_self,
        items=agri_rss_items,
        language="tr"
    )
    (dist_dir / "rss_tarim.xml").write_text(rss_agri_content, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'rss_tarim.xml'}")

    # 2. Tarım Atom 1.0
    atom_agri_content = generate_atom_xml(
        feed_title="Tarım Haber Bülteni",
        feed_description="Türkiye ve Dünya Tarım, Hayvancılık, Bitkisel Üretim ve Akıllı Tarım Gazetesi",
        feed_link=f"{public_url}/tarim.html",
        self_atom_url=atom_agri_self,
        items=agri_rss_items
    )
    (dist_dir / "atom_tarim.xml").write_text(atom_agri_content, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'atom_tarim.xml'}")

    # 3. Tarım JSON Feed
    json_agri_data = generate_json_feed(
        feed_title="Tarım Haber Bülteni",
        feed_description="Türkiye ve Dünya Tarım, Hayvancılık, Bitkisel Üretim ve Akıllı Tarım Gazetesi",
        feed_link=f"{public_url}/tarim.html",
        self_json_url=json_agri_self,
        items=agri_rss_items
    )
    (dist_dir / "feed_tarim.json").write_text(json.dumps(json_agri_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'feed_tarim.json'}")

    # 4. Tarım Portalı (tarim.html)
    tarim_portal_html = generate_newspaper_portal_html(
        agri_items,
        now_str,
        rss_agri_self,
        atom_agri_self,
        json_agri_self,
        channel="agriculture",
        water_count=len(water_items),
        agri_count=len(agri_items)
    )
    (dist_dir / "tarim.html").write_text(tarim_portal_html, encoding="utf-8")
    print(f"[+] Üretildi: {dist_dir / 'tarim.html'} ('Tarım Haber Bülteni' Modern Gazete Portalı)")

    print("[*] Tüm çok kanallı gazete portalları ve yayın akışları başarıyla tamamlandı!")

if __name__ == "__main__":
    main()
