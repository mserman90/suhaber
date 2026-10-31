"""
app/geocoder.py
Gelişmiş Çok Yöntemli Coğrafi Değerlendirme & Konum Doğrulama Motoru (Multi-Method Geographic Evaluator).

Metin tabanlı haber içeriklerinden (başlık, özet, kaynak) konum tespit ederken doğruluğu garanti altına almak için
7 aşamalı değerlendirme ve çapraz doğrulama pipelini uygular:
  1. Google Alert / Kaynak Arama Sorgusu Temizleme (Feed Wrapper Cleaning)
  2. Pozisyonel Ağırlıklandırma (Title: 45, Lead Sentence: 30, Summary: 20)
  3. Coğrafi & Hidrolojik Niteleyici Doğrulaması (Collocation Verification: +25)
  4. Anlamsal Eşadlılık & Sahte Pozitif Filtresi (Semantic Homonym Disambiguation: mısır/corn, ordu/military, van/vehicle, gap/yield gap, tire/wheel, kaş, bor, aras, ren)
  5. Hiyerarşik İdari Çapraz Doğrulama (İlçe + İl Birlikte Geçme Bonusu: +35)
  6. Çoklu Bölge ve Çatışma Çözümleme (Multi-Region / Ambiguity Resolution)
  7. Güven Eşiği Filtresi (Confidence Threshold: Skor >= 70 / 100)
"""

import re
import math
import hashlib
from typing import Dict, Any, Tuple, Optional, List, Set

# 1. İlçe -> İl Hiyerarşik Eşleme Tablosu (Cross-Validation Dictionary)
DISTRICT_TO_PROVINCE: Dict[str, str] = {
    # Ege Bölgesi
    "ödemiş": "izmir", "bergama": "izmir", "tire": "izmir", "menemen": "izmir", "çeşme": "izmir",
    "urla": "izmir", "seferihisar": "izmir", "torbalı": "izmir", "kemalpaşa": "izmir",
    "akhisar": "manisa", "salihli": "manisa", "alaşehir": "manisa", "turgutlu": "manisa", "kırkağaç": "manisa", "soma": "manisa",
    "söke": "aydın", "kuşadası": "aydın", "didim": "aydın", "nazilli": "aydın", "çine": "aydın", "germencik": "aydın",
    "çivril": "denizli", "acıpavam": "denizli", "tavas": "denizli", "sarayköy": "denizli",
    "bodrum": "muğla", "fethiye": "muğla", "milas": "muğla", "marmaris": "muğla", "yatağan": "muğla", "ortaca": "muğla",
    "sandıklı": "afyonkarahisar", "dinar": "afyonkarahisar", "bolvadin": "afyonkarahisar", "emirdağ": "afyonkarahisar",
    "simav": "kütahya", "tavşanlı": "kütahya", "gediz": "kütahya",
    "banaz": "uşak", "eşme": "uşak",

    # Akdeniz Bölgesi
    "silifke": "mersin", "tarsus": "mersin", "anamur": "mersin", "erdemli": "mersin", "mut": "mersin",
    "ceyhan": "adana", "kozan": "adana", "karataş": "adana", "yüreğir": "adana", "imamoğlu": "adana",
    "alanya": "antalya", "manavgat": "antalya", "serik": "antalya", "kumluca": "antalya", "finike": "antalya",
    "kaş": "antalya", "elmalı": "antalya", "korkuteli": "antalya", "demre": "antalya", "gazipaşa": "antalya",
    "dörtyol": "hatay", "iskenderun": "hatay", "kırıkhan": "hatay", "reyhanlı": "hatay", "samandağ": "hatay", "erzin": "hatay",
    "kadirli": "osmaniye", "düziçi": "osmaniye",
    "bucak": "burdur", "gölhisar": "burdur",
    "eğirdir": "isparta", "yalvaç": "isparta", "şarkikaraağaç": "isparta", "gelendost": "isparta",
    "elbistan": "kahramanmaraş", "afşin": "kahramanmaraş", "pazarcık": "kahramanmaraş", "göksun": "kahramanmaraş",

    # Marmara Bölgesi
    "bandırma": "balıkesir", "edremit": "balıkesir", "gönen": "balıkesir", "manyas": "balıkesir", "susurluk": "balıkesir", "ayvalık": "balıkesir",
    "biga": "çanakkale", "çan": "çanakkale", "ezine": "çanakkale", "bayramiç": "çanakkale", "gelibolu": "çanakkale",
    "karacabey": "bursa", "inegöl": "bursa", "mustafakemalpaşa": "bursa", "yenişehir": "bursa", "iznik": "bursa", "mudanya": "bursa",
    "lüleburgaz": "kırklareli", "babaeski": "kırklareli",
    "çorlu": "tekirdağ", "çerkezköy": "tekirdağ", "malkara": "tekirdağ", "hayrabolu": "tekirdağ",
    "uzunköprü": "edirne", "keşan": "edirne", "ipsala": "edirne", "havsa": "edirne",
    "silivri": "istanbul", "çatalca": "istanbul", "şile": "istanbul",
    "gebze": "kocaeli", "gölcük": "kocaeli", "kandıra": "kocaeli", "kartepe": "kocaeli",
    "hendek": "sakarya", "akyazı": "sakarya", "geyve": "sakarya", "karasu": "sakarya",

    # İç Anadolu Bölgesi
    "çumra": "konya", "karapınar": "konya", "akşehir": "konya", "cihanbeyli": "konya", "kulu": "konya",
    "ereğli": "konya", "seydişehir": "konya", "beyşehir": "konya", "kadınhanı": "konya", "sarayönü": "konya", "ilgın": "konya",
    "polatlı": "ankara", "beypazarı": "ankara", "haymana": "ankara", "şereflikoçhisar": "ankara", "bala": "ankara", "nallıhan": "ankara", "çubuk": "ankara",
    "develi": "kayseri", "yeşilhisar": "kayseri", "bünyan": "kayseri", "pınarbaşı": "kayseri",
    "sungurlu": "çorum", "alaca": "çorum", "osmancık": "çorum",
    "şarkışla": "sivas", "suşehri": "sivas", "kangal": "sivas", "yıldızeli": "sivas",
    "sorgun": "yozgat", "yerköy": "yozgat", "boğazlıyan": "yozgat",

    # Karadeniz Bölgesi
    "bafra": "samsun", "çarşamba": "samsun", "vezirköprü": "samsun", "terme": "samsun", "havza": "samsun",
    "merzifon": "amasya", "suluova": "amasya", "taşova": "amasya",
    "turhal": "tokat", "erbaa": "tokat", "niksar": "tokat", "zile": "tokat",
    "ünye": "ordu", "fatsa": "ordu",
    "tosya": "kastamonu", "taşköprü": "kastamonu",
    "boyabat": "sinop",

    # Güneydoğu & Doğu Anadolu Bölgesi
    "siverek": "şanlıurfa", "viranşehir": "şanlıurfa", "birecik": "şanlıurfa", "suruç": "şanlıurfa",
    "akçakale": "şanlıurfa", "ceylanpınar": "şanlıurfa", "harran": "şanlıurfa", "bozova": "şanlıurfa", "halfeti": "şanlıurfa", "hilvan": "şanlıurfa",
    "nizip": "gaziantep", "islahiye": "gaziantep", "araban": "gaziantep",
    "kızıltepe": "mardin", "nusaybin": "mardin", "midyat": "mardin", "derik": "mardin",
    "ergani": "diyarbakır", "bismil": "diyarbakır", "silvan": "diyarbakır", "çınar": "diyarbakır", "dicle": "diyarbakır",
    "cizre": "şırnak", "silopi": "şırnak", "idil": "şırnak",
    "yüksekova": "hakkari", "şemdinli": "hakkari", "çukurca": "hakkari",
    "doğubayazıt": "ağrı", "patnos": "ağrı",
    "erciş": "van", "tuşba": "van", "ipekyolu": "van",
    "tatvan": "bitlis", "ahlat": "bitlis", "adilcevaz": "bitlis",
    "kahta": "adıyaman", "besni": "adıyaman",
    "kovancılar": "elazığ", "karakoçan": "elazığ",
}

