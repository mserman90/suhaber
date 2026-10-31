"""
app/geocoder.py
Metin tabanlı haber içeriklerinden (başlık, özet, kaynak) coğrafi konumları (enlem, boylam ve yer ismi)
çıkaran ve harita görselleştirmesi için koordinat üreten modül.
"""

import re
import math
from typing import Dict, Any, Tuple, Optional

# 1. Türkiye İlleri, İlçeleri, Barajları, Ovaları ve Akarsuları
TURKEY_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # 81 İl
    "adana": (37.0017, 35.3289, "Adana"),
    "adıyaman": (37.7648, 38.2786, "Adıyaman"),
    "afyon": (38.7569, 30.5387, "Afyonkarahisar"),
    "afyonkarahisar": (38.7569, 30.5387, "Afyonkarahisar"),
    "ağrı": (39.7217, 43.0567, "Ağrı"),
    "amasya": (40.6501, 35.8353, "Amasya"),
    "ankara": (39.9334, 32.8597, "Ankara"),
    "antalya": (36.8841, 30.7056, "Antalya"),
    "artvin": (41.1828, 41.8183, "Artvin"),
    "aydın": (37.8444, 27.8458, "Aydın"),
    "balıkesir": (39.6484, 27.8826, "Balıkesir"),
    "bilecik": (40.1451, 29.9799, "Bilecik"),
    "bingöl": (38.8854, 40.4983, "Bingöl"),
    "bitlis": (38.4006, 42.1095, "Bitlis"),
    "bolu": (40.7358, 31.6061, "Bolu"),
    "burdur": (37.7203, 30.2908, "Burdur"),
    "bursa": (40.1885, 29.0610, "Bursa"),
    "çanakkale": (40.1553, 26.4142, "Çanakkale"),
    "çankırı": (40.6013, 33.6134, "Çankırı"),
    "çorum": (40.5506, 34.9556, "Çorum"),
    "denizli": (37.7765, 29.0864, "Denizli"),
    "diyarbakır": (37.9144, 40.2306, "Diyarbakır"),
    "edirne": (41.6772, 26.5557, "Edirne"),
    "elazığ": (38.6810, 39.2264, "Elazığ"),
    "erzincan": (39.7500, 39.5000, "Erzincan"),
    "erzurum": (39.9043, 41.2679, "Erzurum"),
    "eskişehir": (39.7767, 30.5206, "Eskişehir"),
    "gaziantep": (37.0662, 37.3833, "Gaziantep"),
    "giresun": (40.9128, 38.3895, "Giresun"),
    "gümüşhane": (40.4600, 39.4700, "Gümüşhane"),
    "hakkari": (37.5833, 43.7333, "Hakkari"),
    "hatay": (36.2023, 36.1606, "Hatay / Antakya"),
    "antakya": (36.2023, 36.1606, "Hatay / Antakya"),
    "isparta": (37.7648, 30.5566, "Isparta"),
    "mersin": (36.8121, 34.6415, "Mersin"),
    "içel": (36.8121, 34.6415, "Mersin"),
    "istanbul": (41.0082, 28.9784, "İstanbul"),
    "izmir": (38.4237, 27.1428, "İzmir"),
    "kars": (40.6013, 43.0975, "Kars"),
    "kastamonu": (41.3887, 33.7827, "Kastamonu"),
    "kayseri": (38.7312, 35.4787, "Kayseri"),
    "kırklareli": (41.7333, 27.2167, "Kırklareli"),
    "kırşehir": (39.1425, 34.1709, "Kırşehir"),
    "kocaeli": (40.7654, 29.9408, "Kocaeli / İzmit"),
    "izmit": (40.7654, 29.9408, "Kocaeli / İzmit"),
    "konya": (37.8746, 32.4932, "Konya"),
    "kütahya": (39.4167, 29.9833, "Kütahya"),
    "malatya": (38.3552, 38.3095, "Malatya"),
    "manisa": (38.6191, 27.4289, "Manisa"),
    "kahramanmaraş": (37.5858, 36.9371, "Kahramanmaraş"),
    "maraş": (37.5858, 36.9371, "Kahramanmaraş"),
    "mardin": (37.3212, 40.7245, "Mardin"),
    "muğla": (37.2153, 28.3636, "Muğla"),
    "muş": (38.7432, 41.5064, "Muş"),
    "nevşehir": (38.6244, 34.7144, "Nevşehir"),
    "niğde": (37.9667, 34.6833, "Niğde"),
    "ordu": (40.9839, 37.8764, "Ordu"),
    "rize": (41.0201, 40.5234, "Rize"),
    "sakarya": (40.7569, 30.3783, "Sakarya / Adapazarı"),
    "adapazarı": (40.7569, 30.3783, "Sakarya / Adapazarı"),
    "samsun": (41.2867, 36.33, "Samsun"),
    "siirt": (37.9333, 41.95, "Siirt"),
    "sinop": (42.0231, 35.1531, "Sinop"),
    "sivas": (39.7477, 37.0179, "Sivas"),
    "tekirdağ": (40.9833, 27.5167, "Tekirdağ"),
    "tokat": (40.3167, 36.55, "Tokat"),
    "trabzon": (41.0027, 39.7168, "Trabzon"),
    "tunceli": (39.1079, 39.5401, "Tunceli"),
    "şanlıurfa": (37.1591, 38.7969, "Şanlıurfa"),
    "urfa": (37.1591, 38.7969, "Şanlıurfa"),
    "uşak": (38.6823, 29.4082, "Uşak"),
    "van": (38.4891, 43.4089, "Van"),
    "yozgat": (39.8181, 34.8147, "Yozgat"),
    "zonguldak": (41.4564, 31.7987, "Zonguldak"),
    "aksaray": (38.3687, 34.0370, "Aksaray"),
    "bayburt": (40.2552, 40.2249, "Bayburt"),
    "karaman": (37.1759, 33.2287, "Karaman"),
    "kırıkkale": (39.8468, 33.5153, "Kırıkkale"),
    "batman": (37.8812, 41.1293, "Batman"),
    "şırnak": (37.5164, 42.4594, "Şırnak"),
    "bartın": (41.6344, 32.3375, "Bartın"),
    "ardahan": (41.1105, 42.7022, "Ardahan"),
    "iğdır": (39.9196, 44.0454, "Iğdır"),
    "yalova": (40.6500, 29.2667, "Yalova"),
    "karabük": (41.2061, 32.6204, "Karabük"),
    "kilis": (36.7184, 37.1212, "Kilis"),
    "osmaniye": (37.0742, 36.2472, "Osmaniye"),
    "düzce": (40.8438, 31.1565, "Düzce"),

    # Önemli Nehirler, Göller ve Havzalar
    "fırat": (37.5500, 38.5000, "Fırat Nehri Havzası"),
    "dicle": (37.8800, 40.5000, "Dicle Nehri Havzası"),
    "kızılırmak": (39.8500, 35.5000, "Kızılırmak Havzası"),
    "yeşilırmak": (40.8000, 36.5000, "Yeşilırmak Havzası"),
    "meriç": (41.4000, 26.5000, "Meriç Nehri Havzası"),
    "gediz": (38.6000, 27.5000, "Gediz Havzası"),
    "büyük menderes": (37.9000, 28.3000, "Büyük Menderes Havzası"),
    "küçük menderes": (38.1000, 27.8000, "Küçük Menderes Havzası"),
    "seyhan": (36.9500, 35.3000, "Seyhan Havzası"),
    "ceyhan": (37.0000, 35.8000, "Ceyhan Havzası"),
    "çoruh": (41.1000, 41.6000, "Çoruh Havzası"),
    "aras": (40.1000, 43.5000, "Aras Nehri"),
    "van gölü": (38.6000, 42.9000, "Van Gölü"),
    "tuz gölü": (38.8000, 33.3000, "Tuz Gölü"),
    "beyşehir": (37.7000, 31.5000, "Beyşehir Gölü"),
    "eğirdir": (38.0000, 30.8000, "Eğirdir Gölü"),
    "sapanca": (40.7000, 30.2000, "Sapanca Gölü"),
    "manyas": (40.2000, 27.9500, "Manyas Kuşcenneti"),
    "iznik gölü": (40.4300, 29.5000, "İznik Gölü"),

    # Önemli Barajlar ve Tarımsal Alanlar
    "atatürk baraj": (37.4722, 38.3183, "Atatürk Barajı"),
    "keban baraj": (38.8039, 38.7564, "Keban Barajı"),
    "ılısu baraj": (37.5303, 41.8286, "Ilısu / Veysel Eroğlu Barajı"),
    "deriner baraj": (41.1969, 41.8681, "Deriner Barajı"),
    "yusufeli baraj": (40.8258, 41.5369, "Yusufeli Barajı"),
    "karakaya baraj": (38.2250, 38.6367, "Karakaya Barajı"),
    "altınkaya baraj": (41.3500, 35.7000, "Altınkaya Barajı"),
    "hirfanlı": (39.2700, 33.5200, "Hirfanlı Barajı"),
    "gap": (37.3000, 39.0000, "Güneydoğu Anadolu Projesi (GAP)"),
    "çukurova": (36.9500, 35.4000, "Çukurova Tarım Havzası"),
    "trakya": (41.3000, 27.5000, "Trakya Tarım Bölgesi"),
    "harran": (36.8700, 39.0200, "Harran Ovası"),
    "bafra": (41.5600, 35.9000, "Bafra Ovası"),
    "çarşamba": (41.2000, 36.7200, "Çarşamba Ovası"),
    "söke": (37.7500, 27.4000, "Söke Ovası"),
    "menemen": (38.6000, 27.0600, "Menemen Ovası"),
    "patnos": (39.2333, 42.8667, "Patnos Ovası"),
    "polatlı": (39.5800, 32.1400, "Polatlı Tarım Bölgesi"),
    "ceylanpınar": (36.8333, 39.9167, "Ceylanpınar TİGEM İşletmesi"),
    "amasya ovası": (40.6500, 35.8000, "Amasya Ovası"),
    "gediz ovası": (38.6500, 27.6000, "Gediz Ovası"),
    "konya ovası": (37.8500, 32.5000, "Konya Kapalı Havzası"),
}

