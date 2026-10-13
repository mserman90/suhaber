"""
app/livestock_scraper.py
Hayvancılık, Süt ve Et Endüstrisi, Yem, Hayvan Sağlığı, Veterinerlik ve Akıllı Hayvancılık Teknolojileri Haberleri Tarayıcısı.
1. Türkiye Ulusal ve Sektörel Basını (Google News RSS - Türkiye Hayvancılık Gündemi).
2. Küresel Hayvancılık ve Akıllı Çiftlik Teknolojileri (Livestock Tech, Süt Sağım Robotları, Hassas Besleme).
3. Hakemli Akademik Zootekni ve Veterinerlik Yayınları (Google Dorking - ScienceDirect, MDPI Animals, Frontiers in Veterinary Science, DergiPark vb.).
"""

import re
import html
import logging
import urllib.parse
import email.utils
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("livestock_scraper")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}


def clean_livestock_title(raw_title: str) -> Tuple[str, str]:
    """Başlıktan yayıncı eklerini temizler ve (temiz_başlık, yayıncı) döndürür."""
    title = raw_title.strip()
    publisher = ""
    if " - " in title:
        parts = title.rsplit(" - ", 1)
        title = parts[0].strip()
        publisher = parts[1].strip()
    elif " | " in title:
        parts = title.rsplit(" | ", 1)
        title = parts[0].strip()
        publisher = parts[1].strip()
    return title, publisher