# 2. Türkiye Lokasyonları (81 İl, İlçeler, Havzalar, Ovalar, Barajlar ve Göller)
TURKEY_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # 81 İl Merkezi
    "adana": (37.0017, 35.3289, "Adana"),
    "adıyaman": (37.7648, 38.2786, "Adıyaman"),
    "afyonkarahisar": (38.7569, 30.5387, "Afyonkarahisar"),
    "afyon": (38.7569, 30.5387, "Afyonkarahisar"),
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
    "hatay": (36.2023, 36.1606, "Hatay"),
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
    "kocaeli": (40.7654, 29.9408, "Kocaeli"),
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
    "sakarya": (40.7569, 30.3783, "Sakarya"),
    "adapazarı": (40.7569, 30.3783, "Sakarya / Adapazarı"),
    "samsun": (41.2867, 36.3300, "Samsun"),
    "siirt": (37.9333, 41.9500, "Siirt"),
    "sinop": (42.0231, 35.1531, "Sinop"),
    "sivas": (39.7477, 37.0179, "Sivas"),
    "tekirdağ": (40.9833, 27.5167, "Tekirdağ"),
    "tokat": (40.3167, 36.5500, "Tokat"),
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
    "meriç": (41.4000, 26.5000, "Meriç Nehri"),
    "gediz": (38.6000, 27.5000, "Gediz Havzası"),
    "büyük menderes": (37.9000, 28.3000, "Büyük Menderes Havzası"),
    "küçük menderes": (38.1000, 27.8000, "Küçük Menderes Havzası"),
    "seyhan": (36.9500, 35.3000, "Seyhan Havzası"),
    "ceyhan havzası": (37.0000, 35.8000, "Ceyhan Havzası"),
    "çoruh": (41.1000, 41.6000, "Çoruh Havzası"),
    "aras": (40.1000, 43.5000, "Aras Nehri"),
    "asi nehri": (36.1500, 36.0000, "Asi Nehri"),
    "van gölü": (38.6000, 42.9000, "Van Gölü"),
    "tuz gölü": (38.8000, 33.3000, "Tuz Gölü"),
    "beyşehir": (37.7000, 31.5000, "Beyşehir Gölü"),
    "eğirdir": (38.0000, 30.8000, "Eğirdir Gölü"),
    "sapanca": (40.7000, 30.2000, "Sapanca Gölü"),
    "manyas": (40.2000, 27.9500, "Manyas Kuşcenneti"),
    "iznik gölü": (40.4300, 29.5000, "İznik Gölü"),

    # Önemli Barajlar, Ovalar ve Tarım Alanları
    "atatürk barajı": (37.4722, 38.3183, "Atatürk Barajı"),
    "atatürk baraj": (37.4722, 38.3183, "Atatürk Barajı"),
    "keban barajı": (38.8039, 38.7564, "Keban Barajı"),
    "keban baraj": (38.8039, 38.7564, "Keban Barajı"),
    "ılısu barajı": (37.5303, 41.8286, "Ilısu Barajı"),
    "ılısu baraj": (37.5303, 41.8286, "Ilısu Barajı"),
    "deriner barajı": (41.1969, 41.8681, "Deriner Barajı"),
    "yusufeli barajı": (40.8258, 41.5369, "Yusufeli Barajı"),
    "karakaya barajı": (38.2250, 38.6367, "Karakaya Barajı"),
    "altınkaya barajı": (41.3500, 35.7000, "Altınkaya Barajı"),
    "hirfanlı barajı": (39.2700, 33.5200, "Hirfanlı Barajı"),
    "yuvacık barajı": (40.6650, 29.9700, "Yuvacık Barajı (Kocaeli)"),
    "ömerli barajı": (41.0500, 29.3500, "Ömerli Barajı (İstanbul)"),
    "terkos gölü": (41.3300, 28.5300, "Terkos Gölü (İstanbul)"),
    "darlık barajı": (41.1100, 29.5600, "Darlık Barajı (İstanbul)"),
    "büyükçekmece barajı": (41.0600, 28.5500, "Büyükçekmece Barajı"),
    "sazlıdere barajı": (41.1200, 28.7300, "Sazlıdere Barajı"),
    "alibeyköy barajı": (41.1100, 28.9300, "Alibeyköy Barajı"),
    "tahtalı barajı": (38.1600, 27.1000, "Tahtalı Barajı (İzmir)"),
    "gördes barajı": (38.9300, 28.2900, "Gördes Barajı (Manisa)"),
    "kurtboğazı barajı": (40.2600, 32.7000, "Kurtboğazı Barajı (Ankara)"),
    "çamlıdere barajı": (40.5000, 32.4800, "Çamlıdere Barajı (Ankara)"),

    # Bölgesel Projeler ve Ovalar
    "gap": (37.3000, 39.0000, "GAP Bölgesi"),
    "güneydoğu anadolu projesi": (37.3000, 39.0000, "GAP Bölgesi"),
    "çukurova": (36.9500, 35.4000, "Çukurova Tarım Havzası"),
    "trakya": (41.3000, 27.5000, "Trakya Tarım Bölgesi"),
    "harran": (36.8700, 39.0200, "Harran Ovası"),
    "bafra ovası": (41.5600, 35.9000, "Bafra Ovası"),
    "bafra": (41.5600, 35.9000, "Bafra Ovası"),
    "çarşamba ovası": (41.2000, 36.7200, "Çarşamba Ovası"),
    "çarşamba": (41.2000, 36.7200, "Çarşamba"),
    "terme": (41.2092, 36.9739, "Samsun / Terme"),
    "havza": (40.9786, 35.6586, "Samsun / Havza"),
    "vezirköprü": (41.1436, 35.4547, "Samsun / Vezirköprü"),
    "söke ovası": (37.7500, 27.4000, "Söke Ovası"),
    "söke": (37.7500, 27.4000, "Söke Ovası"),
    "menemen": (38.6000, 27.0600, "Menemen Ovası"),
    "amasya ovası": (40.6500, 35.8000, "Amasya Ovası"),
    "gediz ovası": (38.6500, 27.6000, "Gediz Ovası"),
    "konya ovası": (37.8500, 32.5000, "Konya Ovası"),
    "ceylanpınar": (36.8333, 39.9167, "Ceylanpınar TİGEM"),

    # Başlıca Tarım & Su İlçeleri
    "çeşme": (38.3236, 26.3042, "İzmir / Çeşme"),
    "urla": (38.3225, 26.7642, "İzmir / Urla"),
    "seferihisar": (38.1978, 26.8389, "İzmir / Seferihisar"),
    "torbalı": (38.1517, 27.3619, "İzmir / Torbalı"),
    "kemalpaşa": (38.4264, 27.4178, "İzmir / Kemalpaşa"),
    "ödemiş": (38.2289, 27.9733, "İzmir / Ödemiş"),
    "bergama": (39.1200, 27.1800, "İzmir / Bergama"),
    "tire": (38.0889, 27.7333, "İzmir / Tire"),
    "akhisar": (38.9222, 27.8400, "Manisa / Akhisar"),
    "salihli": (38.4800, 28.1300, "Manisa / Salihli"),
    "alaşehir": (38.3500, 28.5200, "Manisa / Alaşehir"),
    "turgutlu": (38.4900, 27.7000, "Manisa / Turgutlu"),
    "kırkağaç": (39.1050, 27.6717, "Manisa / Kırkağaç"),
    "soma": (39.1867, 27.6089, "Manisa / Soma"),
    "kuşadası": (37.8600, 27.2600, "Aydın / Kuşadası"),
    "didim": (37.3800, 27.2700, "Aydın / Didim"),
    "nazilli": (37.9150, 28.3225, "Aydın / Nazilli"),
    "çine": (37.6158, 28.0644, "Aydın / Çine"),
    "germencik": (37.8717, 27.5989, "Aydın / Germencik"),
    "silifke": (36.3775, 33.9344, "Mersin / Silifke"),
    "tarsus": (36.9167, 34.8956, "Mersin / Tarsus"),
    "anamur": (36.0750, 32.8333, "Mersin / Anamur"),
    "erdemli": (36.6050, 34.3083, "Mersin / Erdemli"),
    "kozan": (37.4550, 35.8150, "Adana / Kozan"),
    "ceyhan": (37.0250, 35.8167, "Adana / Ceyhan"),
    "alanya": (36.5438, 31.9997, "Antalya / Alanya"),
    "manavgat": (36.7867, 31.4439, "Antalya / Manavgat"),
    "serik": (36.9189, 31.1017, "Antalya / Serik"),
    "kumluca": (36.3700, 30.2900, "Antalya / Kumluca"),
    "finike": (36.2956, 30.1417, "Antalya / Finike"),
    "kaş": (36.2000, 29.6389, "Antalya / Kaş"),
    "elmalı": (36.7333, 29.9167, "Antalya / Elmalı"),
    "korkuteli": (37.0667, 30.1989, "Antalya / Korkuteli"),
    "bodrum": (37.0383, 27.4292, "Muğla / Bodrum"),
    "fethiye": (36.6217, 29.1164, "Muğla / Fethiye"),
    "milas": (37.3167, 27.7833, "Muğla / Milas"),
    "bandırma": (40.3522, 27.9767, "Balıkesir / Bandırma"),
    "edremit": (39.5961, 27.0244, "Balıkesir / Edremit"),
    "gönen": (40.1050, 27.6539, "Balıkesir / Gönen"),
    "biga": (40.2289, 27.2422, "Çanakkale / Biga"),
    "lüleburgaz": (41.4056, 27.3589, "Kırklareli / Lüleburgaz"),
    "çorlu": (41.1594, 27.8000, "Tekirdağ / Çorlu"),
    "çerkezköy": (41.2856, 28.0014, "Tekirdağ / Çerkezköy"),
    "uzunköprü": (41.2708, 26.6858, "Edirne / Uzunköprü"),
    "keşan": (40.8569, 26.6319, "Edirne / Keşan"),
    "ipsala": (40.9214, 26.3828, "Edirne / İpsala"),
    "havsa": (41.5492, 26.8208, "Edirne / Havsa"),
    "silivri": (41.0742, 28.2478, "İstanbul / Silivri"),
    "çatalca": (41.1439, 28.4611, "İstanbul / Çatalca"),
    "karacabey": (40.2150, 28.3600, "Bursa / Karacabey"),
    "inegöl": (40.0781, 29.5133, "Bursa / İnegöl"),
    "mustafakemalpaşa": (40.0350, 28.4117, "Bursa / M.Kemalpaşa"),
    "sandıklı": (38.4650, 30.2700, "Afyon / Sandıklı"),
    "dinar": (38.0650, 30.1650, "Afyon / Dinar"),
    "bolvadin": (38.7117, 31.0489, "Afyon / Bolvadin"),
    "emirdağ": (38.9289, 31.1500, "Afyon / Emirdağ"),
    "çumra": (37.5731, 32.7744, "Konya / Çumra"),
    "karapınar": (37.7139, 33.5506, "Konya / Karapınar"),
    "akşehir": (38.3575, 31.4164, "Konya / Akşehir"),
    "cihanbeyli": (38.6567, 32.9261, "Konya / Cihanbeyli"),
    "kulu": (39.0950, 33.0800, "Konya / Kulu"),
    "ereğli": (37.5133, 34.0500, "Konya / Ereğli"),
    "seydişehir": (37.4194, 31.8469, "Konya / Seydişehir"),
    "kadınhanı": (38.2389, 32.2139, "Konya / Kadınhanı"),
    "sarayönü": (38.2619, 32.4042, "Konya / Sarayönü"),
    "ilgın": (38.2792, 31.9169, "Konya / Ilgın"),
    "polatlı": (39.5800, 32.1400, "Ankara / Polatlı"),
    "beypazarı": (40.1681, 31.9211, "Ankara / Beypazarı"),
    "haymana": (39.4319, 32.4967, "Ankara / Haymana"),
    "şereflikoçhisar": (38.9389, 33.5389, "Ankara / Şereflikoçhisar"),
    "nallıhan": (40.1844, 31.3528, "Ankara / Nallıhan"),
    "çubuk": (40.2386, 33.0322, "Ankara / Çubuk"),
    "develi": (38.3900, 35.4900, "Kayseri / Develi"),
    "sungurlu": (40.1667, 34.3750, "Çorum / Sungurlu"),
    "merzifon": (40.8739, 35.4628, "Amasya / Merzifon"),
    "suluova": (40.8286, 35.6561, "Amasya / Suluova"),
    "taşova": (40.7783, 36.3217, "Amasya / Taşova"),
    "turhal": (40.3900, 36.0900, "Tokat / Turhal"),
    "erbaa": (40.6700, 36.5700, "Tokat / Erbaa"),
    "zile": (40.3000, 35.8800, "Tokat / Zile"),
    "niksar": (40.5900, 36.9500, "Tokat / Niksar"),
    "ünye": (41.1300, 37.2800, "Ordu / Ünye"),
    "fatsa": (41.0300, 37.5000, "Ordu / Fatsa"),
    "şarkışla": (39.3500, 36.4100, "Sivas / Şarkışla"),
    "bucak": (37.4592, 30.5950, "Burdur / Bucak"),
    "siverek": (37.7550, 39.3175, "Şanlıurfa / Siverek"),
    "viranşehir": (37.2358, 39.7631, "Şanlıurfa / Viranşehir"),
    "birecik": (37.0256, 37.9781, "Şanlıurfa / Birecik"),
    "suruç": (36.9761, 38.4253, "Şanlıurfa / Suruç"),
    "akçakale": (36.7111, 38.9483, "Şanlıurfa / Akçakale"),
    "bozova": (37.3622, 38.5256, "Şanlıurfa / Bozova"),
    "halfeti": (37.2464, 37.8681, "Şanlıurfa / Halfeti"),
    "hilvan": (37.5858, 38.9567, "Şanlıurfa / Hilvan"),
    "nizip": (37.0108, 37.7944, "Gaziantep / Nizip"),
    "islahiye": (37.0264, 36.6311, "Gaziantep / İslahiye"),
    "araban": (37.4239, 37.6889, "Gaziantep / Araban"),
    "kadirli": (37.3750, 36.0964, "Osmaniye / Kadirli"),
    "dörtyol": (36.8400, 36.2200, "Hatay / Dörtyol"),
    "iskenderun": (36.5872, 36.1733, "Hatay / İskenderun"),
    "kırıkhan": (36.4950, 36.3575, "Hatay / Kırıkhan"),
    "reyhanlı": (36.2683, 36.5683, "Hatay / Reyhanlı"),
    "ergani": (38.2689, 39.7639, "Diyarbakır / Ergani"),
    "bismil": (37.8469, 40.6669, "Diyarbakır / Bismil"),
    "silvan": (38.1408, 41.0106, "Diyarbakır / Silvan"),
    "çınar": (37.7214, 40.4139, "Diyarbakır / Çınar"),
    "kızıltepe": (37.1939, 40.5878, "Mardin / Kızıltepe"),
    "midyat": (37.4189, 41.3389, "Mardin / Midyat"),
    "nusaybin": (37.0758, 41.2178, "Mardin / Nusaybin"),
    "derik": (37.3628, 40.2708, "Mardin / Derik"),
    "cizre": (37.3272, 42.1894, "Şırnak / Cizre"),
    "silopi": (37.1750, 42.4722, "Şırnak / Silopi"),
    "idil": (37.3417, 41.8906, "Şırnak / İdil"),
    "yüksekova": (37.5736, 44.2872, "Hakkari / Yüksekova"),
    "şemdinli": (37.2961, 44.5756, "Hakkari / Şemdinli"),
    "çukurca": (37.2472, 43.6139, "Hakkari / Çukurca"),
    "erciş": (39.0278, 43.3589, "Van / Erciş"),
    "tuşba": (38.5200, 43.3700, "Van / Tuşba"),
    "ipekyolu": (38.4900, 43.3900, "Van / İpekyolu"),
    "tatvan": (38.5083, 42.2811, "Bitlis / Tatvan"),
    "ahlat": (38.7517, 42.4939, "Bitlis / Ahlat"),
    "adilcevaz": (38.8028, 42.7306, "Bitlis / Adilcevaz"),
    "doğubayazıt": (39.5469, 44.0839, "Ağrı / Doğubayazıt"),
    "patnos": (39.2333, 42.8667, "Ağrı / Patnos"),
    "kahta": (37.7844, 38.6250, "Adıyaman / Kahta"),
    "besni": (37.6939, 37.8617, "Adıyaman / Besni"),
}