# 2. Küresel Sınır-Aşan Nehir Havzaları ve Ülkeler
GLOBAL_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # Önemli Nehir Havzaları (TFDD & OSU standartları)
    "nil": (15.5000, 32.5000, "Nil Nehri Havzası (Mısır-Sudan-Etiyopya)"),
    "nile": (15.5000, 32.5000, "Nil Nehri Havzası"),
    "amazon": (-3.1000, -60.0000, "Amazon Havzası"),
    "tuna": (45.2000, 19.8000, "Tuna (Danube) Nehri Havzası"),
    "danube": (45.2000, 19.8000, "Tuna (Danube) Nehri Havzası"),
    "ren": (50.0000, 8.2000, "Ren (Rhine) Havzası"),
    "rhine": (50.0000, 8.2000, "Ren (Rhine) Havzası"),
    "indus": (30.0000, 70.0000, "İndus Nehri Havzası (Pakistan-Hindistan)"),
    "ganj": (25.3000, 83.0000, "Ganj / Brahmaputra Havzası"),
    "ganges": (25.3000, 83.0000, "Ganj / Brahmaputra Havzası"),
    "brahmaputra": (26.0000, 91.0000, "Brahmaputra Havzası"),
    "mekong": (15.0000, 105.0000, "Mekong Nehri Havzası"),
    "colorado": (36.0000, -112.0000, "Colorado Nehri Havzası"),
    "mississippi": (38.0000, -90.0000, "Mississippi Havzası"),
    "rio grande": (29.0000, -103.0000, "Rio Grande / Bravo Havzası"),
    "yangtze": (31.0000, 115.0000, "Yangtze (Çang Ciang) Havzası"),
    "sarı nehir": (36.0000, 105.0000, "Sarı Nehir (Yellow River)"),
    "yellow river": (36.0000, 105.0000, "Sarı Nehir (Yellow River)"),
    "murray": (-34.5000, 142.0000, "Murray-Darling Havzası (Avustralya)"),
    "kongo": (-2.0000, 22.0000, "Kongo Havzası"),
    "congo": (-2.0000, 22.0000, "Kongo Havzası"),
    "nijer": (13.0000, 2.0000, "Nijer Nehri Havzası"),
    "niger": (13.0000, 2.0000, "Nijer Nehri Havzası"),
    "zambezi": (-15.0000, 28.0000, "Zambezi Havzası"),
    "aral": (44.5000, 59.0000, "Aral Gölü Havzası"),
    "hazar": (42.0000, 51.0000, "Hazar Denizi Havzası"),
    "caspian": (42.0000, 51.0000, "Hazar Denizi Havzası"),
    "tigris": (34.0000, 44.0000, "Dicle-Fırat Uluslararası Havzası"),
    "euphrates": (34.0000, 44.0000, "Fırat-Dicle Uluslararası Havzası"),

    # Önemli Ülkeler
    "abd": (39.8283, -98.5795, "Amerika Birleşik Devletleri"),
    "usa": (39.8283, -98.5795, "Amerika Birleşik Devletleri"),
    "çin": (35.8617, 104.1954, "Çin Halk Cumhuriyeti"),
    "china": (35.8617, 104.1954, "Çin Halk Cumhuriyeti"),
    "hindistan": (20.5937, 78.9629, "Hindistan"),
    "india": (20.5937, 78.9629, "Hindistan"),
    "brezilya": (-14.2350, -51.9253, "Brezilya"),
    "brazil": (-14.2350, -51.9253, "Brezilya"),
    "mısır": (26.8206, 30.8025, "Mısır"),
    "egypt": (26.8206, 30.8025, "Mısır"),
    "ırak": (33.2232, 43.6793, "Irak"),
    "iraq": (33.2232, 43.6793, "Irak"),
    "suriye": (34.8021, 38.9968, "Suriye"),
    "syria": (34.8021, 38.9968, "Suriye"),
    "iran": (32.4279, 53.6880, "İran"),
    "ispanya": (40.4637, -3.7492, "İspanya"),
    "spain": (40.4637, -3.7492, "İspanya"),
    "italya": (41.8719, 12.5674, "İtalya"),
    "italy": (41.8719, 12.5674, "İtalya"),
    "fransa": (46.2276, 2.2137, "Fransa"),
    "france": (46.2276, 2.2137, "Fransa"),
    "almanya": (51.1657, 10.4515, "Almanya"),
    "germany": (51.1657, 10.4515, "Almanya"),
    "hollanda": (52.1326, 5.2913, "Hollanda"),
    "netherlands": (52.1326, 5.2913, "Hollanda"),
    "avustralya": (-25.2744, 133.7751, "Avustralya"),
    "australia": (-25.2744, 133.7751, "Avustralya"),
    "rusya": (61.5240, 105.3188, "Rusya"),
    "russia": (61.5240, 105.3188, "Rusya"),
    "kanada": (56.1304, -106.3468, "Kanada"),
    "canada": (56.1304, -106.3468, "Kanada"),
    "ingiltere": (55.3781, -3.4360, "Birleşik Krallık"),
    "uk": (55.3781, -3.4360, "Birleşik Krallık"),
    "japonya": (36.2048, 138.2529, "Japonya"),
    "japan": (36.2048, 138.2529, "Japonya"),
    "etiyopya": (9.1450, 40.4897, "Etiyopya"),
    "ethiopia": (9.1450, 40.4897, "Etiyopya"),
    "sudan": (12.8628, 30.2176, "Sudan"),
    "güney afrika": (-30.5595, 22.9375, "Güney Afrika"),
    "fas": (31.7917, -7.0926, "Fas"),
    "yunanistan": (39.0742, 21.8243, "Yunanistan"),
    "azerbaycan": (40.1431, 47.5769, "Azerbaycan"),
    "özbekistan": (41.3775, 64.5853, "Özbekistan"),
    "kazakistan": (48.0196, 66.9237, "Kazakistan"),
    "pakistan": (30.3753, 69.3451, "Pakistan"),
}


