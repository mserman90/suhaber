import html
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.quotes import get_daily_water_quote

def clean_html_tags(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    return " ".join(clean.split())

def generate_newspaper_portal_html(
    items: List[Dict[str, Any]],
    last_updated: str,
    rss_url: str,
    atom_url: str,
    json_url: str,
    channel: str = "water",
    water_count: int = 0,
    agri_count: int = 0,
    livestock_count: int = 0,
    agri_items: Optional[List[Dict[str, Any]]] = None,
    livestock_items: Optional[List[Dict[str, Any]]] = None
) -> str:
    today_str = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    is_agri = (channel == "agriculture")
    is_livestock = (channel == "livestock")

    if is_livestock:
        channel_key = "livestock"
        portal_name_tr = "HAYVANCILIK GÜNDEMİ"
        portal_name_en = "LIVESTOCK AGENDA"
        portal_sub_name_tr = "Türkiye ve Dünya Hayvancılık, Süt, Besi, Yem ve Hayvan Sağlığı Gazetesi"
        portal_sub_name_en = "Turkey & Global Livestock, Dairy, Meat, Feed & Animal Health Newspaper"
        portal_motto_tr = '"Köylünün refahı ve milletin gıdası, güçlü ve yerli hayvancılıkla mümkündür."'
        portal_motto_en = '"The welfare of rural communities and nourishment of the nation rely on strong, sustainable livestock."'
        portal_title_tag_tr = "Hayvancılık Gündemi — Türkiye ve Dünya Hayvancılık & Süt Endüstrisi Gazetesi"
        portal_title_tag_en = "Livestock Agenda — Turkey & Global Livestock & Dairy Industry Newspaper"
    elif is_agri:
        channel_key = "agriculture"
        portal_name_tr = "TARIM GÜNDEMİ"
        portal_name_en = "AGRICULTURE AGENDA"
        portal_sub_name_tr = "Türkiye ve Dünya Tarım, Bitkisel Üretim, Tohumculuk ve Akıllı Tarım Gazetesi"
        portal_sub_name_en = "Turkey & Global Agriculture, Crop Production, Seed & Smart Farming Newspaper"
        portal_motto_tr = '"Milli ekonominin temeli tarımdır." &mdash; Mustafa Kemal Atatürk'
        portal_motto_en = '"The foundation of the national economy is agriculture." &mdash; Mustafa Kemal Atatürk'
        portal_title_tag_tr = "Tarım Gündemi — Türkiye ve Dünya Tarım, Bitkisel Üretim & Akıllı Tarım Gazetesi"
        portal_title_tag_en = "Agriculture Agenda — Turkey & Global Agriculture, Crop Production & Smart Farming Newspaper"
    else:
        channel_key = "water"
        portal_name_tr = "SU GÜNDEMİ"
        portal_name_en = "WATER AGENDA"
        portal_sub_name_tr = "Türkiye ve Dünya Su, Sulama ve Çevre Araştırmaları Gazetesi"
        portal_sub_name_en = "Turkey & Global Water, Irrigation & Environmental Research Newspaper"
        portal_motto_tr = '"Geleceğin dünyasında en stratejik güç sudur."'
        portal_motto_en = '"In the world of tomorrow, water is the most strategic power."'
        portal_title_tag_tr = "Su Gündemi — Türkiye ve Dünya Su & Sulama Gazetesi"
        portal_title_tag_en = "Water Agenda — Turkey & Global Water & Irrigation Newspaper"

    portal_name = portal_name_tr
    portal_sub_name = portal_sub_name_tr
    portal_motto = portal_motto_tr
    portal_title_tag = portal_title_tag_tr

    # Günün Sözü (Su / Tarım / Hayvancılık Yönetimi Öğütleri)
    if is_livestock:
        from app.quotes import get_daily_livestock_quote
        daily_quote = get_daily_livestock_quote()
        quote_text = html.escape(daily_quote.get("quote", ""))
        quote_text_en = html.escape(daily_quote.get("quote_en", daily_quote.get("quote", "")))
        quote_author = html.escape(daily_quote.get("author", "Milli Hayvancılık Rehberi"))
        quote_author_en = html.escape(daily_quote.get("author_en", "National Livestock Guide"))
        quote_cat = html.escape(daily_quote.get("category", "Hayvancılık"))
        quote_cat_en = html.escape(daily_quote.get("category_en", "Livestock"))
    elif is_agri:
        from app.quotes import get_daily_agriculture_quote
        daily_quote = get_daily_agriculture_quote()
        quote_text = html.escape(daily_quote.get("quote", ""))
        quote_text_en = html.escape(daily_quote.get("quote_en", daily_quote.get("quote", "")))
        quote_author = html.escape(daily_quote.get("author", "Milli Tarım Rehberi"))
        quote_author_en = html.escape(daily_quote.get("author_en", "National Agriculture Guide"))
        quote_cat = html.escape(daily_quote.get("category", "Tarım"))
        quote_cat_en = html.escape(daily_quote.get("category_en", "Agriculture"))
    else:
        daily_quote = get_daily_water_quote()
        quote_text = html.escape(daily_quote.get("quote", ""))
        quote_text_en = html.escape(daily_quote.get("quote_en", daily_quote.get("quote", "")))
        quote_author = html.escape(daily_quote.get("author", "Su Yönetimi Rehberi"))
        quote_author_en = html.escape(daily_quote.get("author_en", "Water Management Guide"))
        quote_cat = html.escape(daily_quote.get("category", "Su Yönetimi"))
        quote_cat_en = html.escape(daily_quote.get("category_en", "Water Management"))

    now_ts = int(datetime.now(timezone.utc).timestamp())

    if is_livestock:
        def headline_sort_key(x):
            guid = x.get("guid", "")
            source = x.get("source_feed", "")
            title = (x.get("title_tr", "") + " " + x.get("title", "")).lower()

            if any(bad in title for bad in ["colorado", "california", "texas", "brazil", "australia"]):
                return (-999999999, 0)

            is_tr = bool(
                guid.startswith("tr_livestock:")
                or "🐄" in source
                or "🇹🇷" in source
                or x.get("is_turkey")
                or x.get("category_tr") == "Türkiye"
            )
            if not is_tr:
                return (-999999999, 0)

            pub_ts = int(x.get("pub_date_ts") or 0)
            age_days = max(0.0, (now_ts - pub_ts) / 86400.0) if pub_ts > 0 else 5.0

            quality = 1000.0
            if any(k in title for k in ["süt", "besi", "et ve süt kurumu", "yem", "damızlık", "kırmızı et", "küçükbaş", "büyükbaş", "hayvancılık"]):
                quality += 300.0
            if any(k in title for k in ["personel", "kadro", "voleybol", "futbol"]):
                quality -= 800.0

            final_score = quality - (age_days * 500.0)
            return (final_score, pub_ts)
    elif is_agri:
        def headline_sort_key(x):
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
    else:
        def headline_sort_key(x):
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

    # Filter out livestock items from agriculture channel if present
    if is_agri:
        livestock_terms = [
            "büyükbaş", "küçükbaş", "çiğ süt", "süt üretici", "süt fiyat", "sağım robotu",
            "besi hayvan", "damızlık sığır", "damızlık koyun", "kırmızı et", "şap hastalığı",
            "tavukçuluk", "arıcılık", "kümes hayvan", "et ve süt kurumu"
        ]
        items = [
            it for it in items
            if it.get("category_tr") != "Hayvancılık & Süt"
            and not any(term in (it.get("title_tr", "") + " " + it.get("title", "")).lower() for term in livestock_terms)
        ]

    # Sort items by date
    raw_sorted = sorted(items, key=lambda x: x.get("pub_date_ts", 0), reverse=True)
    tr_candidates = [it for it in raw_sorted if headline_sort_key(it)[0] > -500000]
    tr_sorted = sorted(tr_candidates, key=headline_sort_key, reverse=True)
    if tr_sorted:
        turkey_hero = tr_sorted[0]
        items_sorted = [turkey_hero] + [it for it in raw_sorted if it.get("guid") != turkey_hero.get("guid")]
    else:
        items_sorted = raw_sorted
    
    # Hero article (first item)
    hero_item = items_sorted[0] if items_sorted else None
    secondary_items = items_sorted[1:4] if len(items_sorted) > 1 else []
    remaining_items = items_sorted[4:] if len(items_sorted) > 4 else []

    if is_livestock:
        CATEGORY_SLUGS = {
            "Akademik Yayınlar": "akademik",
            "Hayvancılık Teknolojileri": "teknoloji",
            "Süt & Mandıra": "sut",
            "Besi & Kırmızı Et": "besi",
            "Yem & Besleme": "yem",
            "Hayvan Sağlığı & Biyogüvenlik": "saglik",
            "Küçükbaş Hayvancılık": "kucukbas",
            "Kanatlı Sektörü": "kanatli",
            "Destek & Fiyat Politikaları": "destek",
            "Hayvancılık & Besicilik": "besicilik",
        }
    elif is_agri:
        CATEGORY_SLUGS = {
            "Akademik Yayınlar": "akademik",
            "Tarım Teknolojileri": "teknoloji",
            "Tohum & Gübre": "tohum",
            "Tarımsal Destekler": "destek",
            "Küresel Tarım": "kuresel",
            "Bitkisel Üretim": "bitkisel",
        }
    else:
        CATEGORY_SLUGS = {
            "Akademik Yayınlar": "akademik",
            "Tarımsal Sulama": "sulama",
            "Su Teknolojileri": "teknoloji",
            "Su Arıtma & Kalite": "teknoloji",
            "Su Kaynakları": "kaynak",
            "İklim & Kuraklık": "iklim",
            "Su Politikaları": "politika",
        }

    # JSON payload for modal dialogs
    import json
    from app.image_enricher import resolve_article_image
    portal_data = []
    for idx, it in enumerate(items_sorted):
        img = it.get("image_url")
        if not img or "inoreader.com/camo" in img:
            img = resolve_article_image(it, idx, channel=channel)
        title_tr = it.get("title_tr") or it.get("title")
        summary_tr = it.get("summary_tr") or "Detaylar ilgili bilimsel araştırma ve haber bülteninde yer almaktadır."
        source = it.get("source_feed") or it.get("author") or ("Hayvancılık Araştırma" if is_livestock else ("Tarımsal Araştırma" if is_agri else "Bilimsel Araştırma"))
        is_turkey = bool(it.get("is_turkey") or it.get("category_tr") == "Türkiye" or "🇹🇷" in source or "🌾" in source or "🐄" in source)
        is_academic = bool(it.get("is_academic") or it.get("guid", "").startswith("academic:") or it.get("guid", "").startswith("academic_agri:") or it.get("guid", "").startswith("academic_livestock:") or "🎓" in source)
        cat_raw = it.get("category_tr")
        if not cat_raw or cat_raw == "Türkiye":
            if is_livestock:
                from app.translator import categorize_livestock_article
                cat_raw = categorize_livestock_article(title_tr, summary_tr)
            elif is_agri:
                from app.translator import categorize_agriculture_article
                cat_raw = categorize_agriculture_article(title_tr, summary_tr)
            else:
                from app.translator import categorize_article
                cat_raw = categorize_article(title_tr, summary_tr)
        default_cat_name = "Hayvancılık & Besicilik" if is_livestock else ("Bitkisel Üretim" if is_agri else "Su Kaynakları")
        default_slug_name = "besicilik" if is_livestock else ("bitkisel" if is_agri else "kaynak")
        category = cat_raw or default_cat_name
        slug = CATEGORY_SLUGS.get(category, default_slug_name)
        title_en_val = it.get("title_en") or it.get("title") or title_tr
        summary_en_val = it.get("summary_en") or ""
        curr_channel_tr = "Hayvancılık Gündemi" if is_livestock else ("Tarım Gündemi" if is_agri else "Su Gündemi")
        curr_channel_en = "Livestock Agenda" if is_livestock else ("Agriculture Agenda" if is_agri else "Water Agenda")
        portal_data.append({
            "id": idx,
            "title_tr": title_tr,
            "title_en": title_en_val,
            "summary_tr": summary_tr,
            "summary_en": summary_en_val,
            "category": category,
            "channel_key": channel,
            "channel_name": curr_channel_tr,
            "channel_name_en": curr_channel_en,
            "slug": slug,
            "source": source,
            "author": it.get("author", ""),
            "date": it.get("pub_date", ""),
            "link": it.get("link", ""),
            "image": img,
            "is_turkey": is_turkey,
            "is_academic": is_academic
        })

    from app.geocoder import geocode_article

    # Prepare Geocoded Datasets for Interactive Map (all channels)
    water_map_data = []
    agri_map_data = []
    livestock_map_data = []

    # All articles data dictionary for Modal lookup across all channels
    all_articles_data = list(portal_data)

    for it in portal_data:
        lat, lng, loc_name = geocode_article(it, it["id"])
        if lat is not None and lng is not None:
            water_map_data.append({
                "id": it["id"],
                "title": it["title_tr"],
                "category": it["category"],
                "date": it["date"][:16] if it.get("date") else today_str,
                "source": it.get("source", ""),
                "summary": it.get("summary_tr", "")[:260],
                "lat": lat,
                "lng": lng,
                "loc": loc_name,
                "channel": "water"
            })

    if agri_items:
        for idx, a_it in enumerate(agri_items):
            aid = 10000 + idx
            title_tr = a_it.get("title_tr") or a_it.get("title") or ""
            summary_tr = a_it.get("summary_tr") or ""
            source = a_it.get("source_feed") or a_it.get("author") or "Tarım Basını"
            cat = a_it.get("category_tr") or "Tarım & Bitkisel"
            img = a_it.get("image_url") or "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=900&q=80"
            lat, lng, loc_name = geocode_article(a_it, aid)
            
            all_articles_data.append({
                "id": aid,
                "title_tr": title_tr,
                "title_en": a_it.get("title_en") or a_it.get("title") or title_tr,
                "summary_tr": summary_tr,
                "summary_en": a_it.get("summary_en") or "",
                "category": cat,
                "channel_key": "agriculture",
                "channel_name": "Tarım Gündemi",
                "channel_name_en": "Agriculture Agenda",
                "slug": "tarim",
                "source": source,
                "author": a_it.get("author", "Tarım Muhabiri"),
                "date": a_it.get("pub_date", today_str),
                "link": a_it.get("link", "#"),
                "image": img,
                "is_turkey": a_it.get("is_turkey", False),
                "is_academic": a_it.get("is_academic", False)
            })

            if lat is not None and lng is not None:
                agri_map_data.append({
                    "id": aid,
                    "title": title_tr,
                    "category": cat,
                    "date": (a_it.get("pub_date") or today_str)[:16],
                    "source": source,
                    "summary": summary_tr[:260],
                    "lat": lat,
                    "lng": lng,
                    "loc": loc_name,
                    "channel": "agriculture"
                })

    if livestock_items:
        for idx, l_it in enumerate(livestock_items):
            lid = 20000 + idx
            title_tr = l_it.get("title_tr") or l_it.get("title") or ""
            summary_tr = l_it.get("summary_tr") or ""
            source = l_it.get("source_feed") or l_it.get("author") or "Hayvancılık Basını"
            cat = l_it.get("category_tr") or "Hayvancılık & Süt"
            img = l_it.get("image_url") or "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=900&q=80"
            lat, lng, loc_name = geocode_article(l_it, lid)

            all_articles_data.append({
                "id": lid,
                "title_tr": title_tr,
                "title_en": l_it.get("title_en") or l_it.get("title") or title_tr,
                "summary_tr": summary_tr,
                "summary_en": l_it.get("summary_en") or "",
                "category": cat,
                "channel_key": "livestock",
                "channel_name": "Hayvancılık Gündemi",
                "channel_name_en": "Livestock Agenda",
                "slug": "hayvancilik",
                "source": source,
                "author": l_it.get("author", "Zootekni Uzmanı"),
                "date": l_it.get("pub_date", today_str),
                "link": l_it.get("link", "#"),
                "image": img,
                "is_turkey": l_it.get("is_turkey", False),
                "is_academic": l_it.get("is_academic", False)
            })

            if lat is not None and lng is not None:
                livestock_map_data.append({
                    "id": lid,
                    "title": title_tr,
                    "category": cat,
                    "date": (l_it.get("pub_date") or today_str)[:16],
                    "source": source,
                    "summary": summary_tr[:260],
                    "lat": lat,
                    "lng": lng,
                    "loc": loc_name,
                    "channel": "livestock"
                })

    json_portal_data = json.dumps(all_articles_data, ensure_ascii=False)
    json_water_map = json.dumps(water_map_data, ensure_ascii=False)
    json_agri_map = json.dumps(agri_map_data, ensure_ascii=False)
    json_livestock_map = json.dumps(livestock_map_data, ensure_ascii=False)

    # Interactive Map Section HTML (Rendered on Home / Water Channel)
    interactive_map_html = ""
    if not is_agri and not is_livestock:
        interactive_map_html = f"""
        <section class="newspaper-map-section" id="interactiveMapSection">
            <!-- Map Toolbar: Side Panel Toggle & View Controls -->
            <div class="map-toolbar">
                <div class="map-toolbar-left">
                    <button type="button" class="btn-toggle-layers-bar" onclick="toggleMapSidePanel()" title="Katman Filtreleri Panelini Aç / Kapat">
                        <span class="icon">🗂️</span>
                        <span>Katman Filtreleri</span>
                        <span class="layer-pill-active" id="activeLayersBadge">💧 Su Gündemi Aktif</span>
                    </button>
                </div>
                <div class="map-view-controls">
                    <a href="https://mserman90.github.io/water-agreements-portal/" target="_blank" rel="noopener noreferrer" class="btn-portal-ext-link" title="Su Anlaşmaları Portalı'nı ayrı sekmede tam ekran aç" style="padding: 6px 14px; font-size: 12px; text-decoration: none; border-radius: 8px;">
                        <span>🏛️ Su Anlaşmaları Portalı</span>
                        <span class="ext-icon">↗</span>
                    </a>
                    <button type="button" class="btn-map-view" onclick="zoomMapTo('turkey')" title="Türkiye ve Çevresine Yakınlaş">
                        🇹🇷 Türkiye
                    </button>
                    <button type="button" class="btn-map-view" onclick="zoomMapTo('world')" title="Dünya Genel Görünümüne Uzaklaş">
                        🌍 Dünya
                    </button>
                    <button type="button" class="btn-map-view" id="btnMapFullscreen" onclick="toggleMapFullscreen()" title="Haritayı Genişlet / Küçült">
                        ⛶ Tam Ekran
                    </button>
                </div>
            </div>

            <!-- Map Canvas Container with Collapsible Left Side Panel -->
            <div class="map-canvas-wrapper" id="mapCanvasWrapper">
                <!-- Collapsible Left Side Panel for All News & Data Layers -->
                <aside class="map-side-panel" id="mapSidePanel" aria-label="Harita Katman Filtreleri">
                    <div class="side-panel-header">
                        <div class="side-panel-title-wrap">
                            <span class="side-panel-icon">🗂️</span>
                            <h3 class="side-panel-title">Katman Filtreleri</h3>
                        </div>
                        <button type="button" class="btn-close-side-panel" onclick="toggleMapSidePanel(false)" title="Paneli Gizle (Kapat)">
                            ✕
                        </button>
                    </div>

                    <div class="side-panel-body">
                        <!-- Haber Katmanları Grubu -->
                        <div class="panel-section">
                            <div class="panel-section-header">
                                <span class="panel-section-tag">HABER KATMANLARI</span>
                                <span class="panel-section-help">Haber akışları</span>
                            </div>

                            <label class="panel-layer-card active" data-layer="water" id="layerBtn_water" title="Su Gündemi haberleri (Varsayılan aktif katman)">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerWaterCheck" checked onchange="toggleMapLayer('water')">
                                    <span class="layer-dot layer-dot-water"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">💧 Su Gündemi</span>
                                        <span class="layer-desc">Barajlar, kuraklık, su politikaları</span>
                                    </div>
                                </div>
                                <span class="layer-count" id="countWaterNews">{len(water_map_data)}</span>
                            </label>

                            <label class="panel-layer-card" data-layer="agri" id="layerBtn_agri" title="Tarım Gündemi haber katmanı">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerAgriCheck" onchange="toggleMapLayer('agri')">
                                    <span class="layer-dot layer-dot-agri"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">🌾 Tarım Gündemi</span>
                                        <span class="layer-desc">Bitkisel üretim, hasat, agritech</span>
                                    </div>
                                </div>
                                <span class="layer-count" id="countAgriNews">{len(agri_map_data)}</span>
                            </label>

                            <label class="panel-layer-card" data-layer="livestock" id="layerBtn_livestock" title="Hayvancılık Gündemi haber katmanı">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerLivestockCheck" onchange="toggleMapLayer('livestock')">
                                    <span class="layer-dot layer-dot-livestock"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">🐄 Hayvancılık Gündemi</span>
                                        <span class="layer-desc">Süt, besi, yem, hayvancılık</span>
                                    </div>
                                </div>
                                <span class="layer-count" id="countLivestockNews">{len(livestock_map_data)}</span>
                            </label>
                        </div>

                        <!-- Hidropolitik Veri Grubu -->
                        <div class="panel-section">
                            <div class="panel-section-header">
                                <span class="panel-section-tag">HİDROPOLİTİK VERİ ATLASI</span>
                                <span class="panel-section-help">Uluslararası arşivler</span>
                            </div>

                            <label class="panel-layer-card" data-layer="agreements" id="layerBtn_agreements" title="1820'den günümüze sınır aşan su anlaşmaları (TFDD / Oregon State Univ.)">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerAgreementsCheck" onchange="toggleMapLayer('agreements')">
                                    <span class="layer-dot layer-dot-agreements"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">🌊 Su Anlaşmaları (TFDD)</span>
                                        <span class="layer-desc">Uluslararası ikili/çoklu metinler</span>
                                    </div>
                                </div>
                                <span class="layer-count">3.059</span>
                            </label>

                            <label class="panel-layer-card" data-layer="conflicts" id="layerBtn_conflicts" title="Tarihi su uyuşmazlıkları ve olaylar (Pacific Institute / BAR)">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerConflictsCheck" onchange="toggleMapLayer('conflicts')">
                                    <span class="layer-dot layer-dot-conflicts"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">⚡ Su Olayları &amp; Krizler</span>
                                        <span class="layer-desc">Pacific Institute kronolojisi</span>
                                    </div>
                                </div>
                                <span class="layer-count">2.809</span>
                            </label>

                            <label class="panel-layer-card" data-layer="basins" id="layerBtn_basins" title="310 uluslararası sınır aşan nehir ve göl havzası poligonları">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerBasinsCheck" onchange="toggleMapLayer('basins')">
                                    <span class="layer-dot layer-dot-basins"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">🗺️ 310 Sınır Aşan Havza</span>
                                        <span class="layer-desc">Nehir &amp; göl sınır poligonları</span>
                                    </div>
                                </div>
                                <span class="layer-count">310</span>
                            </label>
                        </div>

                        <!-- Panel Alt Eylemler -->
                        <div class="panel-footer-actions">
                            <button type="button" class="btn-panel-action" onclick="resetToDefaultLayer()" title="Yalnızca Su Gündemi katmanını açık bırak">
                                ↺ Varsayılana Dön (Su Gündemi)
                            </button>
                        </div>
                    </div>
                </aside>

                <!-- Floating Canvas Open Toggle Button (Visible when side panel is closed) -->
                <button type="button" class="map-canvas-toggle-btn" id="mapCanvasToggleBtn" onclick="toggleMapSidePanel(true)" title="Katman Filtrelerini Aç" style="display: inline-flex;">
                    <span class="toggle-icon">☰</span>
                    <span class="toggle-txt">Katmanlar</span>
                    <span class="toggle-badge" id="canvasActiveBadge">1</span>
                </button>

                <div id="portalLeafletMap" class="portal-leaflet-map"></div>

                <!-- Floating In-Map Search Box (Top-Right) -->
                <div class="map-search-bar" id="mapSearchBar">
                    <input type="text" id="mapSearchInput" placeholder="🔎 Şehir, Havza veya Nehir Ara..." onkeydown="if(event.key==='Enter') executeMapSearch()">
                    <button type="button" onclick="executeMapSearch()" title="Konuma Git">Odaklan</button>
                </div>

                <div id="mapLoadingIndicator" class="map-loading-overlay" style="display: none;">
                    <div class="map-spinner"></div>
                    <span id="mapLoadingText">Veri katmanı yükleniyor...</span>
                </div>
            </div>
        </section>
        """
    # Secondary headline cards
    secondary_html = ""
    for it in portal_data[1:4]:
        if it.get("is_turkey"):
            badge_cls = "news-badge news-badge-turkey"
            badge_lbl = f"🇹🇷 {html.escape(it['category'])}"
        elif it.get("is_academic"):
            badge_cls = "news-badge news-badge-academic"
            badge_lbl = f"🎓 {html.escape(it['category'])}"
        else:
            badge_cls = "news-badge"
            badge_lbl = html.escape(it['category'])
        secondary_html += f"""
        <div class="sub-headline-card" onclick="openArticleModal({it['id']})" data-slug="{it['slug']}">
            <div class="sub-headline-img" style="background-image: url('{html.escape(it['image'])}');">
                <span class="{badge_cls}" onclick="event.stopPropagation(); filterCategory('{it['slug']}')">{badge_lbl}</span>
            </div>
            <div class="sub-headline-content">
                <span class="news-date">📅 {html.escape(it['date'][:16] if it.get('date') else today_str)}</span>
                <h4 data-article-title-id="{it['id']}">{html.escape(it['title_tr'])}</h4>
                <p data-article-summary-id="{it['id']}">{html.escape(it['summary_tr'][:120])}...</p>
            </div>
        </div>
        """

    # Grid article cards (renders all items; items 0-3 hidden in 'all' view since displayed in hero/subheadlines)
    grid_html = ""
    for it in portal_data:
        is_top = it['id'] < 4
        display_style = ' style="display: none;"' if is_top else ''
        search_corpus = clean_html_tags(f"{it['title_tr']} {it['title_en']} {it['summary_tr']} {it['category']} {it['source']}").lower()
        if it.get("is_turkey"):
            badge_cls = "news-badge news-badge-turkey"
            badge_lbl = f"🇹🇷 {html.escape(it['category'])}"
        elif it.get("is_academic"):
            badge_cls = "news-badge news-badge-academic"
            badge_lbl = f"🎓 {html.escape(it['category'])}"
        else:
            badge_cls = "news-badge"
            badge_lbl = html.escape(it['category'])
        is_tr_str = "true" if it.get("is_turkey") else "false"
        is_acad_str = "true" if it.get("is_academic") else "false"
        it_orig_title_html = (
            f'<h5 class="card-title-en" data-article-original-title-id="{it["id"]}">Orijinal Başlık: {html.escape(it["title_en"])}</h5>'
            if (it.get('title_en') and it['title_en'] != it['title_tr']) else ''
        )
        grid_html += f"""
        <article class="news-grid-card" data-slug="{it['slug']}" data-is-turkey="{is_tr_str}" data-is-academic="{is_acad_str}" data-category="{html.escape(it['category'])}" data-is-top="{'true' if is_top else 'false'}" data-search="{html.escape(search_corpus)}"{display_style}>
            <div class="card-img-wrap" style="background-image: url('{html.escape(it['image'])}');" onclick="openArticleModal({it['id']})">
                <span class="{badge_cls}" onclick="event.stopPropagation(); filterCategory('{it['slug']}')">{badge_lbl}</span>
            </div>
            <div class="card-body">
                <div class="card-meta">
                    <span>📅 {html.escape(it['date'][:16] if it.get('date') else today_str)}</span>
                    <span>{html.escape(it['source'][:32])}</span>
                </div>
                <h3 class="card-title" data-article-title-id="{it['id']}" onclick="openArticleModal({it['id']})">
                    {html.escape(it['title_tr'])}
                </h3>
                {it_orig_title_html}
                <p class="card-excerpt" data-article-summary-id="{it['id']}">
                    {html.escape(it['summary_tr'][:180])}...
                </p>
                <div class="card-action-bar">
                    <button class="btn-read-more" data-i18n="read_news" onclick="openArticleModal({it['id']})">Haberi Oku &rarr;</button>
                    <a href="{html.escape(it['link'])}" target="_blank" rel="noopener noreferrer" class="link-original" data-i18n="source_link" title="Orijinal Araştırma Sayfası">
                        🔗 Kaynak
                    </a>
                </div>
            </div>
        </article>
        """

    # Channel Ticker Configuration
    if is_livestock:
        channel_ticker_icon = "🐄"
        channel_ticker_label = "HAYVANCILIK GÜNDEMİ"
        bottom_ticker_border = "#d97706"
        bottom_ticker_badge_bg = "linear-gradient(135deg, #b45309, #d97706)"
        bottom_ticker_accent = "#fbbf24"
    elif is_agri:
        channel_ticker_icon = "🌾"
        channel_ticker_label = "TARIM GÜNDEMİ"
        bottom_ticker_border = "#16a34a"
        bottom_ticker_badge_bg = "linear-gradient(135deg, #15803d, #16a34a)"
        bottom_ticker_accent = "#4ade80"
    else:
        channel_ticker_icon = "💧"
        channel_ticker_label = "SU GÜNDEMİ"
        bottom_ticker_border = "#0284c7"
        bottom_ticker_badge_bg = "linear-gradient(135deg, #0369a1, #0284c7)"
        bottom_ticker_accent = "#38bdf8"

    # Ticker items (Bottom fixed banner - prioritizing Turkey news of this channel)
    turkey_ticker_items = [it for it in portal_data if it.get("is_turkey")]
    merged_ticker = []
    # Prioritize top 6 Turkey items of this channel
    merged_ticker.extend(turkey_ticker_items[:6])
    # Then fill up to 18 items with top portal items of this channel
    for it in portal_data:
        if it not in merged_ticker and len(merged_ticker) < 18:
            merged_ticker.append(it)

    ticker_elements = []
    for it in merged_ticker:
        cat = it.get("category", "")
        if it.get("is_turkey"):
            cat_badge = f'<span class="ticker-cat-tag ticker-cat-turkey">[🇹🇷 {html.escape(cat)}]</span>' if (cat and cat != "Türkiye") else '<span class="ticker-cat-tag ticker-cat-turkey">[🇹🇷 Türkiye]</span>'
        elif it.get("is_academic") or cat == "Akademik":
            cat_badge = f'<span class="ticker-cat-tag ticker-cat-academic">[🎓 {html.escape(cat)}]</span>'
        else:
            cat_badge = f'<span class="ticker-cat-tag">[{html.escape(cat)}]</span>' if cat else ""

        ticker_elements.append(
            f'<span class="ticker-item" onclick="openArticleModal({it["id"]})">'
            f'<span class="ticker-icon">⚡</span> '
            f'{cat_badge} '
            f'<span class="ticker-text" data-article-ticker-id="{it["id"]}">{html.escape(it["title_tr"])}</span>'
            f'<span class="ticker-sep">&bull;</span>'
            f'</span>'
        )
    single_track_html = "".join(ticker_elements)
    # Double track ensures seamless infinite loop with zero jump
    ticker_track_content = single_track_html + single_track_html

    # Hero element (Günün Manşeti)
    hero_html = ""
    if portal_data:
        h = portal_data[0]
        is_tr_hero = bool(h.get("is_turkey") or h.get("category") == "Türkiye")
        if is_livestock:
            badge_title = "⭐ GÜNÜN MANŞETİ &bull; 🇹🇷 TÜRKİYE HAYVANCILIK GÜNDEMİ" if is_tr_hero else f"⭐ GÜNÜN MANŞETİ &bull; {html.escape(h['category'])}"
            hero_hint = "📰 Ulusal &amp; Sektörel Basın &bull; Güncel Hayvancılık, Süt ve Et Raporları" if is_tr_hero else "ScienceDirect / MDPI / FAO Hayvancılık Veritabanı Kaynağı"
        elif is_agri:
            badge_title = "⭐ GÜNÜN MANŞETİ &bull; 🇹🇷 TÜRKİYE TARIM GÜNDEMİ" if is_tr_hero else f"⭐ GÜNÜN MANŞETİ &bull; {html.escape(h['category'])}"
            hero_hint = "📰 Ulusal &amp; Tarım Basını &bull; Güncel Tarım ve Üretim Raporları" if is_tr_hero else "ScienceDirect / MDPI / FAO Tarımsal Veritabanı Kaynağı"
        else:
            badge_title = "⭐ GÜNÜN MANŞETİ &bull; 🇹🇷 TÜRKİYE SU GÜNDEMİ" if is_tr_hero else f"⭐ GÜNÜN MANŞETİ &bull; {html.escape(h['category'])}"
            hero_hint = "📰 Ulusal &amp; Yerel Basın &bull; Güncel Su Araştırmaları" if is_tr_hero else "ScienceDirect / ASCE / IWMI Akademik Veritabanı Kaynağı"
        hero_orig_title_html = (
            f'<h4 class="hero-title-en" data-article-original-title-id="{h["id"]}">Orijinal Başlık: {html.escape(h["title_en"])}</h4>'
            if (h.get('title_en') and h['title_en'] != h['title_tr']) else ''
        )
        hero_html = f"""
        <section class="main-headline-banner" id="heroSection" onclick="openArticleModal({h['id']})" data-slug="{h['slug']}">
            <div class="hero-image-col" style="background-image: url('{html.escape(h['image'])}');">
                <div class="hero-image-overlay">
                    <span class="hero-category-tag" onclick="event.stopPropagation(); filterCategory('{h['slug']}')">{badge_title}</span>
                </div>
            </div>
            <div class="hero-content-col">
                <div class="hero-meta">
                    <span>📅 {html.escape(h['date'][:16] if h.get('date') else today_str)}</span> &bull; 
                    <span>{html.escape(h['source'][:40])}</span>
                </div>
                <h2 class="hero-title" data-article-title-id="{h['id']}">{html.escape(h['title_tr'])}</h2>
                {hero_orig_title_html}
                <p class="hero-summary" data-article-summary-id="{h['id']}">{html.escape(h['summary_tr'][:320])}...</p>
                <div class="hero-footer">
                    <button class="btn-hero-read">Tam Haberi ve Analizi Oku &rarr;</button>
                    <span class="hero-hint">{hero_hint}</span>
                </div>
            </div>
        </section>
        """

    # Channel-specific texts, stats, tabs and navigation pills
    water_active_cls = "active" if (not is_agri and not is_livestock) else ""
    agri_active_cls = "active" if is_agri else ""
    livestock_active_cls = "active" if is_livestock else ""
    
    water_badge_count = f'<span class="channel-tab-badge">{water_count}</span>' if water_count > 0 else ''
    agri_badge_count = f'<span class="channel-tab-badge">{agri_count}</span>' if agri_count > 0 else ''
    livestock_badge_count = f'<span class="channel-tab-badge">{livestock_count}</span>' if livestock_count > 0 else ''

    channel_tabs_html = f"""
    <div class="channel-switcher-container">
        <div class="channel-switcher-inner">
            <a href="index.html" class="channel-tab-btn {water_active_cls}" id="tabWater" title="Su Gündemi">
                <span class="channel-tab-icon">💧</span>
                <span class="channel-tab-name" id="tabNameWater" data-i18n="tab_water">SU GÜNDEMİ</span>
                {water_badge_count}
            </a>
            <a href="tarim.html" class="channel-tab-btn {agri_active_cls}" id="tabAgri" title="Tarım Gündemi">
                <span class="channel-tab-icon">🌾</span>
                <span class="channel-tab-name" id="tabNameAgri" data-i18n="tab_agri">TARIM GÜNDEMİ</span>
                {agri_badge_count}
            </a>
            <a href="hayvancilik.html" class="channel-tab-btn {livestock_active_cls}" id="tabLivestock" title="Hayvancılık Gündemi">
                <span class="channel-tab-icon">🐄</span>
                <span class="channel-tab-name" id="tabNameLivestock" data-i18n="tab_livestock">HAYVANCILIK GÜNDEMİ</span>
                {livestock_badge_count}
            </a>
        </div>
    </div>
    """

    if is_livestock:
        top_stat_html = (
            '<a href="https://data.tuik.gov.tr/Bulten/Index?p=Hayvansal-Uretim-Istatistikleri" '
            'target="_blank" rel="noopener noreferrer" class="top-stat-link" '
            'title="Hesaplama Kaynağı: TÜİK Hayvansal Üretim İstatistikleri">'
            '🐄 Büyükbaş Varlığı: ~16.6 Milyon Baş | Küçükbaş: ~52.4 Milyon Baş <span class="ext-link-icon">↗</span></a>'
        )
        category_pills_html = """
                <button type="button" class="cat-btn active" data-slug="all" onclick="filterCategory('all')">Tümü</button>
                <button type="button" class="cat-btn" data-slug="sut" onclick="filterCategory('sut')">🥛 Süt &amp; Mandıra</button>
                <button type="button" class="cat-btn" data-slug="besi" onclick="filterCategory('besi')">🥩 Besi &amp; Kırmızı Et</button>
                <button type="button" class="cat-btn" data-slug="yem" onclick="filterCategory('yem')">🌾 Yem &amp; Besleme</button>
                <button type="button" class="cat-btn" data-slug="saglik" onclick="filterCategory('saglik')">🩺 Hayvan Sağlığı</button>
                <button type="button" class="cat-btn" data-slug="kucukbas" onclick="filterCategory('kucukbas')">🐑 Küçükbaş</button>
                <button type="button" class="cat-btn" data-slug="kanatli" onclick="filterCategory('kanatli')">🐔 Kanatlı Sektörü</button>
                <button type="button" class="cat-btn" data-slug="teknoloji" onclick="filterCategory('teknoloji')">🤖 Hayvancılık Teknolojileri</button>
                <button type="button" class="cat-btn" data-slug="destek" onclick="filterCategory('destek')">📊 Destek &amp; Fiyat</button>
                <button type="button" class="cat-btn" data-slug="akademik" onclick="filterCategory('akademik')">🎓 Akademik Yayınlar</button>
        """.strip()
        section_title = "🐄 Son Hayvancılık Haberleri, Piyasa Raporları &amp; Araştırmalar"
        empty_icon = "🐄"
        sidebar_stats_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Rakamlarla Hayvancılık</h4>
                    <div class="stat-row">
                        <span>Yıllık Çiğ Süt Üretimi</span>
                        <span class="stat-value">~21.5 Milyon Ton</span>
                    </div>
                    <div class="stat-row">
                        <span>Yıllık Kırmızı Et Üretimi</span>
                        <span class="stat-value">~2.4 Milyon Ton</span>
                    </div>
                    <div class="stat-row">
                        <span>Kanatlı Eti Üretimi</span>
                        <span class="stat-value">~2.3 Milyon Ton</span>
                    </div>
                    <div class="stat-row">
                        <span>Kişi Başı Yıllık Süt Tüketimi</span>
                        <span class="stat-value">~265 kg</span>
                    </div>
                </div>
        """.strip()
        sidebar_sources_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Taranan Hayvancılık Kaynakları</h4>
                    <ul style="font-size:12px; color:var(--ink-muted); padding-left:18px; line-height:1.8;">
                        <li>ScienceDirect: Animal Science &amp; Veterinary</li>
                        <li>MDPI: Animals &amp; Dairy Science</li>
                        <li>Frontiers in Veterinary Science</li>
                        <li>FAO: Livestock &amp; Animal Health</li>
                        <li>DergiPark: Ulusal Veterinerlik ve Zootekni Dergileri</li>
                    </ul>
                </div>
        """.strip()
        category_titles_js = """
            'all': '🐄 Son Hayvancılık Haberleri, Piyasa Raporları &amp; Araştırmalar',
            'sut': '🥛 Çiğ Süt, Mandıra &amp; Soğuk Zincir Gelişmeleri',
            'besi': '🥩 Besicilik, Kırmızı Et &amp; Karkas Piyasası',
            'yem': '🌾 Yem, Silaj &amp; Rasyon Maliyetleri',
            'saglik': '🩺 Hayvan Sağlığı, Aşı &amp; Biyogüvenlik',
            'kucukbas': '🐑 Küçükbaş Hayvancılık &amp; Mera Yönetimi',
            'kanatli': '🐔 Kanatlı Endüstrisi &amp; Yumurta Üretimi',
            'teknoloji': '🤖 Akıllı Sağım, Sensör &amp; Sürü Yönetimi',
            'destek': '📊 Hayvancılık Destekleri &amp; Taban Fiyatlar',
            'akademik': '🎓 Hakemli Zootekni &amp; Veterinerlik Araştırmaları'
        """.strip()
        footer_sub_text = "Süt, besi, yem, hayvan sağlığı, zootekni ve hakemli veterinerlik dergilerinden derlenen günlük dijital hayvancılık gazetesi."
        live_feed_file = "feed_hayvancilik.json"
    elif is_agri:
        top_stat_html = (
            '<a href="https://data.worldbank.org/indicator/NV.AGR.TOTL.ZS?locations=TR" '
            'target="_blank" rel="noopener noreferrer" class="top-stat-link" '
            'title="Hesaplama Kaynağı: Dünya Bankası ve TÜİK Tarımsal Üretim İstatistikleri">'
            '🌾 Tarımsal GSYH: ~68.5 Milyar $ <span class="ext-link-icon">↗</span></a>'
        )
        category_pills_html = """
                <button type="button" class="cat-btn active" data-slug="all" onclick="filterCategory('all')">Tümü</button>
                <button type="button" class="cat-btn" data-slug="bitkisel" onclick="filterCategory('bitkisel')">🌱 Bitkisel Üretim</button>
                <button type="button" class="cat-btn" data-slug="teknoloji" onclick="filterCategory('teknoloji')">🚜 Tarım Teknolojileri</button>
                <button type="button" class="cat-btn" data-slug="tohum" onclick="filterCategory('tohum')">🌾 Tohum &amp; Gübre</button>
                <button type="button" class="cat-btn" data-slug="destek" onclick="filterCategory('destek')">📊 Tarımsal Destekler</button>
                <button type="button" class="cat-btn" data-slug="kuresel" onclick="filterCategory('kuresel')">🌍 Küresel Tarım</button>
                <button type="button" class="cat-btn" data-slug="akademik" onclick="filterCategory('akademik')">🎓 Akademik Yayınlar</button>
        """.strip()
        section_title = "🌾 Son Tarım Haberleri, Raporlar &amp; Araştırmalar"
        empty_icon = "🌾"
        sidebar_stats_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Rakamlarla Tarım Durumu</h4>
                    <div class="stat-row">
                        <span>Tarımın İstihdamdaki Payı</span>
                        <span class="stat-value">%15.8</span>
                    </div>
                    <div class="stat-row">
                        <span>İşlenen Tarım Alanı</span>
                        <span class="stat-value">23.8 Milyon Ha</span>
                    </div>
                    <div class="stat-row">
                        <span>Tarımsal İhracat Hacmi</span>
                        <span class="stat-value">~31 Milyar $</span>
                    </div>
                    <div class="stat-row">
                        <span>Örtüaltı Tarım Alanı</span>
                        <span class="stat-value">830 Bin Dekar</span>
                    </div>
                </div>
        """.strip()
        sidebar_sources_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Taranan Tarımsal Kaynaklar</h4>
                    <ul style="font-size:12px; color:var(--ink-muted); padding-left:18px; line-height:1.8;">
                        <li>ScienceDirect: Field Crops &amp; Agronomy</li>
                        <li>MDPI: Agronomy &amp; Agriculture Journal</li>
                        <li>Springer: Precision Agriculture &amp; Food Security</li>
                        <li>FAO: Food &amp; Agriculture Organization</li>
                        <li>DergiPark: Ulusal Tarım Bilimleri Dergileri</li>
                    </ul>
                </div>
        """.strip()
        category_titles_js = """
            'all': '🌾 Son Tarım Haberleri, Raporlar &amp; Araştırmalar',
            'bitkisel': '🌱 Bitkisel Üretim &amp; Hasat Gelişmeleri',
            'teknoloji': '🚜 Akıllı Tarım &amp; Tarım Teknolojileri',
            'tohum': '🌾 Tohum, Gübre &amp; Bitki Besleme',
            'destek': '📊 Tarımsal Destekler &amp; Ekonomi',
            'kuresel': '🌍 Küresel Tarım Piyasaları &amp; Raporlar',
            'akademik': '🎓 Hakemli Tarım &amp; Agronomi Araştırmaları'
        """.strip()
        footer_sub_text = "Bitkisel üretim, tarım teknolojileri, tohumculuk, gübreleme ve hakemli tarım dergilerinden derlenen günlük dijital tarım gazetesi."
        live_feed_file = "feed_tarim.json"
    else:
        top_stat_html = (
            '<a href="https://www.wri.org/applications/aqueduct/water-risk-atlas/" '
            'target="_blank" rel="noopener noreferrer" class="top-stat-link" '
            'title="Hesaplama Kaynağı: WRI (World Resources Institute) Aqueduct Su Riski ve Stresi Atlası">'
            '💧 Türkiye Su Stresi: %64.2 <span class="ext-link-icon">↗</span></a>'
        )
        category_pills_html = """
                <button type="button" class="cat-btn active" data-slug="all" onclick="filterCategory('all')">Tümü</button>
                <button type="button" class="cat-btn" data-slug="akademik" onclick="filterCategory('akademik')">🎓 Akademik Yayınlar</button>
                <button type="button" class="cat-btn" data-slug="sulama" onclick="filterCategory('sulama')">🌾 Tarımsal Sulama</button>
                <button type="button" class="cat-btn" data-slug="teknoloji" onclick="filterCategory('teknoloji')">🔬 Su Teknolojileri</button>
                <button type="button" class="cat-btn" data-slug="kaynak" onclick="filterCategory('kaynak')">💧 Su Kaynakları</button>
                <button type="button" class="cat-btn" data-slug="iklim" onclick="filterCategory('iklim')">🌍 İklim &amp; Kuraklık</button>
                <button type="button" class="cat-btn" data-slug="politika" onclick="filterCategory('politika')">⚖️ Su Politikaları</button>
        """.strip()
        section_title = "🌊 Son Bilimsel Araştırmalar &amp; Raporlar"
        empty_icon = "💧"
        sidebar_stats_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Rakamlarla Su Durumu</h4>
                    <div class="stat-row">
                        <span>Tarımsal Su Kullanım Payı</span>
                        <span class="stat-value">%73</span>
                    </div>
                    <div class="stat-row">
                        <span>Damla Sulamada Tasarruf</span>
                        <span class="stat-value">+%45</span>
                    </div>
                    <div class="stat-row">
                        <span>Kuraklık Tehdidi Altındaki Nüfus</span>
                        <span class="stat-value">2.3 Milyar</span>
                    </div>
                    <div class="stat-row">
                        <span>Yıllık Geri Dönüşüm Hedefi</span>
                        <span class="stat-value">%25 Artış</span>
                    </div>
                </div>
        """.strip()
        sidebar_sources_html = """
                <div class="sidebar-card">
                    <h4 class="sidebar-title">Taranan Bilimsel Kaynaklar</h4>
                    <ul style="font-size:12px; color:var(--ink-muted); padding-left:18px; line-height:1.8;">
                        <li>ScienceDirect: Agricultural Water Management</li>
                        <li>ASCE: Journal of Water Resources Planning</li>
                        <li>IWMI: International Water Management Institute</li>
                        <li>Limnologica: Ecology of Inland Waters</li>
                        <li>Water Finance &amp; Management Bülteni</li>
                    </ul>
                </div>
        """.strip()
        category_titles_js = """
            'all': '🌊 Son Bilimsel Araştırmalar &amp; Raporlar',
            'akademik': '🎓 Yeni Yayınlanan Su Yönetimi Hakemli Akademik Makaleleri',
            'sulama': '🌾 Tarımsal Sulama Araştırmaları',
            'teknoloji': '🔬 Su Teknolojileri &amp; İnovasyon',
            'kaynak': '💧 Su Kaynakları &amp; Havza Yönetimi',
            'iklim': '🌍 İklim &amp; Kuraklık Araştırmaları',
            'politika': '⚖️ Su Politikaları &amp; Yönetişim'
        """.strip()
        footer_sub_text = "Akademik araştırmalar, hakemli dergiler ve küresel su kurumlarından derlenen günlük dijital su gazetesi."
        live_feed_file = "feed.json"

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{portal_title_tag}</title>
    
    <!-- Meta tags for SEO & Feed Readers -->
    <meta name="description" content="{portal_sub_name} araştırmalarından derlenen modern gazete temalı haber portalı.">
    <link rel="alternate" type="application/rss+xml" title="{portal_name} (RSS 2.0)" href="{rss_url}">
    <link rel="alternate" type="application/atom+xml" title="{portal_name} (Atom)" href="{atom_url}">
    <link rel="alternate" type="application/feed+json" title="{portal_name} (JSON)" href="{json_url}">

    <!-- Google Fonts for Editorial Newspaper Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&family=Public+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,800;0,900;1,400;1,700&display=swap" rel="stylesheet">
    <!-- Leaflet & MarkerCluster for Geospatial Intelligence Atlas -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

    <!-- Theme Detection Script (Prevents flash of light theme on load) -->
    <script>
        (function() {{
            const saved = localStorage.getItem('su_portal_theme');
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (saved === 'dark' || (!saved && prefersDark)) {{
                document.documentElement.setAttribute('data-theme', 'dark');
            }} else {{
                document.documentElement.setAttribute('data-theme', 'light');
            }}
        }})();
    </script>

    <style>
        :root {{
            --paper-bg: #fdfdfc;
            --paper-card: #ffffff;
            --ink-black: #111827;
            --ink-dark: #1f2937;
            --ink-muted: #4b5563;
            --ink-light: #6b7280;
            --logo-color: #0b2545;
            --sublogo-color: #134074;
            --newspaper-navy: #0b2545;
            --newspaper-blue: #134074;
            --accent-red: #c1121f;
            --border-line: #d1d5db;
            --border-light: #e5e7eb;
            --border-divider: #111827;
            --border-double: 3px double #111827;
            --top-bar-bg: #0b1a30;
            --top-bar-color: #d1d5db;
            --ticker-bg: #ffffff;
            --nav-bg: #ffffff;
            --cat-btn-bg: #f1f5f9;
            --cat-btn-border: #cbd5e1;
            --cat-btn-color: #1f2937;
            --cat-btn-hover: #e2e8f0;
            --cat-btn-active-bg: #0b2545;
            --cat-btn-active-color: #ffffff;
            --search-bg: #ffffff;
            --search-border: #d1d5db;
            --search-color: #111827;
            --sidebar-card-bg: #ffffff;
            --sidebar-quote-bg: #f8fafc;
            --rss-box-bg: #f0fdf4;
            --rss-box-border: #bbf7d0;
            --modal-bg: #ffffff;
            --modal-header-bg: #f8fafc;
            --modal-text: #262626;
            --modal-footer-bg: #f8fafc;
            --footer-bg: #0b1a30;
            --footer-border: #0b2545;
            --footer-text: #9ca3af;
            --theme-toggle-bg: rgba(255, 255, 255, 0.12);
            --theme-toggle-color: #f1f5f9;
            --theme-toggle-border: rgba(255, 255, 255, 0.25);
            --shadow-subtle: 0 2px 6px rgba(0,0,0,0.03);
            --shadow-hover: 0 8px 18px rgba(0,0,0,0.07);
        }}

        [data-theme="dark"] {{
            --paper-bg: #0a0f1d;
            --paper-card: #131b2e;
            --ink-black: #f8fafc;
            --ink-dark: #e2e8f0;
            --ink-muted: #94a3b8;
            --ink-light: #64748b;
            --logo-color: #f8fafc;
            --sublogo-color: #38bdf8;
            --newspaper-navy: #38bdf8;
            --newspaper-blue: #60a5fa;
            --accent-red: #ef4444;
            --border-line: #1e293b;
            --border-light: #182235;
            --border-divider: #38bdf8;
            --border-double: 3px double #38bdf8;
            --top-bar-bg: #050811;
            --top-bar-color: #94a3b8;
            --ticker-bg: #131b2e;
            --nav-bg: #131b2e;
            --cat-btn-bg: #1a253a;
            --cat-btn-border: #293954;
            --cat-btn-color: #e2e8f0;
            --cat-btn-hover: #23324d;
            --cat-btn-active-bg: #2563eb;
            --cat-btn-active-color: #ffffff;
            --search-bg: #0b1120;
            --search-border: #293954;
            --search-color: #f8fafc;
            --sidebar-card-bg: #131b2e;
            --sidebar-quote-bg: #0e1626;
            --rss-box-bg: #062817;
            --rss-box-border: #14532d;
            --modal-bg: #131b2e;
            --modal-header-bg: #0e1626;
            --modal-text: #e2e8f0;
            --modal-footer-bg: #0e1626;
            --footer-bg: #050811;
            --footer-border: #1e293b;
            --footer-text: #64748b;
            --theme-toggle-bg: rgba(255, 255, 255, 0.15);
            --theme-toggle-color: #f8fafc;
            --theme-toggle-border: rgba(255, 255, 255, 0.25);
            --shadow-subtle: 0 2px 6px rgba(0,0,0,0.3);
            --shadow-hover: 0 8px 20px rgba(0,0,0,0.5);
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--paper-bg);
            color: var(--ink-black);
            font-family: 'Public Sans', -apple-system, sans-serif;
            line-height: 1.6;
            transition: background-color 0.25s ease, color 0.25s ease;
        }}

        /* Top Info Bar */
        .top-masthead-bar {{
            background: var(--top-bar-bg);
            color: var(--top-bar-color);
            font-size: 12px;
            padding: 8px 16px;
            border-bottom: 1px solid var(--border-line);
            transition: background-color 0.25s ease;
        }}
        .top-bar-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}
        .top-bar-left {{
            display: flex;
            align-items: center;
            flex-shrink: 0;
            white-space: nowrap;
            gap: 14px;
        }}
        .top-bar-left span, .top-bar-left a {{ margin-right: 0; }}
        .top-stat-link {{
            color: var(--top-bar-color);
            text-decoration: none;
            border-bottom: 1px dotted rgba(255, 255, 255, 0.4);
            padding-bottom: 1px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.2s ease;
        }}
        .top-stat-link:hover {{
            color: #38bdf8;
            border-bottom: 1px solid #38bdf8;
        }}
        .ext-link-icon {{
            font-size: 10px;
            opacity: 0.75;
            transition: transform 0.15s ease;
        }}
        .top-stat-link:hover .ext-link-icon {{
            transform: translate(1px, -1px);
            opacity: 1;
        }}
        .top-bar-right {{
            display: flex;
            align-items: center;
            flex-shrink: 0;
            gap: 10px;
        }}
        .top-search-box {{
            display: flex;
            align-items: center;
            position: relative;
        }}
        .top-search-box input {{
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 20px;
            font-size: 12px;
            width: 190px;
            transition: all 0.25s ease;
        }}
        .top-search-box input::placeholder {{
            color: rgba(255, 255, 255, 0.65);
        }}
        .top-search-box input:focus {{
            outline: none;
            width: 240px;
            background: rgba(255, 255, 255, 0.16);
            border-color: #38bdf8;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
        }}
        .lang-pill-switch {{
            display: inline-flex;
            align-items: center;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            user-select: none;
            gap: 2px;
        }}
        .lang-btn {{
            background: transparent;
            border: none;
            padding: 3px 10px;
            border-radius: 14px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
            color: var(--ink-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            line-height: 1.2;
        }}
        .lang-btn:hover {{
            color: var(--ink-primary);
        }}
        .lang-btn.active {{
            background: var(--accent-color, #0284c7);
            color: #ffffff !important;
            box-shadow: 0 1px 4px rgba(2, 132, 199, 0.35);
        }}
        .top-theme-toggle-btn {{
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.22);
            padding: 5px 11px;
            border-radius: 20px;
            font-size: 13.5px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            user-select: none;
            line-height: 1;
        }}
        .top-theme-toggle-btn:hover {{
            background: rgba(255, 255, 255, 0.22);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-1px);
        }}
        [data-theme="dark"] .top-search-box input {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.15);
        }}
        [data-theme="dark"] .top-theme-toggle-btn {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.18);
        }}

        /* Channel Switcher Tabs Bar */
        .channel-switcher-container {{
            background: var(--paper-bg);
            border-bottom: 1px solid var(--border-line);
            padding: 8px 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: background-color 0.25s ease, border-color 0.25s ease;
        }}
        .channel-switcher-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .channel-tab-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 20px;
            border-radius: 30px;
            font-size: 13.5px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-decoration: none;
            color: var(--cat-btn-color);
            background: var(--cat-btn-bg);
            border: 1px solid var(--cat-btn-border);
            transition: all 0.2s ease;
            user-select: none;
        }}
        .channel-tab-btn:hover {{
            background: var(--cat-btn-hover);
            transform: translateY(-1px);
        }}
        .channel-tab-btn.active {{
            background: var(--newspaper-navy) !important;
            color: #ffffff !important;
            border-color: var(--newspaper-navy) !important;
            box-shadow: 0 2px 10px rgba(11, 37, 69, 0.25);
        }}
        .channel-tab-badge {{
            background: rgba(0, 0, 0, 0.08);
            color: var(--ink-dark);
            font-size: 11px;
            font-weight: 800;
            padding: 1px 7px;
            border-radius: 10px;
        }}
        .channel-tab-btn.active .channel-tab-badge {{
            background: rgba(255, 255, 255, 0.22);
            color: #ffffff;
        }}
        [data-theme="dark"] .channel-tab-badge {{
            background: rgba(255, 255, 255, 0.12);
            color: #e2e8f0;
        }}


        /* Newspaper Header / Masthead */
        .newspaper-header {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 24px 16px 12px;
            text-align: center;
        }}
        .newspaper-motto {{
            font-family: 'Merriweather', serif;
            font-style: italic;
            font-size: 13px;
            color: var(--ink-muted);
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .newspaper-logo {{
            font-family: 'Playfair Display', 'Cinzel', serif;
            font-size: clamp(2.4rem, 6vw, 4.2rem);
            font-weight: 900;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--logo-color);
            margin: 4px 0;
            line-height: 1.1;
            transition: color 0.25s ease;
        }}
        .newspaper-sub-logo {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--sublogo-color);
            margin-bottom: 16px;
            transition: color 0.25s ease;
        }}
        .masthead-divider {{
            border-top: 1px solid var(--border-divider);
            border-bottom: 3px solid var(--border-divider);
            height: 4px;
            margin: 12px 0 16px;
            transition: border-color 0.25s ease;
        }}

        /* Bottom Screen Fixed Ticker Bar */
        body {{
            padding-bottom: 44px;
        }}
        .bottom-ticker-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 40px;
            z-index: 9999;
            display: flex;
            align-items: center;
            background: #0b1a30;
            border-top: 2px solid var(--bottom-ticker-border, #0284c7);
            box-shadow: 0 -4px 18px rgba(0, 0, 0, 0.4);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            user-select: none;
            transition: background 0.25s ease, border-color 0.25s ease;
        }}
        [data-theme="light"] .bottom-ticker-bar {{
            background: #0f172a;
            color: #f1f5f9;
        }}
        [data-theme="dark"] .bottom-ticker-bar {{
            background: #050914;
            color: #e2e8f0;
        }}
        .bottom-ticker-badge {{
            flex-shrink: 0;
            display: inline-flex;
            align-items: center;
            gap: 7px;
            height: 100%;
            padding: 0 16px;
            background: var(--bottom-ticker-badge-bg, linear-gradient(135deg, #0369a1, #0284c7));
            color: #ffffff;
            font-weight: 800;
            font-size: 11.5px;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            box-shadow: 3px 0 10px rgba(0, 0, 0, 0.25);
            z-index: 2;
        }}
        .ticker-live-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #22c55e;
            box-shadow: 0 0 8px #22c55e;
            animation: liveDotPulse 1.8s infinite;
        }}
        @keyframes liveDotPulse {{
            0% {{ transform: scale(0.9); opacity: 0.8; box-shadow: 0 0 2px #22c55e; }}
            50% {{ transform: scale(1.25); opacity: 1; box-shadow: 0 0 10px #22c55e, 0 0 14px #4ade80; }}
            100% {{ transform: scale(0.9); opacity: 0.8; box-shadow: 0 0 2px #22c55e; }}
        }}
        .bottom-ticker-marquee {{
            flex: 1;
            min-width: 0;
            height: 100%;
            overflow: hidden;
            position: relative;
            display: flex;
            align-items: center;
            mask-image: linear-gradient(to right, transparent, black 24px, black calc(100% - 24px), transparent);
            -webkit-mask-image: linear-gradient(to right, transparent, black 24px, black calc(100% - 24px), transparent);
        }}
        .bottom-ticker-track {{
            display: inline-flex;
            align-items: center;
            white-space: nowrap;
            will-change: transform;
            animation: bottomTickerScroll 160s linear infinite;
        }}
        .bottom-ticker-bar:hover .bottom-ticker-track {{
            animation-play-state: paused;
        }}
        @keyframes bottomTickerScroll {{
            0% {{
                transform: translateX(0);
            }}
            100% {{
                transform: translateX(-50%);
            }}
        }}
        .ticker-item {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            margin-right: 32px;
            cursor: pointer;
            color: #e2e8f0;
            font-size: 13px;
            font-weight: 500;
            text-decoration: none;
            transition: color 0.15s ease;
        }}
        .ticker-item:hover {{
            color: var(--bottom-ticker-accent, #38bdf8);
        }}
        .ticker-item:hover .ticker-text {{
            text-decoration: underline;
        }}
        .ticker-icon {{
            color: #f59e0b;
            font-size: 11px;
        }}
        .ticker-cat-tag {{
            font-size: 11px;
            font-weight: 700;
            color: var(--bottom-ticker-accent, #38bdf8);
            opacity: 0.95;
        }}
        .ticker-cat-turkey {{
            color: #f87171 !important;
            font-weight: 800 !important;
        }}
        .ticker-cat-academic {{
            color: #a78bfa !important;
            font-weight: 700 !important;
        }}
        .ticker-sep {{
            margin-left: 20px;
            color: rgba(255, 255, 255, 0.25);
            font-size: 13px;
        }}
        .bottom-ticker-controls {{
            flex-shrink: 0;
            display: flex;
            align-items: center;
            padding: 0 12px;
            height: 100%;
            background: rgba(0, 0, 0, 0.25);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 2;
        }}
        .btn-ticker-ctrl {{
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 13px;
            color: #cbd5e1;
            padding: 4px 6px;
            border-radius: 4px;
            transition: background 0.15s ease, color 0.15s ease, transform 0.1s ease;
        }}
        .btn-ticker-ctrl:hover {{
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
            transform: scale(1.1);
        }}


        /* Navigation Bar */
        .category-nav-bar {{
            max-width: 1240px;
            margin: 0 auto 24px;
            padding: 0 16px;
        }}
        .nav-inner {{
            background: var(--nav-bg);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
            transition: background-color 0.25s ease, border-color 0.25s ease;
        }}
        .category-pills {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .cat-btn {{
            background: var(--cat-btn-bg);
            border: 1px solid var(--cat-btn-border);
            padding: 7px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--cat-btn-color);
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }}
        .cat-btn:hover {{
            background: var(--cat-btn-hover);
            transform: translateY(-1px);
        }}
        .cat-btn.active {{
            background: var(--cat-btn-active-bg) !important;
            color: var(--cat-btn-active-color) !important;
            border-color: var(--cat-btn-active-bg) !important;
            box-shadow: 0 2px 8px rgba(11, 37, 69, 0.3);
        }}
        .empty-results-box {{
            grid-column: 1 / -1;
            background: var(--paper-card);
            border: 2px dashed var(--border-line);
            border-radius: 8px;
            padding: 48px 24px;
            text-align: center;
            margin: 20px 0;
            width: 100%;
        }}
        .empty-results-box .empty-icon {{
            font-size: 42px;
            margin-bottom: 12px;
        }}
        .empty-results-box h3 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.35rem;
            color: var(--newspaper-navy);
            margin-bottom: 8px;
        }}
        .empty-results-box p {{
            font-size: 13.5px;
            color: var(--ink-muted);
            max-width: 480px;
            margin: 0 auto 20px;
        }}
        .btn-reset-filter {{
            background: var(--newspaper-navy);
            color: white;
            border: none;
            padding: 10px 22px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .btn-reset-filter:hover {{
            background: var(--newspaper-blue);
        }}
        .news-badge {{
            cursor: pointer;
            transition: opacity 0.15s;
        }}
        .news-badge:hover {{
            opacity: 0.85;
        }}
        .hero-category-tag {{
            cursor: pointer;
            transition: opacity 0.15s;
        }}
        .hero-category-tag:hover {{
            opacity: 0.85;
        }}
        .nav-controls {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .search-box {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .search-box input {{
            padding: 6px 12px;
            background: var(--search-bg);
            color: var(--search-color);
            border: 1px solid var(--search-border);
            border-radius: 4px;
            font-size: 13px;
            width: 200px;
            transition: all 0.2s ease;
        }}
        .search-box input:focus {{
            outline: none;
            border-color: var(--newspaper-blue);
        }}
        .theme-toggle-btn-nav {{
            background: var(--cat-btn-bg);
            color: var(--ink-dark);
            border: 1px solid var(--cat-btn-border);
            padding: 6px 11px;
            border-radius: 6px;
            font-size: 15px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            user-select: none;
            line-height: 1;
        }}
        .theme-toggle-btn-nav:hover {{
            background: var(--cat-btn-hover);
            transform: translateY(-1px);
        }}

        /* Main Container */
        .portal-layout {{
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 16px;
        }}

        /* Hero / Main Headline */
        .main-headline-banner {{
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            background: var(--paper-card);
            border: 1px solid var(--border-line);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 28px;
            box-shadow: var(--shadow-subtle);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s, background-color 0.25s ease, border-color 0.25s ease;
        }}
        .main-headline-banner:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}
        .hero-image-col {{
            background-size: cover;
            background-position: center;
            min-height: 380px;
            position: relative;
        }}
        .hero-image-overlay {{
            position: absolute;
            bottom: 12px;
            left: 12px;
        }}
        .hero-category-tag {{
            background: var(--accent-red);
            color: white;
            font-size: 11px;
            font-weight: 800;
            padding: 5px 12px;
            border-radius: 3px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .hero-content-col {{
            padding: 32px 36px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .hero-meta {{
            font-size: 12px;
            color: var(--ink-light);
            margin-bottom: 12px;
            font-weight: 500;
        }}
        .hero-title {{
            font-family: 'Playfair Display', 'Merriweather', serif;
            font-size: clamp(1.4rem, 2.5vw, 2rem);
            font-weight: 800;
            line-height: 1.3;
            color: var(--ink-black);
            margin-bottom: 8px;
        }}
        .hero-title-en {{
            font-size: 12px;
            color: var(--ink-light);
            font-style: italic;
            margin-bottom: 16px;
        }}
        .hero-summary {{
            font-family: 'Merriweather', serif;
            font-size: 14.5px;
            color: var(--ink-dark);
            line-height: 1.65;
            margin-bottom: 24px;
        }}
        .hero-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            border-top: 1px solid var(--border-light);
            padding-top: 16px;
        }}
        .btn-hero-read {{
            background: var(--newspaper-navy);
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 4px;
            cursor: pointer;
        }}
        .hero-hint {{
            font-size: 11.5px;
            color: var(--ink-light);
        }}

        /* Turkey Water News Dedicated Priority Section */
        .turkey-priority-section {{
            background: var(--paper-card);
            border: 1px solid var(--border-line);
            border-top: 4px solid var(--accent-red);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 32px;
            box-shadow: var(--shadow-subtle);
            transition: background-color 0.25s ease, border-color 0.25s ease;
        }}
        [data-theme="dark"] .turkey-priority-section {{
            background: var(--paper-card);
            border-color: #1e293b;
            border-top-color: #ef4444;
        }}
        .turkey-section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-light);
            padding-bottom: 12px;
        }}
        .turkey-header-title-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .turkey-header-right {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .turkey-flag-pill {{
            background: #c1121f;
            color: #ffffff;
            font-size: 11px;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 4px;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }}
        .turkey-section-title {{
            font-family: 'Playfair Display', 'Merriweather', serif;
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--ink-black);
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .turkey-section-subtitle {{
            font-size: 12px;
            color: var(--ink-muted);
            font-weight: 500;
        }}
        .btn-turkey-all {{
            background: transparent;
            border: 1px solid #c1121f;
            color: #c1121f;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}
        .btn-turkey-all:hover {{
            background: #c1121f;
            color: #ffffff;
        }}
        [data-theme="dark"] .btn-turkey-all {{
            border-color: #ef4444;
            color: #f87171;
        }}
        [data-theme="dark"] .btn-turkey-all:hover {{
            background: #ef4444;
            color: #0b1a30;
        }}
        .turkey-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 18px;
        }}
        .turkey-card {{
            background: var(--paper-bg);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            cursor: pointer;
            box-shadow: var(--shadow-subtle);
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s, background-color 0.25s;
        }}
        .turkey-card:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
            border-color: #c1121f;
        }}
        [data-theme="dark"] .turkey-card {{
            background: #0d1527;
            border-color: #1e293b;
        }}
        [data-theme="dark"] .turkey-card:hover {{
            border-color: #ef4444;
        }}
        .turkey-card-img {{
            height: 155px;
            background-size: cover;
            background-position: center;
            position: relative;
        }}
        .turkey-badge {{
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(193, 18, 31, 0.92);
            color: #ffffff;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 3px;
            letter-spacing: 0.3px;
        }}
        .turkey-card-body {{
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}
        .turkey-card-meta {{
            font-size: 11px;
            color: var(--ink-light);
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .turkey-card-title {{
            font-family: 'Merriweather', serif;
            font-size: 13.5px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--ink-black);
            margin-bottom: 6px;
        }}
        .turkey-card:hover .turkey-card-title {{
            color: #c1121f;
        }}
        [data-theme="dark"] .turkey-card:hover .turkey-card-title {{
            color: #f87171;
        }}
        .turkey-card-excerpt {{
            font-size: 12px;
            color: var(--ink-muted);
            line-height: 1.45;
            margin-bottom: 12px;
            flex-grow: 1;
        }}
        .turkey-card-footer {{
            display: flex;
            justify-content: flex-end;
            border-top: 1px solid var(--border-light);
            padding-top: 8px;
            margin-top: auto;
        }}
        .turkey-read-btn {{
            font-size: 11.5px;
            font-weight: 700;
            color: #c1121f;
        }}
        [data-theme="dark"] .turkey-read-btn {{
            color: #f87171;
        }}

        /* Secondary Headlines Row */
        .sub-headlines-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 18px;
            margin-bottom: 36px;
        }}
        .sub-headline-card {{
            background: var(--paper-card);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            cursor: pointer;
            transition: all 0.2s, background-color 0.25s ease, border-color 0.25s ease;
            box-shadow: var(--shadow-subtle);
        }}
        .sub-headline-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}
        .sub-headline-img {{
            width: 140px;
            min-width: 140px;
            background-size: cover;
            background-position: center;
            position: relative;
        }}
        .sub-headline-content {{
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .news-badge {{
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(11, 37, 69, 0.9);
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 2px;
        }}
        .news-badge-turkey {{
            background: #c1121f !important;
            color: #ffffff !important;
            font-weight: 800 !important;
        }}
        .news-badge-academic {{
            background: #1e3a8a !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            border: 1px solid rgba(255, 255, 255, 0.35);
            box-shadow: 0 1px 4px rgba(30, 58, 138, 0.4);
        }}
        [data-theme="dark"] .news-badge-academic {{
            background: #2563eb !important;
            color: #ffffff !important;
        }}
        .news-date {{
            font-size: 11px;
            color: var(--ink-light);
            margin-bottom: 4px;
        }}
        .sub-headline-content h4 {{
            font-family: 'Merriweather', serif;
            font-size: 14px;
            font-weight: 700;
            line-height: 1.35;
            color: var(--ink-black);
            margin-bottom: 6px;
        }}
        .sub-headline-content p {{
            font-size: 12px;
            color: var(--ink-muted);
            line-height: 1.4;
        }}

        /* 2-Column Newspaper Section */
        .newspaper-columns {{
            display: grid;
            grid-template-columns: 2.3fr 1fr;
            gap: 28px;
        }}

        /* Section Headings */
        .section-headline {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--newspaper-navy);
            padding-bottom: 8px;
            margin-bottom: 20px;
        }}
        .section-headline h3 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.35rem;
            color: var(--newspaper-navy);
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .section-headline span {{
            font-size: 12px;
            color: var(--ink-light);
        }}

        /* Article Cards Grid */
        .articles-news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .news-grid-card {{
            background: var(--paper-card);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-subtle);
            transition: all 0.2s, background-color 0.25s ease, border-color 0.25s ease;
        }}
        .news-grid-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }}
        .card-img-wrap {{
            height: 170px;
            background-size: cover;
            background-position: center;
            position: relative;
            cursor: pointer;
        }}
        .card-body {{
            padding: 16px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}
        .card-meta {{
            font-size: 11px;
            color: var(--ink-light);
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .card-title {{
            font-family: 'Merriweather', serif;
            font-size: 15px;
            font-weight: 700;
            line-height: 1.4;
            color: var(--ink-black);
            margin-bottom: 4px;
            cursor: pointer;
        }}
        .card-title:hover {{
            color: var(--newspaper-blue);
        }}
        .card-title-en {{
            font-size: 11px;
            color: var(--ink-light);
            font-style: italic;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        .card-excerpt {{
            font-size: 12.5px;
            color: var(--ink-muted);
            line-height: 1.55;
            margin-bottom: 16px;
            flex-grow: 1;
        }}
        .card-action-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--border-light);
            padding-top: 10px;
            margin-top: auto;
        }}
        .btn-read-more {{
            background: none;
            border: none;
            color: var(--newspaper-blue);
            font-weight: 700;
            font-size: 12px;
            cursor: pointer;
            padding: 0;
        }}
        .btn-read-more:hover {{ text-decoration: underline; }}
        .link-original {{
            font-size: 11.5px;
            color: var(--ink-light);
            text-decoration: none;
        }}
        .link-original:hover {{ color: var(--ink-black); text-decoration: underline; }}

        /* Sidebar Cards */
        .sidebar-card {{
            background: var(--sidebar-card-bg);
            border: 1px solid var(--border-line);
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-subtle);
            transition: background-color 0.25s ease, border-color 0.25s ease;
        }}
        .sidebar-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.15rem;
            color: var(--newspaper-navy);
            border-bottom: 2px solid var(--newspaper-navy);
            padding-bottom: 6px;
            margin-bottom: 14px;
        }}
        .editorial-quote {{
            font-family: 'Merriweather', serif;
            font-size: 13.5px;
            font-style: italic;
            color: var(--ink-dark);
            border-left: 3px solid var(--newspaper-navy);
            background: var(--sidebar-quote-bg);
            padding: 12px 14px;
            border-radius: 4px;
            margin-bottom: 12px;
            line-height: 1.6;
        }}
        .editorial-author {{
            font-size: 12px;
            font-weight: 700;
            color: var(--ink-muted);
            text-align: right;
        }}

        /* Data stats infographic */
        .stat-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--border-light);
            font-size: 13px;
            color: var(--ink-dark);
        }}
        .stat-value {{
            font-weight: 800;
            color: var(--newspaper-navy);
            font-size: 15px;
        }}

        /* RSS box in sidebar */
        .sidebar-rss-box {{
            background: var(--rss-box-bg);
            border: 1px solid var(--rss-box-border);
            border-radius: 6px;
            padding: 16px;
            text-align: center;
        }}
        .rss-url-display {{
            background: var(--paper-card);
            border: 1px solid var(--rss-box-border);
            color: var(--ink-dark);
            padding: 6px 10px;
            font-family: monospace;
            font-size: 11px;
            border-radius: 4px;
            margin: 8px 0;
            word-break: break-all;
        }}
        .btn-copy-rss {{
            background: #16a34a;
            color: white;
            border: none;
            padding: 8px 14px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
        }}
        .btn-copy-rss:hover {{ background: #15803d; }}

        /* Modal / Article Reading Window */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 26, 48, 0.75);
            backdrop-filter: blur(4px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            padding: 20px;
        }}
        .modal-window {{
            background: var(--modal-bg);
            width: 100%;
            max-width: 820px;
            max-height: 90vh;
            border-radius: 8px;
            overflow-y: auto;
            border: 1px solid var(--border-line);
            box-shadow: 0 20px 40px rgba(0,0,0,0.35);
            display: flex;
            flex-direction: column;
            transition: background-color 0.25s ease;
        }}
        .modal-header {{
            padding: 16px 24px;
            background: var(--modal-header-bg);
            border-bottom: 1px solid var(--border-line);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .modal-header span {{ font-weight: 700; font-size: 13px; color: var(--newspaper-navy); }}
        .btn-close-modal {{
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: var(--ink-muted);
        }}
        .modal-body {{
            padding: 32px 36px;
        }}
        .modal-category-tag {{
            background: var(--newspaper-navy);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 3px;
            text-transform: uppercase;
            display: inline-block;
            margin-bottom: 12px;
        }}
        .modal-title-tr {{
            font-family: 'Playfair Display', serif;
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1.3;
            color: var(--ink-black);
            margin-bottom: 8px;
        }}
        .modal-title-en {{
            font-size: 13px;
            color: var(--ink-light);
            font-style: italic;
            margin-bottom: 18px;
        }}
        .modal-meta-bar {{
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: var(--ink-muted);
            border-top: 1px solid var(--border-light);
            border-bottom: 1px solid var(--border-light);
            padding: 10px 0;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }}
        .modal-img {{
            width: 100%;
            max-height: 380px;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 24px;
        }}
        .modal-text {{
            font-family: 'Merriweather', serif;
            font-size: 15.5px;
            color: var(--modal-text);
            line-height: 1.8;
            margin-bottom: 30px;
        }}
        .modal-footer {{
            border-top: 1px solid var(--border-line);
            padding: 16px 24px;
            background: var(--modal-footer-bg);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .btn-doi-link {{
            background: var(--newspaper-navy);
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
        }}
        .btn-doi-link:hover {{ background: var(--newspaper-blue); }}

        /* Footer */
        .newspaper-footer {{
            border-top: 3px solid var(--footer-border);
            background: var(--footer-bg);
            color: var(--footer-text);
            padding: 40px 16px;
            margin-top: 60px;
            transition: background-color 0.25s ease;
        }}
        .footer-inner {{
            max-width: 1240px;
            margin: 0 auto;
            text-align: center;
            font-size: 13px;
        }}
        .footer-inner h4 {{
            font-family: 'Playfair Display', serif;
            color: var(--ink-black);
            font-size: 1.4rem;
            margin-bottom: 8px;
        }}
        .footer-inner p {{ margin-bottom: 12px; }}

        /* Geospatial Intelligence Map Section */
        .newspaper-map-section {{
            margin-bottom: 75px !important;
            padding: 24px;
            background: var(--paper-card);
            border: 1px solid var(--border-line);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            position: relative;
        }}
        [data-theme="dark"] .newspaper-map-section {{
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
        }}
        .map-section-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 18px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-line);
            flex-wrap: wrap;
        }}
        .map-title-group {{
            flex: 1;
            min-width: 280px;
        }}
        .map-badge-tag {{
            display: inline-block;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.8px;
            color: #0284c7;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        [data-theme="dark"] .map-badge-tag {{
            color: #38bdf8;
        }}
        .map-section-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 24px;
            font-weight: 800;
            color: var(--ink-dark);
            margin: 0 0 8px 0;
            line-height: 1.25;
        }}
        .map-section-desc {{
            font-size: 13.5px;
            line-height: 1.55;
            color: var(--ink-light);
            margin: 0;
            max-width: 860px;
        }}
        .map-header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .btn-portal-ext-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff !important;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 700;
            text-decoration: none;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
            transition: all 0.2s ease;
        }}
        .btn-portal-ext-link:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5);
            color: #ffffff !important;
        }}
        .map-toolbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 14px;
            flex-wrap: wrap;
        }}
        .map-toolbar-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .btn-toggle-layers-bar {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 14px;
            border-radius: 8px;
            background: var(--paper-bg);
            border: 1px solid var(--border-line);
            color: var(--ink-dark);
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.18s ease;
        }}
        .btn-toggle-layers-bar:hover {{
            border-color: #0284c7;
            color: #0284c7;
            transform: translateY(-1px);
        }}
        .layer-pill-active {{
            background: rgba(2, 132, 199, 0.12);
            color: #0284c7;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            border: 1px solid rgba(2, 132, 199, 0.25);
        }}
        [data-theme="dark"] .layer-pill-active {{
            background: rgba(56, 189, 248, 0.18);
            color: #38bdf8;
            border-color: rgba(56, 189, 248, 0.35);
        }}
        .layer-dot {{
            width: 9px;
            height: 9px;
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
        }}
        .layer-dot-water {{ background: #0284c7; box-shadow: 0 0 6px rgba(2, 132, 199, 0.6); }}
        .layer-dot-agri {{ background: #16a34a; box-shadow: 0 0 6px rgba(22, 163, 74, 0.6); }}
        .layer-dot-livestock {{ background: #d97706; box-shadow: 0 0 6px rgba(217, 119, 6, 0.6); }}
        .layer-dot-agreements {{ background: #2563eb; box-shadow: 0 0 6px rgba(37, 99, 235, 0.6); }}
        .layer-dot-conflicts {{ background: #dc2626; box-shadow: 0 0 6px rgba(220, 38, 38, 0.6); }}
        .layer-dot-basins {{ background: #0891b2; box-shadow: 0 0 6px rgba(8, 145, 178, 0.6); }}
        .layer-count {{
            font-size: 10.5px;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.12);
            padding: 2px 7px;
            border-radius: 10px;
            color: #cbd5e1;
        }}
        .map-view-controls {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-map-view {{
            background: var(--paper-bg);
            border: 1px solid var(--border-line);
            color: var(--ink-dark);
            padding: 6px 11px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .btn-map-view:hover {{
            border-color: #0284c7;
            background: var(--cat-btn-hover);
        }}
        .map-canvas-wrapper {{
            position: relative;
            width: 100%;
            height: 580px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border-line);
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.08);
        }}
        .map-canvas-wrapper.fullscreen-mode {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            height: 100vh !important;
            z-index: 10000;
            border-radius: 0;
            border: none;
        }}
        .portal-leaflet-map {{
            width: 100%;
            height: 100%;
            background: #1e293b;
        }}

        /* ==========================================
           COLLAPSIBLE LEFT SIDE PANEL (GIS LAYERS)
           ========================================== */
        .map-side-panel {{
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            width: 320px;
            max-width: 88%;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-right: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
            z-index: 1002;
            display: flex;
            flex-direction: column;
            transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
            transform: translateX(-100%);
        }}
        .map-side-panel.open {{
            transform: translateX(0);
        }}
        .side-panel-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 13px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(30, 41, 59, 0.5);
        }}
        .side-panel-title-wrap {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .side-panel-icon {{
            font-size: 15px;
        }}
        .side-panel-title {{
            margin: 0;
            font-size: 13.5px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: #ffffff;
            text-transform: uppercase;
        }}
        .btn-close-side-panel {{
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #cbd5e1;
            width: 26px;
            height: 26px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 14px;
            font-weight: 700;
            transition: all 0.15s ease;
        }}
        .btn-close-side-panel:hover {{
            background: rgba(239, 68, 68, 0.8);
            color: #ffffff;
        }}
        .side-panel-body {{
            flex: 1;
            overflow-y: auto;
            padding: 14px 16px;
        }}
        .side-panel-body::-webkit-scrollbar {{
            width: 6px;
        }}
        .side-panel-body::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
        }}
        .panel-section {{
            margin-bottom: 16px;
        }}
        .panel-section-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-bottom: 8px;
            padding-bottom: 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .panel-section-tag {{
            font-size: 10.5px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: #38bdf8;
            text-transform: uppercase;
        }}
        .panel-section-help {{
            font-size: 10px;
            color: #94a3b8;
        }}
        .panel-layer-card {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 11px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 7px;
            cursor: pointer;
            user-select: none;
            transition: all 0.18s ease;
        }}
        .panel-layer-card:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }}
        .panel-layer-card.active {{
            background: rgba(2, 132, 199, 0.18);
            border-color: rgba(56, 189, 248, 0.5);
        }}
        .layer-card-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .layer-card-left input[type="checkbox"] {{
            width: 15px;
            height: 15px;
            accent-color: #0284c7;
            cursor: pointer;
            margin: 0;
        }}
        .layer-card-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        .layer-name {{
            font-size: 12.5px;
            font-weight: 700;
            color: #f1f5f9;
            line-height: 1.3;
        }}
        .layer-desc {{
            font-size: 10.5px;
            color: #94a3b8;
            line-height: 1.25;
        }}
        .panel-footer-actions {{
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .btn-panel-action {{
            width: 100%;
            padding: 8px 12px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #e2e8f0;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .btn-panel-action:hover {{
            background: rgba(2, 132, 199, 0.25);
            border-color: #38bdf8;
            color: #ffffff;
        }}

        /* Floating Open Button on Map Canvas */
        .map-canvas-toggle-btn {{
            position: absolute;
            top: 14px;
            left: 56px;
            z-index: 1000;
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            padding: 7px 13px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
            transition: all 0.2s ease;
        }}
        .map-canvas-toggle-btn:hover {{
            background: rgba(2, 132, 199, 0.95);
            border-color: #38bdf8;
            transform: translateY(-1px);
        }}
        .map-canvas-toggle-btn .toggle-badge {{
            background: #0284c7;
            color: #fff;
            font-size: 10px;
            font-weight: 800;
            padding: 1px 6px;
            border-radius: 10px;
        }}

        /* Floating Search in Map (Top-Right) */
        .map-search-bar {{
            position: absolute;
            top: 14px;
            right: 14px;
            z-index: 999;
            display: flex;
            align-items: center;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 4px 6px 4px 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
            max-width: 320px;
        }}
        .map-search-bar input {{
            background: transparent;
            border: none;
            color: #ffffff;
            font-size: 12.5px;
            outline: none;
            width: 190px;
            font-family: inherit;
        }}
        .map-search-bar input::placeholder {{
            color: #94a3b8;
        }}
        .map-search-bar button {{
            background: #0284c7;
            border: none;
            color: #fff;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.15s ease;
        }}
        .map-search-bar button:hover {{
            background: #0369a1;
        }}

        .map-loading-overlay {{
            position: absolute;
            top: 58px;
            right: 14px;
            z-index: 1000;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(6px);
            color: #ffffff;
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.15);
        }}
        .map-spinner {{
            width: 14px;
            height: 14px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-top-color: #38bdf8;
            border-radius: 50%;
            animation: mapSpin 0.7s linear infinite;
        }}
        @keyframes mapSpin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Custom Cluster Markers (Channel Themed - NO LIME GREEN!) */
        .portal-cluster-wrapper {{
            background: transparent !important;
            border: none !important;
        }}
        .portal-cluster-badge {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 12.5px;
            font-weight: 800;
            border: 2px solid rgba(255, 255, 255, 0.95);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
            cursor: pointer;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            user-select: none;
        }}
        .portal-cluster-badge:hover {{
            transform: scale(1.18);
            z-index: 10000 !important;
        }}
        .cluster-water {{
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            box-shadow: 0 4px 16px rgba(2, 132, 199, 0.6);
        }}
        .cluster-agri {{
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
            box-shadow: 0 4px 16px rgba(22, 163, 74, 0.6);
        }}
        .cluster-livestock {{
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            box-shadow: 0 4px 16px rgba(217, 119, 6, 0.6);
        }}
        .cluster-agreements {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.6);
        }}
        .cluster-conflicts {{
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.6);
        }}
        .cluster-badge-icon {{
            font-size: 11px;
            line-height: 1;
        }}
        .cluster-badge-count {{
            font-size: 12.5px;
            letter-spacing: -0.3px;
        }}

        /* Custom Popup Styling */
        .leaflet-popup-content-wrapper {{
            border-radius: 10px !important;
            padding: 4px !important;
            box-shadow: 0 8px 26px rgba(0, 0, 0, 0.3) !important;
        }}
        .portal-popup-card {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 12px;
            line-height: 1.45;
            color: #1e293b;
            min-width: 250px;
            max-width: 300px;
        }}
        .portal-popup-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
            gap: 6px;
        }}
        .popup-channel-badge {{
            color: #ffffff;
            font-size: 10px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 4px;
            letter-spacing: 0.3px;
        }}
        .popup-cat-badge {{
            font-size: 11px;
            font-weight: 700;
            color: #0369a1;
        }}
        .portal-popup-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: #0f172a;
            margin: 0 0 6px 0;
            line-height: 1.35;
        }}
        .portal-popup-meta {{
            font-size: 11px;
            color: #64748b;
            margin-bottom: 6px;
            background: #f8fafc;
            padding: 4px 6px;
            border-radius: 4px;
        }}
        .portal-popup-desc {{
            font-size: 11.5px;
            color: #334155;
            line-height: 1.4;
            margin: 0 0 10px 0;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .btn-map-popup-read {{
            display: block;
            width: 100%;
            background: #0284c7;
            color: #ffffff;
            border: none;
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            text-align: center;
            transition: background 0.15s ease;
        }}
        .btn-map-popup-read:hover {{
            background: #0369a1;
        }}

        @media (max-width: 768px) {{
            .map-section-header {{
                flex-direction: column;
                align-items: stretch;
            }}
            .map-toolbar {{
                flex-direction: column;
                align-items: stretch;
            }}
            .map-canvas-wrapper {{
                height: 400px;
            }}

        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .main-headline-banner {{ grid-template-columns: 1fr; }}
            .newspaper-columns {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 860px) {{
            .top-bar-inner {{
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                gap: 8px;
            }}
            .top-bar-left {{
                font-size: 11px;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .top-bar-right {{
                gap: 6px;
            }}
            .top-search-box input {{
                width: 140px;
            }}
            .top-search-box input:focus {{
                width: 170px;
            }}
            body {{
                padding-bottom: 40px;
            }}
            .bottom-ticker-bar {{
                height: 36px;
            }}
            .bottom-ticker-badge {{
                padding: 0 10px;
                font-size: 10.5px;
                gap: 5px;
            }}
            .ticker-item {{
                font-size: 12px;
                margin-right: 22px;
            }}
            .bottom-ticker-controls {{
                padding: 0 8px;
            }}
        }}
    </style>
</head>
<body>

    <!-- Top Bar -->
    <div class="top-masthead-bar">
        <div class="top-bar-inner">
            <div class="top-bar-left">
                <span id="topBarDate">🗓️ {today_str}</span>
                <span id="topStatContainer">{top_stat_html}</span>
            </div>
            <div class="top-bar-right">
                <div class="lang-pill-switch" id="langPillSwitch" title="Dil Seçimi / Select Language">
                    <button type="button" class="lang-btn active" id="btnLangTR" onclick="setPortalLanguage('tr')">TR</button>
                    <button type="button" class="lang-btn" id="btnLangEN" onclick="setPortalLanguage('en')">EN</button>
                </div>
                <div class="top-search-box">
                    <input type="text" id="searchInput" placeholder="🔍 Başlıklarda ara..." oninput="filterSearch()" aria-label="Haberlerde ara">
                </div>
                <button type="button" id="themeToggleBtn" class="top-theme-toggle-btn" onclick="toggleTheme()" title="Gece / Gündüz Temasını Değiştir" aria-label="Temayı Değiştir">
                    <span class="theme-icon">🌙</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Channel Switcher Tabs -->
    {channel_tabs_html}

    <!-- Masthead -->
    <header class="newspaper-header">
        <div class="newspaper-motto" id="newspaperMotto">{portal_motto}</div>
        <h1 class="newspaper-logo" id="newspaperLogo">{portal_name}</h1>
        <div class="newspaper-sub-logo" id="newspaperSubLogo">{portal_sub_name}</div>
        <div class="masthead-divider"></div>
    </header>

    <!-- Category Nav Bar -->
    <nav class="category-nav-bar" id="categoryNavBar">
        <div class="nav-inner">
            <div class="category-pills" id="categoryPills">
                {category_pills_html}
            </div>
        </div>
    </nav>

    <!-- Main Layout -->
    <main class="portal-layout">
        
        <!-- Hero / Gunun Manseti -->
        {hero_html}


        <!-- Sub Headlines (Surmansetler) -->
        <section class="sub-headlines-grid" id="subHeadlinesSection">
            {secondary_html}
        </section>

        <!-- Interactive Map Section -->
        {interactive_map_html}

        <!-- Columns Section -->
        <div class="newspaper-columns">
            
            <!-- Left Main Column: News Grid -->
            <div class="main-articles-col">
                <div class="section-headline" id="mainNewsSection">
                    <h3 id="sectionTitle">{section_title}</h3>
                    <span id="sectionCount">Toplam <strong>{len(items)}</strong> makale</span>
                </div>
                
                <div class="articles-news-grid" id="newsGrid">
                    <!-- Empty State Box -->
                    <div id="noResultsState" class="empty-results-box" style="display: none;">
                        <div class="empty-icon">{empty_icon}</div>
                        <h3 id="emptyTitle">Bu kategoride henüz haber bulunmuyor</h3>
                        <p id="emptyDesc">Seçilen kriterlerle eşleşen makale bulunamadı. Yeni bültenler taranmaya devam etmektedir.</p>
                        <button type="button" class="btn-reset-filter" onclick="filterCategory('all')">Tüm Haberleri Göster</button>
                    </div>

                    {grid_html}
                </div>
            </div>

            <!-- Right Sidebar: Editorial & Infographics -->
            <aside class="newspaper-sidebar">
                
                <!-- Günün Sözü (Su / Tarım Yönetimi Öğütleri) -->
                <div class="sidebar-card">
                    <h4 class="sidebar-title" id="dailyQuoteTitle" data-i18n="daily_quote_title">Günün Sözü</h4>
                    <div class="editorial-quote" id="dailyQuoteText">
                        "{quote_text}"
                    </div>
                    <div class="editorial-author">&mdash; <span id="dailyQuoteAuthor">{quote_author}</span> &bull; <span style="font-weight:normal; color:var(--ink-light);" id="dailyQuoteCat">{quote_cat}</span></div>
                </div>

                <!-- Stats Infographic -->
                {sidebar_stats_html}

                <!-- Live RSS Subscription Card -->
                <div class="sidebar-card sidebar-rss-box">
                    <h4 style="color:#166534; font-size:15px; margin-bottom:6px;">📡 Sabit RSS Kaynağınız</h4>
                    <p style="font-size:12px; color:#14532d;">Feedly, Inoreader, Outlook veya istediğiniz okuyucuya doğrudan ekleyin:</p>
                    <div class="rss-url-display" id="sidebarRssUrl">{rss_url}</div>
                    <button class="btn-copy-rss" onclick="navigator.clipboard.writeText(document.getElementById('sidebarRssUrl').innerText); alert('Sabit RSS linki kopyalandı!');">
                        📋 RSS Linkini Kopyala
                    </button>
                    <div style="margin-top:10px; font-size:11px; color:#15803d;">
                        <a href="{atom_url}" target="_blank" style="color:#15803d; font-weight:bold;">Atom 1.0</a> &bull; 
                        <a href="{json_url}" target="_blank" style="color:#15803d; font-weight:bold;">JSON Feed</a>
                    </div>
                </div>

                <!-- Sources Card -->
                {sidebar_sources_html}

            </aside>
        </div>

    </main>

    <!-- Reading Modal -->
    <div class="modal-backdrop" id="articleModal" onclick="closeArticleModal(event)">
        <div class="modal-window" onclick="event.stopPropagation()">
            <div class="modal-header">
                <span id="modalHeaderCategory">BİLİMSEL YAYIN &bull; {portal_name}</span>
                <button class="btn-close-modal" onclick="closeArticleModal()">&times;</button>
            </div>
            <div class="modal-body">
                <span class="modal-category-tag" id="modalBadge">Kategori</span>
                <h2 class="modal-title-tr" id="modalTitleTr">Türkçe Başlık</h2>
                <h4 class="modal-title-en" id="modalTitleEn">Orijinal Başlık</h4>
                
                <div class="modal-meta-bar">
                    <span id="modalDate">📅 Tarih</span>
                    <span id="modalSource">📰 Kaynak</span>
                    <span id="modalAuthor">✍️ Yazar</span>
                </div>

                <img src="" id="modalImg" class="modal-img" alt="Haber Görseli" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1544717305-2782549b5136?w=900&q=80';">

                <div class="modal-text" id="modalContent">
                    Haber içeriği yükleniyor...
                </div>
            </div>
            <div class="modal-footer">
                <button class="cat-btn" onclick="window.print()">🖨️ Sayfayı Yazdır</button>
                <a href="#" id="modalDoiLink" target="_blank" rel="noopener noreferrer" class="btn-doi-link">
                    Kaynağı Aç
                </a>
            </div>
        </div>
    </div>

    <!-- Newspaper Footer -->
    <footer class="newspaper-footer">
        <div class="footer-inner">
            <h4>{portal_name}</h4>
            <p>{footer_sub_text}</p>
            <p style="font-size:11.5px; opacity:0.75;">
                Otomasyon: GitHub Actions ile 30 dakikada bir güncellenir &bull; Son Güncelleme: {last_updated} &bull; Depo: mserman90/suhaber
            </p>
        </div>
    </footer>

    <!-- Interactive Scripts -->
    <script>
        const articlesData = {json_portal_data};
        const waterMapData = {json_water_map};
        const agriMapData = {json_agri_map};
        const livestockMapData = {json_livestock_map};

        let portalMap = null;
        let portalTileLayer = null;
        const mapLayers = {{}};

        function escapeMapHtml(str) {{
            if (!str) return '';
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        }}

        function createChannelClusterIcon(cluster, symbol, gradientClass) {{
            const count = cluster.getChildCount();
            return L.divIcon({{
                html: `<div class="portal-cluster-badge ${{gradientClass}}">
                    <span class="cluster-badge-icon">${{symbol}}</span>
                    <span class="cluster-badge-count">${{count}}</span>
                </div>`,
                className: 'portal-cluster-wrapper',
                iconSize: [42, 42],
                iconAnchor: [21, 21]
            }});
        }}

        function buildNewsMarkerIcon(color, symbol) {{
            return L.divIcon({{
                className: '',
                html: `<div style="
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background: ${{color}};
                    border: 2px solid #ffffff;
                    box-shadow: 0 0 8px ${{color}}cc, 0 2px 5px rgba(0,0,0,0.4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    cursor: pointer;
                    user-select: none;
                ">${{symbol}}</div>`,
                iconSize: [24, 24],
                iconAnchor: [12, 12],
                popupAnchor: [0, -12]
            }});
        }}

        function buildNewsPopup(item, channelBadge, channelBg) {{
            return `
                <div class="portal-popup-card">
                    <div class="portal-popup-header">
                        <span class="popup-channel-badge" style="background:${{channelBg}};">${{channelBadge}}</span>
                        <span class="popup-cat-badge">[${{item.category}}]</span>
                    </div>
                    <h4 class="portal-popup-title">${{escapeMapHtml(item.title)}}</h4>
                    <div class="portal-popup-meta">
                        <span>📅 ${{escapeMapHtml(item.date)}}</span> &bull; <span>📍 ${{escapeMapHtml(item.loc || 'Bölge')}}</span>
                    </div>
                    <p class="portal-popup-desc">${{escapeMapHtml(item.summary)}}...</p>
                    <button type="button" class="btn-map-popup-read" onclick="openArticleModal(${{item.id}})">
                        Tam Haberi ve Analizi Oku &rarr;
                    </button>
                </div>
            `;
        }}

        function getTileLayerConfig(isDark) {{
            if (isDark) {{
                return {{
                    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}',
                    attr: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ | <a href="https://mserman90.github.io/water-agreements-portal/" target="_blank">TFDD / OSU</a>',
                    subdomains: ''
                }};
            }} else {{
                return {{
                    url: 'https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
                    attr: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://mserman90.github.io/water-agreements-portal/" target="_blank">TFDD / OSU</a>',
                    subdomains: 'abc'
                }};
            }}
        }}

        function initPortalMap() {{
            const mapEl = document.getElementById('portalLeafletMap');
            if (!mapEl || typeof L === 'undefined') return;

            const isDark = (document.documentElement.getAttribute('data-theme') === 'dark');
            const tileCfg = getTileLayerConfig(isDark);

            portalMap = L.map('portalLeafletMap', {{
                center: [38.5, 35.0],
                zoom: 6,
                minZoom: 2,
                maxZoom: 18,
                scrollWheelZoom: true
            }});

            portalTileLayer = L.tileLayer(tileCfg.url, {{
                attribution: tileCfg.attr,
                subdomains: tileCfg.subdomains,
                maxZoom: 18
            }}).addTo(portalMap);

            window.portalMapInstance = portalMap;
            window.portalTileLayer = portalTileLayer;

            // 1. Water News Layer (DEFAULT: ACTIVE / VISIBLE)
            const waterCluster = L.markerClusterGroup({{
                chunkedLoading: true,
                maxClusterRadius: 40,
                showCoverageOnHover: false,
                spiderfyOnMaxZoom: true,
                iconCreateFunction: (c) => createChannelClusterIcon(c, '💧', 'cluster-water')
            }});
            const waterIcon = buildNewsMarkerIcon('#0284c7', '💧');
            waterMapData.forEach(item => {{
                if (!item.lat || !item.lng) return;
                const marker = L.marker([item.lat, item.lng], {{ icon: waterIcon, title: item.title }});
                marker.bindPopup(buildNewsPopup(item, '💧 SU GÜNDEMİ', '#0284c7'));
                waterCluster.addLayer(marker);
            }});
            portalMap.addLayer(waterCluster);
            mapLayers['water'] = waterCluster;

            // 2. Agriculture News Layer (Toggleable)
            const agriCluster = L.markerClusterGroup({{
                chunkedLoading: true,
                maxClusterRadius: 40,
                showCoverageOnHover: false,
                spiderfyOnMaxZoom: true,
                iconCreateFunction: (c) => createChannelClusterIcon(c, '🌾', 'cluster-agri')
            }});
            const agriIcon = buildNewsMarkerIcon('#16a34a', '🌾');
            agriMapData.forEach(item => {{
                if (!item.lat || !item.lng) return;
                const marker = L.marker([item.lat, item.lng], {{ icon: agriIcon, title: item.title }});
                marker.bindPopup(buildNewsPopup(item, '🌾 TARIM GÜNDEMİ', '#16a34a'));
                agriCluster.addLayer(marker);
            }});
            mapLayers['agri'] = agriCluster;

            // 3. Livestock News Layer (Toggleable)
            const livestockCluster = L.markerClusterGroup({{
                chunkedLoading: true,
                maxClusterRadius: 40,
                showCoverageOnHover: false,
                spiderfyOnMaxZoom: true,
                iconCreateFunction: (c) => createChannelClusterIcon(c, '🐄', 'cluster-livestock')
            }});
            const livestockIcon = buildNewsMarkerIcon('#d97706', '🐄');
            livestockMapData.forEach(item => {{
                if (!item.lat || !item.lng) return;
                const marker = L.marker([item.lat, item.lng], {{ icon: livestockIcon, title: item.title }});
                marker.bindPopup(buildNewsPopup(item, '🐄 HAYVANCILIK GÜNDEMİ', '#d97706'));
                livestockCluster.addLayer(marker);
            }});
            mapLayers['livestock'] = livestockCluster;
            updateActiveLayersBadges();
            toggleMapSidePanel(false);
        }}

        function executeMapSearch() {{
            if (!portalMap) return;
            const inp = document.getElementById('mapSearchInput');
            if (!inp || !inp.value.trim()) return;
            const q = inp.value.trim().toLowerCase();

            // Check news data
            const allItems = [...waterMapData, ...agriMapData, ...livestockMapData];
            const match = allItems.find(it => (it.loc && it.loc.toLowerCase().includes(q)) || (it.title && it.title.toLowerCase().includes(q)));
            if (match && match.lat && match.lng) {{
                portalMap.flyTo([match.lat, match.lng], 9, {{ duration: 1.2 }});
                return;
            }}

            // Common preset coordinates for quick search
            const presets = {{
                'fırat': [37.55, 38.5, 8], 'dicle': [37.88, 40.5, 8], 'gap': [37.3, 39.0, 8],
                'ankara': [39.93, 32.85, 9], 'istanbul': [41.01, 28.98, 9], 'izmir': [38.42, 27.14, 9],
                'konya': [37.87, 32.49, 9], 'adana': [37.00, 35.32, 9], 'antalya': [36.88, 30.7, 9],
                'nil': [15.5, 32.55, 6], 'ren': [50.93, 6.96, 6], 'tuna': [44.6, 22.0, 6],
                'singur': [17.75, 78.12, 10], 'çukurova': [36.95, 35.4, 8], 'harran': [36.87, 39.02, 9]
            }};
            for (const [key, coords] of Object.entries(presets)) {{
                if (key.includes(q) || q.includes(key)) {{
                    portalMap.flyTo([coords[0], coords[1]], coords[2], {{ duration: 1.2 }});
                    return;
                }}
            }}
        }}

function toggleMapSidePanel(forceState) {{
            const panel = document.getElementById('mapSidePanel');
            const toggleBtn = document.getElementById('mapCanvasToggleBtn');
            if (!panel) return;
            if (typeof forceState === 'boolean') {{
                if (forceState) panel.classList.add('open');
                else panel.classList.remove('open');
            }} else {{
                panel.classList.toggle('open');
            }}
            const isOpen = panel.classList.contains('open');
            if (toggleBtn) {{
                toggleBtn.style.display = isOpen ? 'none' : 'inline-flex';
            }}
        }}

        function updateActiveLayersBadges() {{
            const layerIds = ['water', 'agri', 'livestock', 'agreements', 'conflicts', 'basins'];
            const active = [];
            layerIds.forEach(id => {{
                const chk = document.getElementById('layer' + id.charAt(0).toUpperCase() + id.slice(1) + 'Check');
                if (chk && chk.checked) active.push(id);
            }});
            const count = active.length;
            const canvasBadge = document.getElementById('canvasActiveBadge');
            const barBadge = document.getElementById('activeLayersBadge');
            if (canvasBadge) canvasBadge.innerText = count;
            if (barBadge) {{
                if (count === 1 && active[0] === 'water') {{
                    barBadge.innerText = '💧 Su Gündemi Aktif';
                }} else if (count === 0) {{
                    barBadge.innerText = 'Katmanlar Kapalı';
                }} else {{
                    barBadge.innerText = count + ' Katman Aktif';
                }}
            }}
        }}

        function resetToDefaultLayer() {{
            const otherIds = ['agri', 'livestock', 'agreements', 'conflicts', 'basins'];
            otherIds.forEach(id => {{
                const chk = document.getElementById('layer' + id.charAt(0).toUpperCase() + id.slice(1) + 'Check');
                const card = document.getElementById('layerBtn_' + id);
                if (chk && chk.checked) {{
                    chk.checked = false;
                    if (card) card.classList.remove('active');
                    if (mapLayers[id] && portalMap) portalMap.removeLayer(mapLayers[id]);
                }}
            }});

            const waterChk = document.getElementById('layerWaterCheck');
            const waterCard = document.getElementById('layerBtn_water');
            if (waterChk && !waterChk.checked) {{
                waterChk.checked = true;
                if (waterCard) waterCard.classList.add('active');
                if (mapLayers['water'] && portalMap) portalMap.addLayer(mapLayers['water']);
            }}
            updateActiveLayersBadges();
        }}

        async function toggleMapLayer(layerId) {{
            if (!portalMap) return;
            const chk = document.getElementById('layer' + layerId.charAt(0).toUpperCase() + layerId.slice(1) + 'Check');
            const btn = document.getElementById('layerBtn_' + layerId);
            const isChecked = chk ? chk.checked : false;

            if (btn) {{
                if (isChecked) btn.classList.add('active');
                else btn.classList.remove('active');
            }}

            const loader = document.getElementById('mapLoadingIndicator');
            const loaderText = document.getElementById('mapLoadingText');

            if (layerId === 'water' || layerId === 'agri' || layerId === 'livestock') {{
                const cluster = mapLayers[layerId];
                if (!cluster) return;
                if (isChecked) {{
                    portalMap.addLayer(cluster);
                }} else {{
                    portalMap.removeLayer(cluster);
                }}
                updateActiveLayersBadges();
                return;
            }}

            if (layerId === 'agreements') {{
                if (!isChecked) {{
                    if (mapLayers['agreements']) portalMap.removeLayer(mapLayers['agreements']);
                    updateActiveLayersBadges();
                    return;
                }}
                if (mapLayers['agreements']) {{
                    portalMap.addLayer(mapLayers['agreements']);
                    return;
                }}
                // Fetch agreements
                if (loader) {{ loaderText.innerText = '3.059 Sınır Aşan Su Anlaşması yükleniyor...'; loader.style.display = 'flex'; }}
                try {{
                    let res = await fetch('data/agreements.min.json');
                    if (!res.ok) res = await fetch('https://mserman90.github.io/water-agreements-portal/data/agreements.min.json');
                    const agreements = await res.json();
                    const cluster = L.markerClusterGroup({{ chunkedLoading: true, maxClusterRadius: 45, iconCreateFunction: (c) => createChannelClusterIcon(c, '🌊', 'cluster-agreements') }});
                    const icon = L.divIcon({{
                        className: '',
                        html: '<div style="width:11px;height:11px;border-radius:50%;background:#2563eb;border:1.5px solid #fff;box-shadow:0 0 6px rgba(37,99,235,0.8);"></div>',
                        iconSize: [11, 11],
                        iconAnchor: [5, 5]
                    }});
                    agreements.forEach(a => {{
                        if (!a.latitude || !a.longitude) return;
                        const marker = L.marker([a.latitude, a.longitude], {{ icon, title: a.name }});
                        marker.bindPopup(`
                            <div class="portal-popup-card">
                                <div class="portal-popup-header">
                                    <span class="popup-channel-badge" style="background:#2563eb;">🌊 ULUSLARARASI ANLAŞMA</span>
                                    <span class="popup-cat-badge">📅 ${{a.year || ''}}</span>
                                </div>
                                <h4 class="portal-popup-title">${{escapeMapHtml(a.name)}}</h4>
                                <div class="portal-popup-meta">
                                    <div>📍 <b>Ülkeler:</b> ${{escapeMapHtml(a.country || '')}}</div>
                                    <div>🌊 <b>Havza:</b> ${{escapeMapHtml(a.basin || '')}}</div>
                                    <div>📋 <b>Konu:</b> ${{escapeMapHtml(a.purpose || '')}}</div>
                                </div>
                                <a href="https://mserman90.github.io/water-agreements-portal/" target="_blank" rel="noopener noreferrer" class="btn-map-popup-read" style="text-decoration:none;">
                                    🏛️ Su Anlaşmaları Portalında İncele ↗
                                </a>
                            </div>
                        `);
                        cluster.addLayer(marker);
                    }});
                    mapLayers['agreements'] = cluster;
                    portalMap.addLayer(cluster);
                }} catch (err) {{
                    console.error('Agreements layer error:', err);
                }} finally {{
                    if (loader) loader.style.display = 'none';
                }}
                return;
            }}

            if (layerId === 'conflicts') {{
                if (!isChecked) {{
                    if (mapLayers['conflicts']) portalMap.removeLayer(mapLayers['conflicts']);
                    updateActiveLayersBadges();
                    return;
                }}
                if (mapLayers['conflicts']) {{
                    portalMap.addLayer(mapLayers['conflicts']);
                    return;
                }}
                if (loader) {{ loaderText.innerText = '2.809 Tarihi Su Olayı & Çatışması yükleniyor...'; loader.style.display = 'flex'; }}
                try {{
                    let res = await fetch('data/water_conflicts.json');
                    if (!res.ok) res = await fetch('https://mserman90.github.io/water-agreements-portal/data/water_conflicts.json');
                    const conflicts = await res.json();
                    const cluster = L.markerClusterGroup({{ chunkedLoading: true, maxClusterRadius: 40, iconCreateFunction: (c) => createChannelClusterIcon(c, '⚡', 'cluster-conflicts') }});
                    conflicts.forEach(c => {{
                        if (!c.latitude || !c.longitude) return;
                        const symbol = c.intensity <= -4 ? '⚡' : (c.intensity > 0 ? '🤝' : '⚔️');
                        const color = c.intensity < 0 ? '#dc2626' : '#16a34a';
                        const icon = L.divIcon({{
                            className: '',
                            html: `<div style="width:18px;height:18px;border-radius:50%;background:${{color}};border:1.5px solid #fff;box-shadow:0 0 6px ${{color}};display:flex;align-items:center;justify-content:center;font-size:10px;cursor:pointer;">${{symbol}}</div>`,
                            iconSize: [18, 18],
                            iconAnchor: [9, 9]
                        }});
                        const marker = L.marker([c.latitude, c.longitude], {{ icon, title: c.title }});
                        marker.bindPopup(`
                            <div class="portal-popup-card">
                                <div class="portal-popup-header">
                                    <span class="popup-channel-badge" style="background:${{color}};">⚡ SU OLAYI (BAR: ${{c.intensity}})</span>
                                    <span class="popup-cat-badge">📅 ${{c.dateStr || c.year}}</span>
                                </div>
                                <h4 class="portal-popup-title">${{escapeMapHtml(c.title)}}</h4>
                                <div class="portal-popup-meta">
                                    <div>📍 <b>Taraflar:</b> ${{escapeMapHtml(c.countries || '')}}</div>
                                    <div>🌊 <b>Havza:</b> ${{escapeMapHtml(c.basin || '')}}</div>
                                </div>
                                <p class="portal-popup-desc">${{escapeMapHtml(c.description || '')}}</p>
                                <a href="${{c.pacificRefUrl || 'https://mserman90.github.io/water-agreements-portal/'}}" target="_blank" rel="noopener noreferrer" class="btn-map-popup-read" style="text-decoration:none;">
                                    📚 Pacific Institute / Kaynakça ↗
                                </a>
                            </div>
                        `);
                        cluster.addLayer(marker);
                    }});
                    mapLayers['conflicts'] = cluster;
                    portalMap.addLayer(cluster);
                }} catch (err) {{
                    console.error('Conflicts layer error:', err);
                }} finally {{
                    if (loader) loader.style.display = 'none';
                }}
                return;
            }}

            if (layerId === 'basins') {{
                if (!isChecked) {{
                    if (mapLayers['basins']) portalMap.removeLayer(mapLayers['basins']);
                    updateActiveLayersBadges();
                    return;
                }}
                if (mapLayers['basins']) {{
                    portalMap.addLayer(mapLayers['basins']);
                    return;
                }}
                if (loader) {{ loaderText.innerText = '310 Sınır Aşan Nehir Havzası poligonları yükleniyor...'; loader.style.display = 'flex'; }}
                try {{
                    let res = await fetch('data/Basin310_Master_20180511.geojson');
                    if (!res.ok) res = await fetch('https://mserman90.github.io/water-agreements-portal/data/Basin310_Master_20180511.geojson');
                    const geoJson = await res.json();
                    const geoLayer = L.geoJSON(geoJson, {{
                        style: () => ({{
                            fillColor: '#0284c7',
                            weight: 1.2,
                            opacity: 0.8,
                            color: '#0369a1',
                            fillOpacity: 0.12
                        }}),
                        onEachFeature: (feature, layer) => {{
                            const p = feature.properties || {{}};
                            const bName = p.Basin_Name || 'Bilinmeyen Havza';
                            const area = p.Area_km2 ? Number(p.Area_km2).toLocaleString() : 'N/A';
                            const pop = p.Pop_2020 ? Number(p.Pop_2020).toLocaleString() : 'N/A';
                            layer.bindPopup(`
                                <div class="portal-popup-card">
                                    <div class="portal-popup-header">
                                        <span class="popup-channel-badge" style="background:#0891b2;">🗺️ SINIR AŞAN HAVZA</span>
                                        <span class="popup-cat-badge">${{p.BCODE || ''}}</span>
                                    </div>
                                    <h4 class="portal-popup-title">🌊 ${{escapeMapHtml(bName)}}</h4>
                                    <div class="portal-popup-meta">
                                        <div>📐 <b>Yüzölçümü:</b> ${{area}} km²</div>
                                        <div>👥 <b>Nüfus (2020):</b> ${{pop}}</div>
                                        <div>🌍 <b>Kıta:</b> ${{escapeMapHtml(p.Continent_ || '')}}</div>
                                    </div>
                                    <a href="https://mserman90.github.io/water-agreements-portal/" target="_blank" rel="noopener noreferrer" class="btn-map-popup-read" style="text-decoration:none;">
                                        📊 Havza İklim Anomalilerini İncele ↗
                                    </a>
                                </div>
                            `);
                        }}
                    }});
                    mapLayers['basins'] = geoLayer;
                    portalMap.addLayer(geoLayer);
                }} catch (err) {{
                    console.error('Basins layer error:', err);
                }} finally {{
                    if (loader) loader.style.display = 'none';
                }}
                return;
            }}
        }}

        function zoomMapTo(target) {{
            if (!portalMap) return;
            if (target === 'turkey') {{
                portalMap.setView([38.5, 35.0], 6);
            }} else {{
                portalMap.setView([25.0, 20.0], 2.5);
            }}
        }}

        function toggleMapFullscreen() {{
            const wrapper = document.getElementById('mapCanvasWrapper');
            const btn = document.getElementById('btnMapFullscreen');
            if (!wrapper) return;
            wrapper.classList.toggle('fullscreen-mode');
            const isFull = wrapper.classList.contains('fullscreen-mode');
            if (btn) btn.innerText = isFull ? '✕ Küçült' : '⛶ Tam Ekran';
            if (portalMap) {{
                setTimeout(() => portalMap.invalidateSize(), 200);
            }}
        }}

                window.currentModalArticleId = null;

        function openArticleModal(id) {{
            const it = articlesData.find(a => a.id === id);
            if (!it) return;

            window.currentModalArticleId = id;
            const isEn = (window.currentPortalLang === 'en');
            const channelTag = isEn ? (it.channel_name_en || 'Water Agenda') : (it.channel_name || '{portal_name}');
            const catName = isEn ? (CATEGORIES_I18N[it.category] || it.category) : it.category;

            if (it.is_academic) {{
                document.getElementById('modalBadge').innerText = '🎓 ' + catName;
                document.getElementById('modalHeaderCategory').innerText = isEn
                    ? ('🎓 PEER-REVIEWED RESEARCH • ' + catName.toUpperCase())
                    : ('🎓 HAKEMLİ AKADEMİK YAYIN • ' + catName.toUpperCase());
            }} else if (it.is_turkey) {{
                document.getElementById('modalBadge').innerText = '🇹🇷 ' + catName;
                document.getElementById('modalHeaderCategory').innerText = channelTag.toUpperCase() + ' • ' + catName.toUpperCase();
            }} else {{
                document.getElementById('modalBadge').innerText = catName;
                document.getElementById('modalHeaderCategory').innerText = catName.toUpperCase() + ' • ' + channelTag;
            }}

            const titleTr = it.title_tr || it.title || '';
            const titleEn = it.title_en || it.title || titleTr;

            document.getElementById('modalTitleTr').innerText = isEn ? titleEn : titleTr;
            const titleEnEl = document.getElementById('modalTitleEn');
            if (isEn) {{
                if (titleTr && titleTr !== titleEn) {{
                    titleEnEl.innerText = 'Turkish Headline: ' + titleTr;
                    titleEnEl.style.display = 'block';
                }} else {{
                    titleEnEl.style.display = 'none';
                }}
            }} else {{
                if (titleEn && titleEn !== titleTr) {{
                    titleEnEl.innerText = 'Orijinal Başlık: ' + titleEn;
                    titleEnEl.style.display = 'block';
                }} else {{
                    titleEnEl.style.display = 'none';
                }}
            }}

            document.getElementById('modalDate').innerText = '📅 ' + (it.date || '');
            document.getElementById('modalSource').innerText = (it.source && (it.source.startsWith('📰') || it.source.startsWith('🎓') || it.source.startsWith('🇹🇷') || it.source.startsWith('📡') || it.source.startsWith('🌾') || it.source.startsWith('🐄'))) ? it.source : '📰 ' + (it.source || (isEn ? 'Press' : 'Basın'));
            document.getElementById('modalAuthor').innerText = it.author ? ('✍️ ' + it.author) : ('✍️ ' + (isEn ? 'Press Release' : 'Basın Bülteni'));
            
            const imgEl = document.getElementById('modalImg');
            if (it.image) {{
                imgEl.src = it.image;
                imgEl.style.display = 'block';
            }} else {{
                imgEl.style.display = 'none';
            }}

            const summary = isEn ? (it.summary_en || it.summary_tr || '') : (it.summary_tr || '');
            document.getElementById('modalContent').innerHTML = '<p>' + summary.replace(/
/g, '</p><p>') + '</p>';
            document.getElementById('modalDoiLink').href = it.link || '#';
            const doiBtn = document.getElementById('modalDoiLink');
            if (doiBtn) {{
                doiBtn.innerHTML = isEn ? 'Original Article & Sources &rarr;' : 'Orijinal Araştırma ve Kaynak &rarr;';
            }}

            const modal = document.getElementById('articleModal');
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}

        function closeArticleModal(e) {{
            const modal = document.getElementById('articleModal');
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }}

        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeArticleModal();
        }});

                // Bilingual (Turkish / English) Engine
        window.currentPortalLang = localStorage.getItem('portal_language') || 'tr';

        const CHANNEL_CONFIG = {{
            channel_key: '{channel_key}',
            portal_name_tr: `{portal_name_tr}`,
            portal_name_en: `{portal_name_en}`,
            portal_sub_name_tr: `{portal_sub_name_tr}`,
            portal_sub_name_en: `{portal_sub_name_en}`,
            portal_motto_tr: `{portal_motto_tr}`,
            portal_motto_en: `{portal_motto_en}`,
            portal_title_tag_tr: `{portal_title_tag_tr}`,
            portal_title_tag_en: `{portal_title_tag_en}`,
            quote_text_tr: `{quote_text}`,
            quote_text_en: `{quote_text_en}`,
            quote_author_tr: `{quote_author}`,
            quote_author_en: `{quote_author_en}`,
            quote_cat_tr: `{quote_cat}`,
            quote_cat_en: `{quote_cat_en}`,
            today_str: `{today_str}`
        }};

        const CATEGORIES_I18N = {{
            "Su Kaynakları": "Water Resources",
            "İklim & Kuraklık": "Climate & Drought",
            "Tarımsal Sulama": "Agricultural Irrigation",
            "Su Teknolojileri": "Water Technologies",
            "Su Arıtma & Kalite": "Water Treatment & Quality",
            "Su Politikaları": "Water Policy & Governance",
            "Akademik Yayınlar": "Academic Publications",
            "Akademik": "Academic",
            "Türkiye": "Turkey",

            "Tarım Teknolojileri": "AgTech & Precision Farming",
            "Tohum & Gübre": "Seed & Fertilizer",
            "Tarımsal Destekler": "Agricultural Subsidies",
            "Küresel Tarım": "Global Agriculture",
            "Bitkisel Üretim": "Crop Production",
            "Tarım & Bitkisel": "Agriculture & Crops",

            "Hayvancılık Teknolojileri": "Livestock Technologies",
            "Süt & Mandıra": "Dairy & Milk",
            "Besi & Kırmızı Et": "Livestock & Beef",
            "Yem & Besleme": "Feed & Nutrition",
            "Hayvan Sağlığı & Biyogüvenlik": "Animal Health & Biosecurity",
            "Küçükbaş Hayvancılık": "Small Ruminants (Sheep & Goat)",
            "Kanatlı Sektörü": "Poultry Sector",
            "Destek & Fiyat Politikaları": "Subsidies & Market Prices",
            "Hayvancılık & Besicilik": "Livestock & Ranching",
            "Hayvancılık & Süt": "Livestock & Dairy"
        }};

        const CATEGORY_TITLES_EN = {{
            'all': '{channel_ticker_icon} Latest Articles & Research',
            'akademik': '🎓 Peer-Reviewed Academic Research Papers',
            'sulama': '🌾 Agricultural Irrigation Research',
            'teknoloji': '🔬 Water & Agritech Innovations',
            'kaynak': '💧 Water Resources & Basin Management',
            'iklim': '🌍 Climate & Drought Research',
            'politika': '⚖️ Water & Agricultural Policy',
            'tohum': '🌱 Seeds, Fertilizers & Soil Health',
            'destek': '🏛️ Subsidies, Grants & Market Prices',
            'kuresel': '🌐 Global Markets & Commodities',
            'bitkisel': '🚜 Crop Production & Greenhouses',
            'sut': '🥛 Dairy & Milk Processing',
            'besi': '🥩 Beef & Livestock Ranching',
            'yem': '🌾 Feed & Animal Nutrition',
            'saglik': '🩺 Animal Health & Veterinary',
            'kucukbas': '🐑 Small Ruminants (Sheep & Goat)',
            'kanatli': '🐔 Poultry Industry'
        }};

        function setPortalLanguage(lang) {{
            window.currentPortalLang = lang;
            localStorage.setItem('portal_language', lang);

            const isEn = (lang === 'en');

            // 1. Language pill switcher buttons
            const btnTR = document.getElementById('btnLangTR');
            const btnEN = document.getElementById('btnLangEN');
            if (btnTR) btnTR.classList.toggle('active', !isEn);
            if (btnEN) btnEN.classList.toggle('active', isEn);

            // 2. HTML lang and document title
            document.documentElement.lang = lang;
            document.title = isEn ? CHANNEL_CONFIG.portal_title_tag_en : CHANNEL_CONFIG.portal_title_tag_tr;

            // 3. Header Masthead Elements
            const logoEl = document.getElementById('newspaperLogo');
            const subLogoEl = document.getElementById('newspaperSubLogo');
            const mottoEl = document.getElementById('newspaperMotto');
            if (logoEl) logoEl.innerText = isEn ? CHANNEL_CONFIG.portal_name_en : CHANNEL_CONFIG.portal_name_tr;
            if (subLogoEl) subLogoEl.innerText = isEn ? CHANNEL_CONFIG.portal_sub_name_en : CHANNEL_CONFIG.portal_sub_name_tr;
            if (mottoEl) mottoEl.innerHTML = isEn ? CHANNEL_CONFIG.portal_motto_en : CHANNEL_CONFIG.portal_motto_tr;

            // 4. Channel Switcher Tabs
            const tabW = document.getElementById('tabNameWater');
            const tabA = document.getElementById('tabNameAgri');
            const tabL = document.getElementById('tabNameLivestock');
            if (tabW) tabW.innerText = isEn ? 'WATER AGENDA' : 'SU GÜNDEMİ';
            if (tabA) tabA.innerText = isEn ? 'AGRICULTURE AGENDA' : 'TARIM GÜNDEMİ';
            if (tabL) tabL.innerText = isEn ? 'LIVESTOCK AGENDA' : 'HAYVANCILIK GÜNDEMİ';

            // 5. Search Box Placeholder
            const searchEl = document.getElementById('searchInput');
            if (searchEl) searchEl.placeholder = isEn ? '🔍 Search in headlines...' : '🔍 Başlıklarda ara...';

            // 6. Günün Sözü (Quote of the Day)
            const qTitle = document.getElementById('dailyQuoteTitle');
            const qText = document.getElementById('dailyQuoteText');
            const qAuth = document.getElementById('dailyQuoteAuthor');
            const qCat = document.getElementById('dailyQuoteCat');
            if (qTitle) qTitle.innerText = isEn ? 'Quote of the Day' : 'Günün Sözü';
            if (qText) qText.innerText = '"' + (isEn ? CHANNEL_CONFIG.quote_text_en : CHANNEL_CONFIG.quote_text_tr) + '"';
            if (qAuth) qAuth.innerText = isEn ? CHANNEL_CONFIG.quote_author_en : CHANNEL_CONFIG.quote_author_tr;
            if (qCat) qCat.innerText = isEn ? CHANNEL_CONFIG.quote_cat_en : CHANNEL_CONFIG.quote_cat_tr;

            // 7. Update All Article Titles, Summaries, Categories across Page
            document.querySelectorAll('[data-article-title-id]').forEach(el => {{
                const aid = parseInt(el.getAttribute('data-article-title-id'));
                const art = articlesData.find(a => a.id === aid);
                if (art) {{
                    el.innerText = isEn ? (art.title_en || art.title_tr) : art.title_tr;
                }}
            }});

            document.querySelectorAll('[data-article-summary-id]').forEach(el => {{
                const aid = parseInt(el.getAttribute('data-article-summary-id'));
                const art = articlesData.find(a => a.id === aid);
                if (art) {{
                    const fullSum = isEn ? (art.summary_en || art.summary_tr || '') : (art.summary_tr || '');
                    const maxLen = el.classList.contains('hero-summary') ? 320 : (el.classList.contains('card-excerpt') ? 180 : 120);
                    el.innerText = fullSum.slice(0, maxLen) + '...';
                }}
            }});

            document.querySelectorAll('[data-article-ticker-id]').forEach(el => {{
                const aid = parseInt(el.getAttribute('data-article-ticker-id'));
                const art = articlesData.find(a => a.id === aid);
                if (art) {{
                    el.innerText = isEn ? (art.title_en || art.title_tr) : art.title_tr;
                }}
            }});

            // 8. Buttons (Read news & source links)
            document.querySelectorAll('[data-i18n="read_news"]').forEach(el => {{
                el.innerText = isEn ? 'Read Article →' : 'Haberi Oku →';
            }});
            document.querySelectorAll('[data-i18n="source_link"]').forEach(el => {{
                el.innerText = isEn ? '🔗 Source' : '🔗 Kaynak';
            }});

            // 9. Map section labels & side panel (if present)
            const mapBadge = document.querySelector('.map-badge-tag');
            if (mapBadge) mapBadge.innerText = isEn ? '🌐 GEOGRAPHIC INFORMATION SYSTEM (GIS) & ATLAS' : '🌐 COĞRAFİ BİLGİ SİSTEMİ (GIS) & HİDROPOLİTİK ATLAS';
            const mapTitle = document.querySelector('.map-section-title');
            if (mapTitle) mapTitle.innerText = isEn ? 'Interactive Water, Agriculture & Transboundary Basins Map' : 'İnteraktif Su, Tarım & Sınır Aşan Havza Haritası';
            const sidePanelTitle = document.querySelector('.side-panel-title');
            if (sidePanelTitle) sidePanelTitle.innerText = isEn ? 'Layer Filters' : 'Katman Filtreleri';
            const sidePanelClose = document.querySelector('.btn-close-side-panel');
            if (sidePanelClose) sidePanelClose.title = isEn ? 'Hide Panel' : 'Paneli Gizle (Kapat)';
            const btnToggleLayers = document.querySelector('.btn-toggle-layers-bar');
            if (btnToggleLayers) btnToggleLayers.title = isEn ? 'Toggle Layer Filters Panel' : 'Katman Filtreleri Panelini Aç / Kapat';

            // 10. Update current active category title header
            if (typeof filterCategory === 'function') {{
                const secTitle = document.getElementById('sectionTitle');
                if (secTitle) {{
                    if (isEn && CATEGORY_TITLES_EN[currentSlug]) {{
                        secTitle.innerText = CATEGORY_TITLES_EN[currentSlug];
                    }} else if (CATEGORY_TITLES[currentSlug]) {{
                        secTitle.innerText = CATEGORY_TITLES[currentSlug];
                    }}
                }}
            }}

            // 11. If an article modal is currently open, refresh it in the active language
            if (window.currentModalArticleId !== null && window.currentModalArticleId !== undefined) {{
                openArticleModal(window.currentModalArticleId);
            }}
        }}

        // Initialize language immediately
        document.addEventListener('DOMContentLoaded', function() {{
            setPortalLanguage(window.currentPortalLang);
        }});

        let currentSlug = 'all';

        const CATEGORY_TITLES = {{
            {category_titles_js}
        }};

        function filterCategory(slug) {{
            currentSlug = slug;

            // Clear search input if present
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.value = '';

            // Update active states on category buttons
            document.querySelectorAll('.cat-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.slug === slug);
            }});

            const heroEl = document.getElementById('heroSection');
            const subEl = document.getElementById('subHeadlinesSection');
            const titleEl = document.getElementById('sectionTitle');
            const countEl = document.getElementById('sectionCount');
            const noResultsEl = document.getElementById('noResultsState');
            const allCards = document.querySelectorAll('.news-grid-card');

            let visibleCount = 0;

            if (slug === 'all') {{
                // Show Hero and Subheadlines
                if (heroEl) heroEl.style.display = '';
                if (subEl) subEl.style.display = '';

                // Show only non-top cards in grid
                allCards.forEach(card => {{
                    const isTop = card.getAttribute('data-is-top') === 'true';
                    if (!isTop) {{
                        card.style.display = '';
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                if (titleEl) titleEl.innerHTML = CATEGORY_TITLES['all'];
                if (countEl) countEl.innerHTML = `Toplam <strong>${{allCards.length}}</strong> makale`;
                if (noResultsEl) noResultsEl.style.display = 'none';

            }} else if (slug === 'akademik') {{
                if (heroEl) heroEl.style.display = 'none';
                if (subEl) subEl.style.display = 'none';

                allCards.forEach(card => {{
                    const isAcademic = card.getAttribute('data-is-academic') === 'true' || card.dataset.slug === 'akademik';
                    if (isAcademic) {{
                        card.style.display = '';
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                if (titleEl) titleEl.innerHTML = CATEGORY_TITLES['akademik'];
                if (countEl) countEl.innerHTML = `Kategoride <strong>${{visibleCount}}</strong> hakemli makale`;

                if (visibleCount === 0) {{
                    if (noResultsEl) {{
                        document.getElementById('emptyTitle').innerText = 'Akademik su yönetimi yayınları taranıyor...';
                        document.getElementById('emptyDesc').innerText = 'ScienceDirect, MDPI, Springer Nature, Wiley ve DergiPark akademik yayınları taranmaktadır.';
                        noResultsEl.style.display = 'block';
                    }}
                }} else {{
                    if (noResultsEl) noResultsEl.style.display = 'none';
                }}

                const target = document.getElementById('mainNewsSection');
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}

            }} else {{
                // Specific category chosen: hide hero and subheadlines
                if (heroEl) heroEl.style.display = 'none';
                if (subEl) subEl.style.display = 'none';

                // Display all matching cards (including cards 0..3)
                allCards.forEach(card => {{
                    if (card.dataset.slug === slug) {{
                        card.style.display = '';
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});

                const catTitle = CATEGORY_TITLES[slug] || 'Kategori Haberleri';
                if (titleEl) titleEl.innerHTML = catTitle;
                if (countEl) countEl.innerHTML = `Kategoride <strong>${{visibleCount}}</strong> makale`;

                if (visibleCount === 0) {{
                    if (noResultsEl) {{
                        document.getElementById('emptyTitle').innerText = 'Bu kategoride henüz haber bulunmuyor';
                        document.getElementById('emptyDesc').innerText = 'Seçtiğiniz kategoride yeni bültenler otomatik taranmaya devam etmektedir.';
                        noResultsEl.style.display = 'block';
                    }}
                }} else {{
                    if (noResultsEl) noResultsEl.style.display = 'none';
                }}

                // Smoothly scroll to the articles section
                const target = document.getElementById('mainNewsSection');
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }}
        }}

        function filterSearch() {{
            const input = document.getElementById('searchInput');
            const query = input.value.trim().toLowerCase();

            if (!query) {{
                filterCategory(currentSlug);
                return;
            }}

            // Deactivate category buttons while search query is active
            document.querySelectorAll('.cat-btn').forEach(btn => btn.classList.remove('active'));

            const heroEl = document.getElementById('heroSection');
            const subEl = document.getElementById('subHeadlinesSection');
            const titleEl = document.getElementById('sectionTitle');
            const countEl = document.getElementById('sectionCount');
            const noResultsEl = document.getElementById('noResultsState');
            const allCards = document.querySelectorAll('.news-grid-card');

            if (heroEl) heroEl.style.display = 'none';
            if (subEl) subEl.style.display = 'none';

            let matchCount = 0;
            allCards.forEach(card => {{
                const searchCorpus = (card.getAttribute('data-search') || '').toLowerCase();
                if (searchCorpus.indexOf(query) > -1) {{
                    card.style.display = '';
                    matchCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            if (titleEl) titleEl.innerHTML = `🔍 Arama Sonuçları: "${{query}}"`;
            if (countEl) countEl.innerHTML = `Eşleşen <strong>${{matchCount}}</strong> makale`;

            if (matchCount === 0) {{
                if (noResultsEl) {{
                    document.getElementById('emptyTitle').innerText = `"${{query}}" ile eşleşen sonuç bulunamadı`;
                    document.getElementById('emptyDesc').innerText = 'Farklı bir arama terimi deneyebilir veya kategorileri seçebilirsiniz.';
                    noResultsEl.style.display = 'block';
                }}
            }} else {{
                if (noResultsEl) noResultsEl.style.display = 'none';
            }}
        }}

        function updateThemeElements(theme) {{
            const isDark = (theme === 'dark');
            const icon = isDark ? '☀️' : '🌙';
            const tooltip = isDark ? 'Gündüz Moduna Geç' : 'Gece Moduna Geç';

            const btn = document.getElementById('themeToggleBtn') || document.getElementById('themeToggleBtnNav');
            if (btn) {{
                btn.innerHTML = `<span class="theme-icon">${{icon}}</span>`;
                btn.title = tooltip;
            }}
            if (window.portalTileLayer && typeof getTileLayerConfig === 'function') {{
                const cfg = getTileLayerConfig(isDark);
                window.portalTileLayer.setUrl(cfg.url);
            }}
        }}

        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const next = (current === 'dark') ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('su_portal_theme', next);
            updateThemeElements(next);
        }}

        // Initialize theme button state as soon as DOM is ready
        (function initThemeUI() {{
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', () => {{
                    updateThemeElements(current);
                    initPortalMap();
                }});
            }} else {{
                updateThemeElements(current);
                initPortalMap();
            }}
        }})();

        // Client-side auto-update: Polls feed.json every 90 seconds to check for new articles
        (function initLiveFeedSync() {{
            let knownTopTitle = (articlesData && articlesData.length > 0) ? articlesData[0].title_en : '';

            function escapeHtml(str) {{
                if (!str) return '';
                const p = document.createElement('p');
                p.textContent = str;
                return p.innerHTML;
            }}

            async function checkLiveFeed() {{
                try {{
                    const res = await fetch('{live_feed_file}?_=' + Date.now(), {{ cache: 'no-store' }});
                    if (!res.ok) return;
                    const feed = await res.json();
                    const items = feed.items || [];
                    if (!items.length) return;

                    const latest = items[0];
                    const latestTitle = latest.title || latest.id || '';
                    if (latestTitle && knownTopTitle && latestTitle !== knownTopTitle) {{
                        console.log('[Canlı Akış] Yeni haberler tespit edildi, ticker güncelleniyor...');
                        knownTopTitle = latestTitle;

                        // Update continuous ticker track seamlessly
                        const track = document.getElementById('tickerTrack');
                        if (track) {{
                            let trackHtml = '';
                            items.slice(0, 15).forEach(item => {{
                                const title = item.title || '';
                                trackHtml += `<span class="ticker-item" onclick="window.location.reload()"><span class="ticker-icon">⚡</span> <span class="ticker-text">${{escapeHtml(title)}}</span> <span class="ticker-sep">&bull;</span></span>`;
                            }});
                            track.innerHTML = trackHtml + trackHtml;
                        }}

                    }}
                }} catch (e) {{
                    // Ignore transient network errors
                }}
            }}

            // Start checking after 45 seconds, then every 90 seconds
            setTimeout(() => {{
                checkLiveFeed();
                setInterval(checkLiveFeed, 90000);
            }}, 45000);
            let isTickerPaused = false;
            window.toggleTickerPause = function() {{
                const track = document.getElementById('tickerTrack');
                const btn = document.getElementById('tickerPauseBtn');
                if (!track) return;
                isTickerPaused = !isTickerPaused;
                if (isTickerPaused) {{
                    track.style.animationPlayState = 'paused';
                    if (btn) btn.innerHTML = '▶️';
                }} else {{
                    track.style.animationPlayState = 'running';
                    if (btn) btn.innerHTML = '⏸️';
                }}
            }};
        }})();
    </script>

    <!-- Bottom Screen Fixed Ticker Bar -->
    <div class="bottom-ticker-bar" id="bottomTickerBar" style="--bottom-ticker-border: {bottom_ticker_border}; --bottom-ticker-badge-bg: {bottom_ticker_badge_bg}; --bottom-ticker-accent: {bottom_ticker_accent};" role="region" aria-label="{channel_ticker_label} Canlı Akış">
        <div class="bottom-ticker-badge">
            <span class="ticker-live-dot" aria-hidden="true"></span>
            <span class="badge-icon">{channel_ticker_icon}</span>
            <span class="badge-text">{channel_ticker_label}</span>
        </div>
        <div class="bottom-ticker-marquee" title="Akışı durdurmak için imleci üzerine getirebilir veya duraklat düğmesini kullanabilirsiniz">
            <div class="bottom-ticker-track" id="tickerTrack">
                {ticker_track_content}
            </div>
        </div>
        <div class="bottom-ticker-controls">
            <button type="button" id="tickerPauseBtn" class="btn-ticker-ctrl" onclick="toggleTickerPause()" title="Akışı Duraklat / Devam Ettir" aria-label="Akışı Duraklat veya Devam Ettir">⏸️</button>
        </div>
    </div>
</body>
</html>"""