# 3. Küresel Sınır-Aşan Nehir Havzaları, Ülkeler ve Şehirler
GLOBAL_LOCATIONS: Dict[str, Tuple[float, float, str]] = {
    # Küresel Nehir Havzaları
    "nil": (15.5007, 32.5599, "Nil Nehri Havzası"),
    "nile": (15.5007, 32.5599, "Nil Nehri Havzası"),
    "ren": (50.9375, 6.9603, "Ren Nehri (Rhine) Havzası"),
    "rhine": (50.9375, 6.9603, "Ren Nehri Havzası"),
    "tuna": (44.6000, 22.0000, "Tuna Nehri (Danube) Havzası"),
    "danube": (44.6000, 22.0000, "Tuna Nehri Havzası"),
    "colorado": (36.0544, -112.1401, "Colorado Nehri Havzası"),
    "indus": (30.0000, 71.0000, "İndus Nehri Havzası"),
    "ganj": (25.5000, 85.0000, "Ganj Nehri Havzası"),
    "ganges": (25.5000, 85.0000, "Ganj Nehri Havzası"),
    "mekong": (11.5564, 104.9282, "Mekong Nehri Havzası"),
    "amazon": (-3.4653, -62.2159, "Amazon Havzası"),
    "mississippi": (38.0000, -90.0000, "Mississippi Havzası"),
    "yangtze": (30.5928, 114.3055, "Yangtze Nehri Havzası"),
    "yellow river": (36.0000, 106.0000, "Sarı Nehir Havzası"),
    "kongo": (-4.3217, 15.3126, "Kongo Nehri Havzası"),
    "zambezi": (-17.9244, 25.8567, "Zambezi Havzası"),
    "volga": (56.0000, 44.0000, "Volga Nehri Havzası"),
    "singur": (17.7500, 78.1200, "Singur Barajı / Hindistan"),
    "singur dam": (17.7500, 78.1200, "Singur Barajı"),

    # Ülkeler
    "hindistan": (20.5937, 78.9629, "Hindistan"),
    "india": (20.5937, 78.9629, "Hindistan"),
    "çin": (35.8617, 104.1954, "Çin"),
    "china": (35.8617, 104.1954, "Çin"),
    "abd": (37.0902, -95.7129, "Amerika Birleşik Devletleri"),
    "usa": (37.0902, -95.7129, "ABD"),
    "mısır": (26.8206, 30.8025, "Mısır"),
    "egypt": (26.8206, 30.8025, "Mısır"),
    "etiopya": (9.1450, 40.4897, "Etiyopya"),
    "etiyopya": (9.1450, 40.4897, "Etiyopya"),
    "sudan": (12.8628, 30.2176, "Sudan"),
    "irak": (33.2232, 43.6793, "Irak"),
    "iraq": (33.2232, 43.6793, "Irak"),
    "suriye": (34.8021, 38.9968, "Suriye"),
    "syria": (34.8021, 38.9968, "Suriye"),
    "iran": (32.4279, 53.6880, "İran"),
    "hollanda": (52.1326, 5.2913, "Hollanda"),
    "netherlands": (52.1326, 5.2913, "Hollanda"),
    "almanya": (51.1657, 10.4515, "Almanya"),
    "germany": (51.1657, 10.4515, "Almanya"),
    "ispanya": (40.4637, -3.7492, "İspanya"),
    "spain": (40.4637, -3.7492, "İspanya"),
    "italya": (41.8719, 12.5674, "İtalya"),
    "italy": (41.8719, 12.5674, "İtalya"),
    "fransa": (46.2276, 2.2137, "Fransa"),
    "france": (46.2276, 2.2137, "Fransa"),
    "yunanistan": (39.0742, 21.8243, "Yunanistan"),
    "greece": (39.0742, 21.8243, "Yunanistan"),
    "bulgaristan": (42.7339, 25.4858, "Bulgaristan"),
    "romanya": (45.9432, 24.9668, "Romanya"),
    "azerbaycan": (40.1431, 47.5769, "Azerbaycan"),
    "gürcistan": (42.3154, 43.3569, "Gürcistan"),
    "özbekistan": (41.3775, 64.5853, "Özbekistan"),
    "kazakistan": (48.0196, 66.9237, "Kazakistan"),
    "türkmenistan": (38.9697, 59.5563, "Türkmenistan"),
    "brezilya": (-14.2350, -51.9253, "Brezilya"),
    "brazil": (-14.2350, -51.9253, "Brezilya"),
    "avustralya": (-25.2744, 133.7751, "Avustralya"),
    "australia": (-25.2744, 133.7751, "Avustralya"),
    "israil": (31.0461, 34.8516, "İsrail"),
    "ürdün": (30.5852, 36.2384, "Ürdün"),
    "pakistan": (30.3753, 69.3451, "Pakistan"),
    "bangladeş": (23.6850, 90.3563, "Bangladeş"),
    "vietnam": (14.0583, 108.2772, "Vietnam"),
    "tayland": (15.8700, 100.9925, "Tayland"),
    "fas": (31.7917, -7.0926, "Fas"),
    "morocco": (31.7917, -7.0926, "Fas"),
    "cezayir": (28.0339, 1.6596, "Cezayir"),
    "tunus": (33.8869, 9.5375, "Tunus"),
    "güney afrika": (-30.5595, 22.9375, "Güney Afrika"),
    "kenya": (-0.0236, 37.9062, "Kenya"),
    "nijerya": (9.0820, 8.6753, "Nijerya"),
    "suudi arabistan": (23.8859, 45.0792, "Suudi Arabistan"),
    "birleşik krallık": (55.3781, -3.4360, "Birleşik Krallık"),
    "ingiltere": (52.3555, -1.1743, "Birleşik Krallık"),
    "uk": (55.3781, -3.4360, "Birleşik Krallık"),
    "japonya": (36.2048, 138.2529, "Japonya"),
    "japan": (36.2048, 138.2529, "Japonya"),
    "kore": (35.9078, 127.7669, "Güney Kore"),
    "rusya": (61.5240, 105.3188, "Rusya"),
    "russia": (61.5240, 105.3188, "Rusya"),
    "ukrayna": (48.3794, 31.1656, "Ukrayna"),
    "polonya": (51.9194, 19.1451, "Polonya"),
    "macaristan": (47.1625, 19.5033, "Macaristan"),
    "kanada": (56.1304, -106.3468, "Kanada"),
    "meksika": (23.6345, -102.5528, "Meksika"),
    "arjantin": (-38.4161, -63.6167, "Arjantin"),
    "şili": (-35.6751, -71.5430, "Şili"),
}