def _normalize_turkish_text(text: str) -> str:
    """Türkçe karakterleri güvenli şekilde küçük harfe çevirir."""
    if not text:
        return ""
    mapping = {
        "İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç"
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text.lower()


def geocode_article(article: Dict[str, Any], index_seed: int = 0) -> Tuple[float, float, str]:
    """
    Haber nesnesinden en uygun coğrafi konumu belirler.
    Dönen değer: (enlem, boylam, yer_ismi)
    """
    title_tr = article.get("title_tr") or article.get("title") or ""
    title_en = article.get("title") or ""
    summary_tr = article.get("summary_tr") or ""
    source = article.get("source_feed") or article.get("source") or ""
    cat = article.get("category_tr") or article.get("category") or ""
    guid = article.get("guid") or ""

    full_text = f"{title_tr} {title_en} {summary_tr} {source} {cat}".strip()
    norm = _normalize_turkish_text(full_text)

    # 1. Öncelik: Türkiye Barajları, Ovaları, Gölleri ve İlleri
    for keyword, (lat, lng, loc_name) in TURKEY_LOCATIONS.items():
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, norm):
            # Küçük deterministik jitter (aynı şehirde üst üste binmesin)
            jitter_lat = ((index_seed * 17) % 19 - 9) * 0.007
            jitter_lng = ((index_seed * 23) % 19 - 9) * 0.007
            return (round(lat + jitter_lat, 4), round(lng + jitter_lng, 4), loc_name)

    # 2. Öncelik: Küresel Sınır Aşan Havzalar ve Ülkeler
    for keyword, (lat, lng, loc_name) in GLOBAL_LOCATIONS.items():
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, norm):
            jitter_lat = ((index_seed * 13) % 21 - 10) * 0.04
            jitter_lng = ((index_seed * 19) % 21 - 10) * 0.04
            return (round(lat + jitter_lat, 4), round(lng + jitter_lng, 4), loc_name)

    # 3. Öncelik: Türkiye Genel Haberi (is_turkey=True veya tr_ kaynaklı)
    is_tr = bool(
        article.get("is_turkey")
        or guid.startswith("tr_")
        or guid.startswith("sygm:")
        or "🇹🇷" in source
        or cat == "Türkiye"
    )
    if is_tr:
        # Türkiye geneline yayılmış tarım ve su merkezleri çevresinde deterministik dağılım
        centers = [
            (39.93, 32.85, "Türkiye / İç Anadolu"),
            (37.87, 32.49, "Konya Ovası / Orta Anadolu"),
            (38.42, 27.14, "Ege Tarım Havzası"),
            (41.01, 28.98, "Marmara Bölgesi"),
            (37.16, 38.80, "Güneydoğu Anadolu (GAP)"),
            (37.00, 35.32, "Çukurova Bölgesi"),
            (41.29, 36.33, "Karadeniz Havzası"),
            (39.90, 41.27, "Doğu Anadolu"),
        ]
        chosen = centers[index_seed % len(centers)]
        lat_base, lng_base, base_name = chosen
        jitter_lat = ((index_seed * 31) % 15 - 7) * 0.025
        jitter_lng = ((index_seed * 43) % 15 - 7) * 0.025
        return (round(lat_base + jitter_lat, 4), round(lng_base + jitter_lng, 4), base_name)

    # 4. Öncelik: Küresel Akademik Araştırma veya Uluslararası Haber
    is_academic = bool(
        article.get("is_academic")
        or guid.startswith("academic:")
        or guid.startswith("academic_agri:")
        or guid.startswith("academic_livestock:")
        or "🎓" in source
    )
    if is_academic:
        # Önde gelen uluslararası su/tarım araştırma merkezleri & akdeniz kuşağı
        centers_global = [
            (41.90, 12.49, "FAO & Uluslararası Araştırma Merkezi (Roma)"),
            (46.20, 6.14, "BM & WMO Küresel Su Güvenliği (Cenevre)"),
            (52.13, 5.29, "Wageningen & UNESCO-IHE Su Enstitüsü"),
            (38.90, -77.03, "Dünya Bankası Su & Çevre Grubu (Washington)"),
            (-1.28, 36.82, "UNEP & IWMI Afrika Su Araştırmaları"),
            (31.23, 121.47, "Asya-Pasifik Hidro-İklim Araştırmaları"),
            (38.00, 23.72, "Akdeniz Su & Kuraklık İnisiyatifi"),
            (40.41, -3.70, "İber Havzası & Kuraklık Yönetim Merkezi"),
        ]
        chosen_g = centers_global[index_seed % len(centers_global)]
        lat_g, lng_g, base_g = chosen_g
        jitter_lat = ((index_seed * 27) % 17 - 8) * 0.03
        jitter_lng = ((index_seed * 37) % 17 - 8) * 0.03
        return (round(lat_g + jitter_lat, 4), round(lng_g + jitter_lng, 4), base_g)

    # Genel Dünya Odak Noktası
    jitter_lat = ((index_seed * 11) % 31 - 15) * 0.2
    jitter_lng = ((index_seed * 17) % 31 - 15) * 0.2
    return (round(39.0 + jitter_lat, 4), round(35.0 + jitter_lng, 4), "Türkiye & Dünya Gündemi")
