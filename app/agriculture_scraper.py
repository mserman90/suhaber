"""
app/agriculture_scraper.py
Tarım, Hayvancılık, Bitkisel Üretim ve Akıllı Tarım Teknolojileri Haberleri Tarayıcısı.
1. Türkiye Ulusal ve Yerel Basını (Google News RSS - Türkiye Tarım Gündemi).
2. Küresel Tarım ve Akıllı Tarım Teknolojileri (Agritech, Hassas Tarım).
3. Hakemli Akademik Ziraat ve Tarım Yayınları (Google Dorking - ScienceDirect, MDPI Agronomy, DergiPark vb.).
"""

import re
import html
import logging
import urllib.parse
import email.utils
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("agriculture_scraper")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}


def clean_agriculture_title(raw_title: str) -> Tuple[str, str]:
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


def scrape_turkey_agriculture_news(limit: int = 30) -> List[Dict[str, Any]]:
    """
    Türkiye ulusal ve sektörel basınından güncel bitkisel üretim, hasat,
    tohum, gübre, tarım teknolojileri ve tarımsal destek haberlerini çeker.
    (Hayvancılık haberleri Hayvancılık Gündemi kanalına aittir).
    """
    import xml.etree.ElementTree as ET

    query = (
        'tarımsal üretim OR "tarım teknolojileri" OR çiftçi OR hasat OR '
        'tohumculuk OR gübre OR "tarımsal destekler" OR seracılık OR '
        '"akıllı tarım" OR "bitkisel üretim" OR "tarla bitkileri"'
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
                source_name = source_el.text if source_el is not None else "Türkiye Tarım Bülteni"

                # Sosyal medya ve alakasız platformları filtrele
                combined_src = (link + " " + source_name).lower()
                if any(bad in combined_src for bad in [
                    "instagram.com", "youtube.com", "tiktok.com", "facebook.com",
                    "twitter.com", "x.com", "linkedin.com", "pinterest.com"
                ]):
                    continue

                clean_title, pub_from_title = clean_agriculture_title(raw_title)
                if pub_from_title and source_name == "Türkiye Tarım Bülteni":
                    source_name = pub_from_title

                # Hayvancılık haberlerini Tarım kanalına alma (Hayvancılık Gündemi'ne aittir)
                t_lower = clean_title.lower()
                livestock_terms = [
                    "büyükbaş", "küçükbaş", "çiğ süt", "süt üretici", "süt fiyat", 
                    "sağım robotu", "besi hayvan", "damızlık sığır", "damızlık koyun",
                    "kırmızı et", "şap hastalığı", "tavukçuluk", "arıcılık", "kümes hayvan"
                ]
                if any(t in t_lower for t in livestock_terms):
                    continue

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
                    "guid": f"tr_agri:{guid}",
                    "title": clean_title,
                    "title_tr": clean_title,
                    "link": link,
                    "author": source_name,
                    "source_feed": f"🌾 {source_name}",
                    "description": clean_desc,
                    "summary_tr": clean_desc,
                    "category_tr": "Bitkisel Üretim",
                    "is_turkey": 1,
                    "is_academic": 0,
                    "channel": "agriculture",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
    except Exception as e:
        logger.warning("Turkey agriculture news scrape failed: %s", e)

    return items


def scrape_global_agritech_news(limit: int = 25) -> List[Dict[str, Any]]:
    """
    Küresel akıllı tarım, hassas tarım, agritech ve gıda güvenliği haberlerini çeker.
    (Yabancı dildeki haberler translator modülü ile tam Türkçeleştirilir).
    """
    import xml.etree.ElementTree as ET

    query = (
        '"precision agriculture" OR "smart farming" OR "agritech" OR '
        '"agricultural technology" OR "crop yield" OR "vertical farming" OR '
        '"sustainable agriculture"'
    )
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-US&gl=US&ceid=US:en"

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
                source_name = source_el.text if source_el is not None else "Global Agritech"

                clean_title, pub_from_title = clean_agriculture_title(raw_title)
                if pub_from_title and source_name == "Global Agritech":
                    source_name = pub_from_title

                # Hayvancılık haberlerini Tarım kanalına alma (Hayvancılık Gündemi'ne aittir)
                t_lower = clean_title.lower()
                livestock_terms = [
                    "büyükbaş", "küçükbaş", "çiğ süt", "süt üretici", "süt fiyat", 
                    "sağım robotu", "besi hayvan", "damızlık sığır", "damızlık koyun",
                    "kırmızı et", "şap hastalığı", "tavukçuluk", "arıcılık", "kümes hayvan"
                ]
                if any(t in t_lower for t in livestock_terms):
                    continue

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
                    "guid": f"global_agri:{guid}",
                    "title": clean_title,
                    "title_tr": "",
                    "link": link,
                    "author": source_name,
                    "source_feed": f"🌍 {source_name}",
                    "description": clean_desc,
                    "summary_tr": "",
                    "category_tr": "Tarım Teknolojileri",
                    "is_turkey": 0,
                    "is_academic": 0,
                    "channel": "agriculture",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
    except Exception as e:
        logger.warning("Global agritech scrape failed: %s", e)

    return items


def scrape_academic_agriculture_publications(limit_per_query: int = 10, max_total: int = 35) -> List[Dict[str, Any]]:
    """
    Hakemli akademik ziraat, tarım, tohumculuk ve bitki bilimi yayınlarını
    Google Dorking operatörleriyle ScienceDirect, MDPI, Springer ve DergiPark üzerinden tarar.
    """
    import xml.etree.ElementTree as ET

    dork_queries = [
        # 1. ScienceDirect / Elsevier - Crop Science & Smart Agriculture
        ('site:sciencedirect.com/science/article ("smart agriculture" OR "precision farming" OR "crop yield") when:90d', 'en-US', 'US', 'US:en', 'ScienceDirect (Elsevier)'),
        # 2. MDPI Agronomy & Agriculture
        ('(site:mdpi.com/journal/agronomy OR site:mdpi.com/journal/agriculture) when:90d', 'en-US', 'US', 'US:en', 'MDPI Agronomy'),
        # 3. Springer Nature - Agriculture & Food Security
        ('site:link.springer.com/article ("agriculture" OR "agronomy" OR "crop production") when:90d', 'en-US', 'US', 'US:en', 'Springer Nature'),
        # 4. Frontiers in Sustainable Food Systems & Agronomy
        ('site:frontiersin.org/articles ("sustainable agriculture" OR "agronomy") when:90d', 'en-US', 'US', 'US:en', 'Frontiers in Agronomy'),
        # 5. DergiPark - Türkiye Akademik Ziraat ve Tarım Dergileri (TÜBİTAK ULAKBİM)
        ('(site:dergipark.org.tr/tr/pub/*/article OR site:dergipark.org.tr "ziraat fakültesi" OR "tarımsal araştırma") when:120d', 'tr', 'TR', 'TR:tr', 'DergiPark (TÜBİTAK ULAKBİM)'),
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

                clean_title, extracted_pub = clean_agriculture_title(raw_title)
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

                # Hayvancılık haberlerini Tarım kanalına alma (Hayvancılık Gündemi'ne aittir)
                t_lower = clean_title.lower()
                livestock_terms = [
                    "büyükbaş", "küçükbaş", "çiğ süt", "süt üretici", "süt fiyat", 
                    "sağım robotu", "besi hayvan", "damızlık sığır", "damızlık koyun",
                    "kırmızı et", "şap hastalığı", "tavukçuluk", "arıcılık", "kümes hayvan"
                ]
                if any(t in t_lower for t in livestock_terms):
                    continue

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
                    "guid": f"academic_agri:{guid}",
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
                    "channel": "agriculture",
                    "image_url": "",
                    "pub_date": pub_rfc,
                    "pub_date_ts": pub_ts,
                    "raw_date_str": pub_str,
                })
                query_count += 1
        except Exception as e:
            logger.warning("Academic agriculture publication scrape failed for query [%s]: %s", query, e)

    return items