# 4. Coğrafi ve İdari Belirteçler (Collocation Indicators)
GEO_INDICATORS_TR: Set[str] = {
    "il", "ili", "ilinde", "iline", "ilinin",
    "ilce", "ilcesi", "ilcesinde", "ilcesine",
    "belediye", "belediyesi", "belediyesinin",
    "valilik", "valiligi", "valiligince",
    "kaymakamlik", "kaymakamligi",
    "buyuksehir", "buyuksehiri",
    "koy", "koyu", "koyunde",
    "mahalle", "mahallesi", "mahallesinde",
    "baraj", "baraji", "barajinda", "barajinin", "barajlar", "barajlari", "barajlarinda",
    "havza", "havzasi", "havzasinda", "havzasinin", "havzalar",
    "nehir", "nehri", "nehrinde", "nehrinin",
    "cay", "cayi", "cayinda",
    "dere", "deresi", "deresinde",
    "gol", "golu", "golunde", "golunun",
    "golet", "goleti", "goletinde",
    "ova", "ovasi", "ovasinda", "ovasinin",
    "yayla", "yaylasi", "yaylasinda",
    "mera", "merasi", "merasinda",
    "ciftlik", "ciftligi", "ciftliginde",
    "sulama", "sulamasi", "sulamasinda",
    "dsi", "sygm", "tigem",
    "tarim il", "tarim ve orman", "sulama birligi",
    "su idaresi", "iski", "izsu", "aski", "deski", "maski", "saski", "gaski", "kaski"
}