def scrape_turkey_livestock_news(limit: int = 30) -> List[Dict[str, Any]]:
    """
    Türkiye ulusal ve sektörel basınından güncel hayvancılık, süt üretimi,
    kırmızı et sektörü, besicilik, yem fiyatları, küçükbaş/büyükbaş ve hayvan sağlığı haberlerini çeker.
    """
    import xml.etree.ElementTree as ET

    query = (
        'hayvancılık OR besicilik OR "süt üreticileri" OR "çiğ süt" OR '
        '"kırmızı et" OR küçükbaş OR büyükbaş OR "yem fiyatları" OR '
        '"et ve süt kurumu" OR kanatlı OR veteriner OR damızlık'
    )
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=tr&gl=TR&ceid=TR:tr"

    items: List[Dict[str, Any]] = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            now_dt = datetime.now(timezone.utc)

            for it in root.findall(".//item"):
                if len(items) >= limit:
                    break

                raw_title = it.find("title").text if it.find("title") is not None else ""
                link = it.find("link").text if it.find("link") is not None else ""
                pub_str = it.find("pubDate").text if it.find("pubDate") is not None else ""
                guid = it.find("guid").text if it.find("guid") is not None else link
                source_el = it.find("source")
                source_name = source_el.text if source_el is not None else "Türkiye Hayvancılık Bülteni"

                # Sosyal medya ve alakasız platformları filtrele
                combined_src = (link + " " + source_name).lower()
                if any(bad in combined_src for bad in [
                    "instagram.com", "youtube.com", "tiktok.com", "facebook.com",
                    "twitter.com", "x.com", "linkedin.com", "pinterest.com"
                ]):
                    continue

                clean_title, pub_from_title = clean_livestock_title(raw_title)
                if pub_from_title and source_name == "Türkiye Hayvancılık Bülteni":
                    source_name = pub_from_title

                pub_ts = int(now_dt.timestamp())
                pub_rfc = email.utils.format_datetime(now_dt)
                if pub_str:
                    try:
                        dt_parsed = email.utils.parsedate_to_datetime(pub_str)
                        pub_ts = int(dt_parsed.timestamp())
                        pub_rfc = email.utils.format_datetime(dt_parsed)
                    except Exception:
                        pass

                desc_el = it.find("description")
                raw_desc = desc_el.text if desc_el is not None else ""
                clean_desc = BeautifulSoup(raw_desc, "html.parser").get_text(" ", strip=True) if raw_desc else clean_title

                # Kategori ataması
                tl = clean_title.lower()
                if any(k in tl for k in ["süt", "sağım", "mandıra"]):
                    category = "Süt & Mandıra"
                elif any(k in tl for k in ["et", "besi", "karkas", "kırmızı et", "kesim"]):
                    category = "Besi & Kırmızı Et"
                elif any(k in tl for k in ["yem", "silaj", "arpa", "küspe", "saman"]):
                    category = "Yem & Besleme"
                elif any(k in tl for k in ["küçükbaş", "koyun", "keçi", "mera"]):
                    category = "Küçükbaş Hayvancılık"
                elif any(k in tl for k in ["aşı", "hastalık", "şap", "veteriner", "sağlık", "salgın"]):
                    category = "Hayvan Sağlığı & Biyogüvenlik"
                elif any(k in tl for k in ["tavuk", "kanatlı", "yumurta", "broyler"]):
                    category = "Kanatlı Sektörü"
                elif any(k in tl for k in ["robot", "sensör", "otomasyon", "akıllı"]):
                    category = "Hayvancılık Teknolojileri"
                elif any(k in tl for k in ["destek", "hibe", "fiyat", "et ve süt kurumu", "prim"]):
                    category = "Destek & Fiyat Politikaları"
                else:
                    category = "Hayvancılık & Besicilik"

                items.append({
                    "guid": f"tr_livestock:{guid}",
                    "title": clean_title,
                    "title_tr": clean_title,
                    "link": link,
                    "author": source_name,
                    "source_feed": f"🇹🇷 {source_name}",
                    "description": clean_desc,
                    "summary_tr": clean_desc,
                    "category_tr": category,
                    "is_turkey": 1,
                    "is_academic": 0,
                    "channel": "livestock",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
    except Exception as e:
        logger.warning("Turkey livestock scrape failed: %s", e)

    return items


def scrape_global_livestock_tech_news(limit: int = 25) -> List[Dict[str, Any]]:
    """
    Dünyadan akıllı hayvancılık, hassas hayvancılık (precision livestock farming),
    otomatik sağım sistemleri, sürü yönetim yazılımları ve küresel et/süt piyasası haberlerini tarar.
    """
    import xml.etree.ElementTree as ET

    queries = [
        '("precision livestock" OR "dairy robotics" OR "milking robot" OR "smart cattle") when:60d',
        '("livestock farming" OR "poultry technology" OR "animal genetics" OR "dairy farming tech") when:60d',
    ]

    items: List[Dict[str, Any]] = []
    seen_guids = set()
    now_dt = datetime.now(timezone.utc)

    for q in queries:
        if len(items) >= limit:
            break
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=en-US&gl=US&ceid=US:en"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                continue
            root = ET.fromstring(resp.text)

            for it in root.findall(".//item"):
                if len(items) >= limit:
                    break

                raw_title = it.find("title").text if it.find("title") is not None else ""
                link = it.find("link").text if it.find("link") is not None else ""
                pub_str = it.find("pubDate").text if it.find("pubDate") is not None else ""
                guid = it.find("guid").text if it.find("guid") is not None else link
                source_el = it.find("source")
                source_name = source_el.text if source_el is not None else "Global Livestock Intelligence"

                clean_title, pub_from_title = clean_livestock_title(raw_title)
                if pub_from_title and source_name == "Global Livestock Intelligence":
                    source_name = pub_from_title

                if clean_title in seen_guids:
                    continue
                seen_guids.add(clean_title)

                pub_ts = int(now_dt.timestamp())
                pub_rfc = email.utils.format_datetime(now_dt)
                if pub_str:
                    try:
                        dt_parsed = email.utils.parsedate_to_datetime(pub_str)
                        pub_ts = int(dt_parsed.timestamp())
                        pub_rfc = email.utils.format_datetime(dt_parsed)
                    except Exception:
                        pass

                desc_el = it.find("description")
                raw_desc = desc_el.text if desc_el is not None else ""
                clean_desc = BeautifulSoup(raw_desc, "html.parser").get_text(" ", strip=True) if raw_desc else clean_title

                items.append({
                    "guid": f"global_livestock:{guid}",
                    "title": clean_title,
                    "title_tr": "",
                    "link": link,
                    "author": source_name,
                    "source_feed": f"🌍 {source_name}",
                    "description": clean_desc,
                    "summary_tr": "",
                    "category_tr": "Hayvancılık Teknolojileri",
                    "is_turkey": 0,
                    "is_academic": 0,
                    "channel": "livestock",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
        except Exception as e:
            logger.warning("Global livestock scrape failed for query [%s]: %s", q, e)

    return items


def scrape_academic_livestock_publications(limit_per_query: int = 10, max_total: int = 35) -> List[Dict[str, Any]]:
    """
    Hakemli akademik zootekni, hayvan besleme, sürü sağlığı ve veterinerlik yayınlarını
    ScienceDirect, MDPI Animals, Frontiers in Veterinary Science ve DergiPark üzerinden tarar.
    """
    import xml.etree.ElementTree as ET

    dork_queries = [
        # 1. ScienceDirect / Elsevier - Animal Science & Veterinary
        ('site:sciencedirect.com/science/article ("livestock" OR "dairy cows" OR "animal nutrition" OR "precision livestock") when:90d', 'en-US', 'US', 'US:en', 'ScienceDirect (Elsevier)'),
        # 2. MDPI Animals
        ('site:mdpi.com/journal/animals ("livestock" OR "ruminant" OR "poultry" OR "dairy") when:90d', 'en-US', 'US', 'US:en', 'MDPI Animals'),
        # 3. Frontiers in Veterinary Science & Animal Science
        ('(site:frontiersin.org/articles/ "veterinary" OR "animal science") when:90d', 'en-US', 'US', 'US:en', 'Frontiers in Veterinary Science'),
        # 4. DergiPark - Türkiye Akademik Veterinerlik ve Zootekni Dergileri
        ('(site:dergipark.org.tr/tr/pub/*/article OR site:dergipark.org.tr "veteriner fakültesi" OR "zootekni") when:120d', 'tr', 'TR', 'TR:tr', 'DergiPark (TÜBİTAK ULAKBİM)'),
    ]

    items: List[Dict[str, Any]] = []
    seen_titles = set()
    now_dt = datetime.now(timezone.utc)

    for query, hl, gl, ceid, default_pub in dork_queries:
        if len(items) >= max_total:
            break

        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl={hl}&gl={gl}&ceid={ceid}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                continue

            root = ET.fromstring(resp.text)
            query_count = 0
            for it in root.findall(".//item"):
                if query_count >= limit_per_query or len(items) >= max_total:
                    break

                raw_title = it.find("title").text if it.find("title") is not None else ""
                link = it.find("link").text if it.find("link") is not None else ""
                pub_str = it.find("pubDate").text if it.find("pubDate") is not None else ""
                guid = it.find("guid").text if it.find("guid") is not None else link

                src_elem = it.find("source")
                src_text = src_elem.text if src_elem is not None else default_pub

                clean_title, extracted_pub = clean_livestock_title(raw_title)
                publisher = extracted_pub or src_text or default_pub

                t_lower = clean_title.lower()
                if any(bad in t_lower for bad in [
                    "user profile", "editorial board", "author guidelines",
                    "aims and scope", "call for papers", "privacy policy"
                ]):
                    continue

                if len(clean_title) < 16:
                    continue

                norm_key = re.sub(r'[^a-zA-Z0-9çğıöşüÇĞİÖŞÜ]', '', t_lower)
                if norm_key in seen_titles:
                    continue
                seen_titles.add(norm_key)

                pub_ts = int(now_dt.timestamp())
                pub_rfc = email.utils.format_datetime(now_dt)
                if pub_str:
                    try:
                        dt_parsed = email.utils.parsedate_to_datetime(pub_str)
                        pub_ts = int(dt_parsed.timestamp())
                        pub_rfc = email.utils.format_datetime(dt_parsed)
                    except Exception:
                        pass

                desc_el = it.find("description")
                raw_desc = desc_el.text if desc_el is not None else ""
                clean_desc = BeautifulSoup(raw_desc, "html.parser").get_text(" ", strip=True) if raw_desc else clean_title

                is_turkey_academic = bool("dergipark" in publisher.lower() or ".edu.tr" in publisher.lower() or "türkiye" in clean_title.lower())

                items.append({
                    "guid": f"academic_livestock:{guid}",
                    "title": clean_title,
                    "title_tr": clean_title if is_turkey_academic else "",
                    "link": link,
                    "author": publisher,
                    "source_feed": f"🎓 {publisher}",
                    "description": clean_desc,
                    "summary_tr": clean_desc if is_turkey_academic else "",
                    "category_tr": "Akademik Yayınlar",
                    "is_turkey": 1 if is_turkey_academic else 0,
                    "is_academic": 1,
                    "channel": "livestock",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
                query_count += 1
        except Exception as e:
            logger.warning("Academic livestock scrape failed for query [%s]: %s", query, e)

    return items