GEO_INDICATORS_EN: Set[str] = {
    "basin", "basins", "watershed", "watersheds",
    "river", "rivers", "lake", "lakes", "reservoir", "reservoirs",
    "dam", "dams", "delta", "deltasi", "deltada", "deltanin", "valley",
    "province", "district", "city of", "municipality",
    "irrigation", "drought in", "flooding in", "floods in",
    "water supply in", "water crisis in", "water authority"
}

def _clean_alert_query_from_source(source: str) -> str:
    """Google Alert arama sorgusu etiketlerini temizler."""
    if not source:
        return ""
    s = re.sub(r'Google\s+(?:Alert|Uyarı)\s*[-–—:]\s*["\'][^"\']+["\']', '', source, flags=re.IGNORECASE)
    s = re.sub(r'Google\s+(?:Alert|Uyarı)', '', s, flags=re.IGNORECASE)
    return s.strip()

def _normalize_text(text: str) -> str:
    """Türkçe karakterleri ve noktalama işaretlerini standartlaştırır."""
    if not text:
        return ""
    t = text.lower()
    t = t.replace("i̇", "i").replace("ı", "i").replace("ğ", "g")
    t = t.replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return " ".join(t.split())

def _check_homonym_validity(keyword_norm: str, text_norm: str, is_turkish_feed: bool) -> bool:
    """
    Kelimelerin çift anlamlılık (homonym) durumlarını denetler.
    Tarım mısırı, askeri ordu, taşıt van gibi sahte pozitifleri kesin olarak eler.
    """
    if keyword_norm == "misir":
        # Tarımsal mısır bitkisi kontrolü
        corn_terms = {
            "hasat", "hasadi", "ekim", "ekimi", "dane", "tohum", "tohumu", "cesit", "cesitleri",
            "yetistirici", "yetistiricileri", "silaj", "silaji", "fiyat", "fiyati", "fiyatlari",
            "yem", "yemi", "verim", "verimi", "zararli", "zararlisi", "tarla", "tarlasi",
            "corn", "maize", "grain", "usda", "hybrid", "stover"
        }
        words = set(text_norm.split())
        if words.intersection(corn_terms):
            egypt_country_terms = {"kahire", "cairo", "hukumet", "devlet", "bakanlik", "suez", "nil", "nile", "egypt", "egyptian"}
            if not words.intersection(egypt_country_terms):
                return False  # Mısır bitkisidir, Mısır ülkesi değildir!

    elif keyword_norm == "ordu":
        # Askeri ordu kontrolü
        military_terms = {"asker", "askeri", "birlik", "birlikleri", "tugay", "komutan", "komutani", "general", "ordusu", "isgal", "savunma", "guvenlik", "silahli"}
        words = set(text_norm.split())
        if words.intersection(military_terms):
            city_terms = {"ili", "ilinde", "valiligi", "belediyesi", "unye", "fatsa", "altinordu", "karadeniz"}
            if not words.intersection(city_terms):
                return False

    elif keyword_norm == "van":
        # Panelvan araç veya İngilizce "van der/moving van"
        if not is_turkish_feed:
            eng_van_terms = {"delivery van", "moving van", "van der", "van den", "vanguard", "caravan"}
            if any(term in text_norm for term in eng_van_terms) or not any(k in text_norm for k in ["lake van", "van province", "van goli", "turkey"]):
                return False
        else:
            vehicle_terms = {"panelvan", "minibus", "kamyonet", "arac", "servis araci"}
            words = set(text_norm.split())
            if words.intersection(vehicle_terms) and not any(k in text_norm for k in ["golu", "ili", "valiligi", "belediyesi", "ercis", "tusba", "ipekyolu"]):
                return False

    elif keyword_norm == "gap":
        # İngilizce "yield gap", "price gap"
        if not is_turkish_feed or any(k in text_norm for k in ["yield gap", "knowledge gap", "price gap", "bridge the gap", "generation gap"]):
            if not any(k in text_norm for k in ["guneydogu anadolu", "gap bolgesi", "gap idaresi", "gap sulama", "gap projesi"]):
                return False

    elif keyword_norm == "tire":
        if not is_turkish_feed or any(k in text_norm for k in ["flat tire", "rubber tire", "tire pressure", "tire wear"]):
            if not any(k in text_norm for k in ["izmir", "ilcesi", "ilcesinde", "belediyesi", "organize"]):
                return False

    elif keyword_norm == "kas":
        if not any(k in text_norm for k in ["antalya", "ilcesi", "ilcesinde", "belediyesi", "kaymakamligi", "demre", "kalkan"]):
            return False

    elif keyword_norm == "bor":
        # Bor madeni mi yoksa Niğde Bor ilçesi mi
        if any(k in text_norm for k in ["maden", "madeni", "eti maden", "karbur", "element", "gubre", "gubreleme", "asit"]):
            if not any(k in text_norm for k in ["nigde", "ilcesi", "ilcesinde", "belediyesi", "ovasi"]):
                return False

    elif keyword_norm == "aras":
        if not any(k in text_norm for k in ["nehir", "nehri", "nehrinde", "havza", "havzasi", "edash", "kars", "igdir", "erzurum"]):
            return False

    elif keyword_norm == "ren":
        if not any(k in text_norm for k in ["nehir", "nehri", "rhine", "havza", "havzasi", "germany", "almanya"]):
            return False

    return True

def evaluate_article_location(article: Dict[str, Any], index_seed: int = 0) -> Tuple[Optional[float], Optional[float], Optional[str], int, str]:
    """
    Çok Yöntemli Coğrafi Değerlendirme Pipeline'ı (7 Aşamalı).
    (lat, lng, loc_name, confidence_score, audit_reason) döner.
    Güven skoru >= 70 ise konum doğrulanmış kabul edilir; aksi halde (None, None, None, score, reason) döner.
    """
    title_tr = article.get("title_tr") or ""
    title_en = article.get("title") or ""
    summary_tr = article.get("summary_tr") or article.get("description") or ""
    source_raw = article.get("source_feed") or article.get("source") or ""
    guid = article.get("guid") or str(article.get("id") or "")

    # Aşama 1: Kaynak Arama Sorgusu Temizleme
    cleaned_source = _clean_alert_query_from_source(source_raw)

    is_tr_feed = bool(
        article.get("is_turkey")
        or "🇹🇷" in source_raw
        or guid.startswith("tr_")
        or guid.startswith("sygm:")
        or any(k in cleaned_source.lower() for k in ["iha", "dha", "aa", "anadolu", "tarım", "dsi", "iski", "belediye", "gazete", "bülten", "ajans"])
    )

    norm_title = _normalize_text(f"{title_tr} {title_en}")
    norm_summary = _normalize_text(summary_tr)
    norm_first_sentence = norm_summary.split(".")[0] if "." in norm_summary else norm_summary[:120]
    full_norm = f"{norm_title} {norm_summary} {_normalize_text(cleaned_source)}"

    turkey_keys = sorted(TURKEY_LOCATIONS.keys(), key=lambda k: len(_normalize_text(k)), reverse=True)
    global_keys = sorted(GLOBAL_LOCATIONS.keys(), key=lambda k: len(_normalize_text(k)), reverse=True)

    candidates: Dict[Tuple[str, str], Dict[str, Any]] = {}

    # Aşama 2, 3, 4: Türkiye Lokasyon Adaylarını Değerlendir
    for kw in turkey_keys:
        kw_norm = _normalize_text(kw)
        pattern = r"\b" + re.escape(kw_norm) + r"\b"

        in_title = bool(re.search(pattern, norm_title))
        in_lead = bool(re.search(pattern, norm_first_sentence))
        in_summary = bool(re.search(pattern, norm_summary))

        if not (in_title or in_lead or in_summary):
            continue

        if not _check_homonym_validity(kw_norm, full_norm, is_tr_feed):
            continue

        score = 0
        reasons = []

        # Pozisyonel Ağırlıklandırma
        if in_title:
            score += 45
            reasons.append("başlıkta_doğrulandı(+45)")
        elif in_lead:
            score += 30
            reasons.append("giriş_cümlesinde_tespit(+30)")
        elif in_summary:
            score += 20
            reasons.append("özette_tespit(+20)")

        # Coğrafi / İdari Belirteç Denetimi (±6 kelime penceresi)
        kw_words = kw_norm.split()
        all_words = full_norm.split()
        for idx, w in enumerate(all_words):
            if w == kw_words[0] and all_words[idx:idx + len(kw_words)] == kw_words:
                window_start = max(0, idx - 6)
                window_end = min(len(all_words), idx + len(kw_words) + 6)
                surrounding = set(all_words[window_start:window_end])
                matched_ind = surrounding.intersection(GEO_INDICATORS_TR | GEO_INDICATORS_EN)
                if matched_ind:
                    score += 25
                    reasons.append(f"coğrafi_niteleyici({','.join(list(matched_ind)[:2])})(+25)")
                    break

        if is_tr_feed:
            score += 10
            reasons.append("yerel_kaynak_uyumu(+10)")

        candidates[("turkey", kw)] = {"score": score, "reasons": reasons, "kw": kw, "type": "turkey"}

    # Aşama 5: Hiyerarşik Çapraz Doğrulama (İlçe + İl)
    for (ctype, kw), cdata in list(candidates.items()):
        if ctype == "turkey":
            kw_norm = _normalize_text(kw)
            parent_prov = DISTRICT_TO_PROVINCE.get(kw_norm)
            if parent_prov:
                parent_norm = _normalize_text(parent_prov)
                if re.search(r"\b" + re.escape(parent_norm) + r"\b", full_norm):
                    cdata["score"] += 35
                    cdata["reasons"].append(f"ilçe_il_çapraz_doğrulaması({parent_prov})(+35)")

    # Küresel Lokasyon Adaylarını Değerlendir
    for kw in global_keys:
        kw_norm = _normalize_text(kw)
        pattern = r"\b" + re.escape(kw_norm) + r"\b"

        in_title = bool(re.search(pattern, norm_title))
        in_lead = bool(re.search(pattern, norm_first_sentence))
        in_summary = bool(re.search(pattern, norm_summary))

        if not (in_title or in_lead or in_summary):
            continue

        if not _check_homonym_validity(kw_norm, full_norm, is_tr_feed):
            continue

        score = 0
        reasons = []
        if in_title:
            score += 45
            reasons.append("başlıkta_doğrulandı(+45)")
        elif in_lead:
            score += 30
            reasons.append("giriş_cümlesinde_tespit(+30)")
        elif in_summary:
            score += 20
            reasons.append("özette_tespit(+20)")

        kw_words = kw_norm.split()
        all_words = full_norm.split()
        for idx, w in enumerate(all_words):
            if w == kw_words[0] and all_words[idx:idx + len(kw_words)] == kw_words:
                window_start = max(0, idx - 6)
                window_end = min(len(all_words), idx + len(kw_words) + 6)
                surrounding = set(all_words[window_start:window_end])
                matched_ind = surrounding.intersection(GEO_INDICATORS_TR | GEO_INDICATORS_EN)
                if matched_ind:
                    score += 25
                    reasons.append(f"küresel_havza_niteleyici({','.join(list(matched_ind)[:2])})(+25)")
                    break

        candidates[("global", kw)] = {"score": score, "reasons": reasons, "kw": kw, "type": "global"}

    if not candidates:
        return (None, None, None, 0, "Doğrulanmış coğrafi varlık bulunamadı")

    # Aşama 6: Çoklu Aday ve Çatışma Çözümleme
    sorted_candidates = sorted(candidates.values(), key=lambda c: c["score"], reverse=True)
    best = sorted_candidates[0]

    # Aşama 7: Güven Eşiği (Score >= 70)
    CONFIDENCE_THRESHOLD = 70
    if best["score"] < CONFIDENCE_THRESHOLD:
        return (None, None, None, best["score"], f"Eşik altı güven skoru ({best['score']}<{CONFIDENCE_THRESHOLD}): {'; '.join(best['reasons'])}")

    if len(sorted_candidates) > 1:
        second = sorted_candidates[1]
        if best["score"] - second["score"] < 10 and best["kw"] != second["kw"]:
            b_norm = _normalize_text(best["kw"])
            s_norm = _normalize_text(second["kw"])
            if DISTRICT_TO_PROVINCE.get(b_norm) == s_norm or DISTRICT_TO_PROVINCE.get(s_norm) == b_norm:
                # İlçe ile il birlikte ise daha hassas olan ilçeyi tercih et
                if DISTRICT_TO_PROVINCE.get(s_norm) == b_norm:
                    best = second
            else:
                # Farklı 3 il eşit yoğunlukta geçiyorsa genel/dağınık haberdir
                if len(sorted_candidates) >= 3 and sorted_candidates[2]["score"] >= 65:
                    return (None, None, None, best["score"], "Çoklu bölge genel haberi (tek konuma indirgenemez)")

    ctype = best["type"]
    kw = best["kw"]
    if ctype == "turkey":
        lat, lng, loc_name = TURKEY_LOCATIONS[kw]
        kw_norm = _normalize_text(kw)
        max_rad = 3.5 if kw_norm in DISTRICT_TO_PROVINCE else 6.5
    else:
        lat, lng, loc_name = GLOBAL_LOCATIONS[kw]
        max_rad = 20.0

    seed_str = f"{guid}_{title_tr}_{index_seed}"
    h = int(hashlib.md5(seed_str.encode("utf-8")).hexdigest()[:8], 16)
    radius_deg = (max_rad / 111.0) * math.sqrt((h % 1000) / 1000.0)
    angle_rad = ((h // 1000) % 360) * (math.pi / 180.0)
    j_lat = radius_deg * math.sin(angle_rad)
    j_lng = radius_deg * math.cos(angle_rad)

    audit_str = f"Skor: {best['score']}/100 | Doğrulama: {'; '.join(best['reasons'])}"
    return (round(lat + j_lat, 4), round(lng + j_lng, 4), loc_name, best["score"], audit_str)

def geocode_article(article: Dict[str, Any], index_seed: int = 0) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Mevcut portalla tam geriye uyumlu arayüz fonksiyonu.
    Gelişmiş 7 aşamalı değerlendirme sonucunda eşiği aşan (doğrulanmış) konumu döner;
    eşiği aşamayan haberler için (None, None, None) döner.
    """
    lat, lng, loc_name, _, _ = evaluate_article_location(article, index_seed)
    return (lat, lng, loc_name)
