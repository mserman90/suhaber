"""
app/events_data.py
Uluslararası Öneme Sahip Zirveler, Kongreler ve Toplantılar Veri Tabanı & Arayüz Bileşenleri.
Su Gündemi, Tarım Gündemi ve Hayvancılık Gündemi kanallarına özel,
küresel politikaları, anlaşmaları ve bilimsel gündemi belirleyen en prestijli etkinlikler.
"""

import html
import urllib.parse
from typing import Dict, List, Any

# Kanal Başlık ve Açıklamaları
CHANNEL_EVENTS_METADATA: Dict[str, Dict[str, str]] = {
    "water": {
        "title_tr": "💧 Uluslararası Su Zirveleri, Kongreler ve Taraflar Konferansları",
        "title_en": "💧 International Water Summits, Congresses & Conferences",
        "desc_tr": "Küresel su güvenliği, sınır-aşan havzaların yönetimi, kuraklık finansmanı ve BM SDG 6 hedeflerini belirleyen en kritik uluslararası buluşmalar.",
        "desc_en": "The most critical global gatherings directing transboundary basin treaties, international water diplomacy, drought finance, and UN SDG 6.",
        "badge_tr": "🌐 KÜRESEL SU GÜNDEMİ & DİPLOMASİSİ",
        "badge_en": "🌐 GLOBAL WATER AGENDA & DIPLOMACY"
    },
    "agriculture": {
        "title_tr": "🌾 Uluslararası Tarım, Gıda Güvenliği & Agronomi Zirveleri",
        "title_en": "🌾 International Agriculture, Food Security & Agronomy Summits",
        "desc_tr": "Dünya tarım politikaları, tohum güvenliği, hassas tarım teknolojileri ve küresel gıda arzını belirleyen en üst düzey uluslararası zirveler.",
        "desc_en": "Leading multilateral summits shaping international food security, certified seed systems, smart precision agriculture, and zero hunger policies.",
        "badge_tr": "🌐 KÜRESEL TARIM GÜNDEMİ & İNOVASYON",
        "badge_en": "🌐 GLOBAL AGRICULTURE AGENDA & INNOVATION"
    },
    "livestock": {
        "title_tr": "🐄 Uluslararası Hayvancılık, Sütçülük & Veterinerlik Zirveleri",
        "title_en": "🐄 International Livestock, Dairy & Veterinary Summits",
        "desc_tr": "Dünya süt ve kırmızı et piyasaları, hayvan refahı, sürü yönetimi teknolojileri ve Tek Sağlık (One Health) gündemini belirleyen küresel kongreler.",
        "desc_en": "Premier global congresses steering international dairy and beef economics, precision herd sensors, genetics, and the One Health framework.",
        "badge_tr": "🌐 KÜRESEL HAYVANCILIK & TEK SAĞLIK GÜNDEMİ",
        "badge_en": "🌐 GLOBAL LIVESTOCK & ONE HEALTH AGENDA"
    }
}

# Etkinlik Kategori Filtre Tanımları
EVENT_CATEGORIES: Dict[str, Dict[str, str]] = {
    "all": {
        "tr": "🌟 Tüm Zirveler",
        "en": "🌟 All Summits"
    },
    "un_gov": {
        "tr": "🏛️ BM & Hükümetlerarası",
        "en": "🏛️ UN & Intergovernmental"
    },
    "science_academic": {
        "tr": "🔬 Bilimsel Kongreler",
        "en": "🔬 Scientific Congresses"
    },
    "industry_expo": {
        "tr": "🚜 Sektörel & Fuarlar",
        "en": "🚜 Industry & Global Expos"
    },
    "treaty_policy": {
        "tr": "📜 Sözleşmeler & Politikalar",
        "en": "📜 Treaties & Policies"
    }
}

# 1. SU GÜNDEMİ (Water Agenda) Uluslararası Toplantıları
WATER_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "wwf-11",
        "channel": "water",
        "category": "un_gov",
        "acronym": "WWF 11",
        "title_tr": "11. Dünya Su Forumu",
        "title_en": "11th World Water Forum",
        "organizer_tr": "Dünya Su Konseyi (WWC) & Suudi Arabistan Su Bakanlığı",
        "organizer_en": "World Water Council (WWC) & Kingdom of Saudi Arabia",
        "date_display_tr": "2027 (Hazırlık Süreci: 2026)",
        "date_display_en": "2027 (Preparatory Process: 2026)",
        "cycle_tr": "3 Yılda Bir",
        "cycle_en": "Triennial",
        "location_city": "Riyad",
        "location_country_tr": "Suudi Arabistan",
        "location_country_en": "Saudi Arabia",
        "flag": "🇸🇦",
        "summary_tr": "Dünyanın en geniş katılımlı su zirvesi. Devlet başkanları, bakanlar, su idareleri ve uluslararası finans kuruluşları sınır-aşan havzaların yönetimi, kuraklık finansmanı ve su diplomasisini burada karara bağlar.",
        "summary_en": "The world's largest triennial water event bringing together heads of state, ministers, and water basin authorities to steer transboundary water diplomacy, arid climate resilience, and global investment.",
        "topics_tr": ["Sınır Aşan Sular", "Küresel Su Güvenliği", "Tuzdan Arındırma", "Su Diplomasisi"],
        "topics_en": ["Transboundary Waters", "Water Security", "Desalination", "Water Diplomacy"],
        "url": "https://www.worldwatercouncil.org/en/world-water-forum",
        "lat": 24.7136,
        "lng": 46.6753
    },
    {
        "id": "siwi-www-2026",
        "channel": "water",
        "category": "science_academic",
        "acronym": "SIWI WWW",
        "title_tr": "Stockholm Dünya Su Haftası 2026",
        "title_en": "Stockholm World Water Week 2026",
        "organizer_tr": "Stockholm Uluslararası Su Enstitüsü (SIWI)",
        "organizer_en": "Stockholm International Water Institute (SIWI)",
        "date_display_tr": "23 - 27 Ağustos 2026",
        "date_display_en": "August 23 - 27, 2026",
        "cycle_tr": "Her Yıl (Ağustos)",
        "cycle_en": "Annual (August)",
        "location_city": "Stockholm",
        "location_country_tr": "İsveç",
        "location_country_en": "Sweden",
        "flag": "🇸🇪",
        "summary_tr": "Küresel su topluluğunun en saygın yıllık düşünce platformu. Stockholm Su Ödülü'nün takdim edildiği haftada, su-iklim dengesi, döngüsel ekonomi ve nehir havzası ekosistemleri bilimsel oturumlarla tartışılır.",
        "summary_en": "The leading annual focal point for global water issues since 1991. Hosts the prestigious Stockholm Water Prize and guides evidence-based policies on water governance and freshwater resilience.",
        "topics_tr": ["Tatlı Su Ekosistemleri", "İklim Değişikliği", "Stockholm Su Ödülü", "Havza Yönetimi"],
        "topics_en": ["Freshwater Resilience", "Climate Action", "Stockholm Water Prize", "Basin Governance"],
        "url": "https://www.worldwaterweek.org/",
        "lat": 59.3293,
        "lng": 18.0686
    },
    {
        "id": "un-water-conf-2026",
        "channel": "water",
        "category": "un_gov",
        "acronym": "UN WATER",
        "title_tr": "Birleşmiş Milletler 2026 Su Konferansı",
        "title_en": "United Nations 2026 Water Conference",
        "organizer_tr": "Birleşmiş Milletler (UN-Water, BAE & Senegal Eş Başkanlığında)",
        "organizer_en": "United Nations (Co-hosted by UAE & Senegal)",
        "date_display_tr": "2 - 4 Aralık 2026",
        "date_display_en": "December 2 - 4, 2026",
        "cycle_tr": "Özel BM Zirvesi",
        "cycle_en": "Special UN Summit",
        "location_city": "Abu Dabi",
        "location_country_tr": "Birleşik Arap Emirlikleri",
        "location_country_en": "United Arab Emirates",
        "flag": "🇦🇪",
        "summary_tr": "BM Sürdürülebilir Kalkınma Amacı 6 (SDG 6: Herkes İçin Temiz Su) hedeflerinin küresel düzeyde hesap verebilirlik denetiminin yapılacağı, devletler arası bağlayıcı su eylem taahhütlerinin imzalanacağı tarihi zirve.",
        "summary_en": "High-level UN conference mandated to accelerate SDG 6 implementation worldwide, mobilizing multilateral commitments to solve accelerating groundwater depletion and transboundary scarcity.",
        "topics_tr": ["BM SDG 6 Hedefleri", "Küresel Eylem Gündemi", "Yeraltı Suyu Güvenliği", "Uluslararası Fonlar"],
        "topics_en": ["UN SDG 6", "Water Action Agenda", "Groundwater Security", "Multilateral Finance"],
        "url": "https://www.unwater.org/",
        "lat": 24.4539,
        "lng": 54.3773
    },
    {
        "id": "iwa-wwce-2026",
        "channel": "water",
        "category": "science_academic",
        "acronym": "IWA WWCE",
        "title_tr": "IWA Dünya Su Kongresi ve Sergisi 2026",
        "title_en": "IWA World Water Congress & Exhibition 2026",
        "organizer_tr": "Uluslararası Su Birliği (International Water Association - IWA)",
        "organizer_en": "International Water Association (IWA)",
        "date_display_tr": "11 - 15 Ekim 2026",
        "date_display_en": "October 11 - 15, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Glasgow",
        "location_country_tr": "Birleşik Krallık",
        "location_country_en": "United Kingdom",
        "flag": "🇬🇧",
        "summary_tr": "10.000'den fazla su kamu idaresi yöneticisi (İSKİ, İZSU eşdeğerleri), mühendis ve bilim insanının katıldığı; ileri atık su geri kazanımı, dijital ikizler ve kayıp-kaçak kontrolü teknolojileri kongresi.",
        "summary_en": "Over 10,000 water professionals and municipal utility leaders gather to review transformative wastewater reclamation technologies, digital twins, and AI-enabled leak detection systems.",
        "topics_tr": ["İleri Arıtma", "Kayıp-Kaçak Yönetimi", "Akıllı Su Şebekeleri", "Döngüsel Ekonomi"],
        "topics_en": ["Advanced Wastewater", "Non-Revenue Water", "Smart Water Grids", "Circular Economy"],
        "url": "https://worldwatercongress.org/",
        "lat": 55.8642,
        "lng": -4.2518
    },
    {
        "id": "global-water-summit-2026",
        "channel": "water",
        "category": "industry_expo",
        "acronym": "GWS 2026",
        "title_tr": "Küresel Su Zirvesi 2026 (Global Water Summit)",
        "title_en": "Global Water Summit 2026",
        "organizer_tr": "Global Water Intelligence (GWI)",
        "organizer_en": "Global Water Intelligence (GWI)",
        "date_display_tr": "18 - 20 Mayıs 2026",
        "date_display_en": "May 18 - 20, 2026",
        "cycle_tr": "Her Yıl (Mayıs)",
        "cycle_en": "Annual (May)",
        "location_city": "Paris",
        "location_country_tr": "Fransa",
        "location_country_en": "France",
        "flag": "🇫🇷",
        "summary_tr": "Su sektörünün CEO'larını, kamu-özel ortaklığı (PPP) liderlerini ve kalkınma bankalarını buluşturan dünyanın 1 numaralı su iş ve yatırım zirvesi. Küresel Su Ödülleri gala töreniyle taçlandırılır.",
        "summary_en": "The premier business conference for the international water industry, bringing together utility CEOs, private developers, sovereign wealth funds, and multilateral banks investing in major water assets.",
        "topics_tr": ["Su Finansmanı & PPP", "Tuzdan Arındırma", "Endüstriyel Su Geri Kazanımı", "Küresel Su Ödülleri"],
        "topics_en": ["Water Project Finance", "Desalination PPP", "Industrial Reuse", "Global Water Awards"],
        "url": "https://www.watermeetsmoney.com/",
        "lat": 48.8566,
        "lng": 2.3522
    },
    {
        "id": "ramsar-cop15",
        "channel": "water",
        "category": "treaty_policy",
        "acronym": "RAMSAR COP15",
        "title_tr": "Ramsar Sulak Alanlar Sözleşmesi 15. Taraflar Konferansı",
        "title_en": "Ramsar Convention on Wetlands 15th COP",
        "organizer_tr": "Ramsar Konvansiyonu Sekretaryası & Zimbabve Çevre Bakanlığı",
        "organizer_en": "Ramsar Convention Secretariat & Republic of Zimbabwe",
        "date_display_tr": "23 - 31 Temmuz 2026",
        "date_display_en": "July 23 - 31, 2026",
        "cycle_tr": "3 Yılda Bir",
        "cycle_en": "Triennial",
        "location_city": "Victoria Falls",
        "location_country_tr": "Zimbabve",
        "location_country_en": "Zimbabwe",
        "flag": "🇿🇼",
        "summary_tr": "Dünyanın en kritik sulak alanları, gölleri ve nehir deltalarının uluslararası korunma statüsünün belirlendiği, 172 taraf devletin katıldığı bağlayıcı uluslararası çevre sözleşmesi zirvesi.",
        "summary_en": "Intergovernmental treaty gathering where 172 contracting parties adopt binding resolutions on safeguarding transboundary wetlands, lake ecosystems, and coastal river deltas.",
        "topics_tr": ["Sulak Alanların Korunması", "Göl & Nehir Restorasyonu", "Ramsar Alanları", "Biyoçeşitlilik"],
        "topics_en": ["Wetlands Protection", "Lake & River Restoration", "Ramsar Sites", "Biodiversity"],
        "url": "https://www.ramsar.org/",
        "lat": -17.9244,
        "lng": 25.8567
    },
    {
        "id": "iwra-wwc-2026",
        "channel": "water",
        "category": "treaty_policy",
        "acronym": "IWRA WWC",
        "title_tr": "IWRA XVIII. Dünya Su Kongresi",
        "title_en": "IWRA XVIII World Water Congress",
        "organizer_tr": "Uluslararası Su Kaynakları Birliği (IWRA)",
        "organizer_en": "International Water Resources Association (IWRA)",
        "date_display_tr": "21 - 25 Eylül 2026",
        "date_display_en": "September 21 - 25, 2026",
        "cycle_tr": "3 Yılda Bir",
        "cycle_en": "Triennial",
        "location_city": "Pekin",
        "location_country_tr": "Çin",
        "location_country_en": "China",
        "flag": "🇨🇳",
        "summary_tr": "Sınır aşan nehir havzası yönetimi, uluslararası su hukuku, baraj mühendisliği ve su güvenliği stratejilerinde 50 yıllık akademik köke sahip en köklü su kongresi.",
        "summary_en": "Half a century of leadership in transboundary river basin planning, international water law, and major hydrological engineering systems.",
        "topics_tr": ["Sınır Aşan Havza Hukuku", "Entegre Havza Yönetimi", "Baraj & Hidroloji", "Su Hakkı"],
        "topics_en": ["Transboundary Water Law", "Integrated Basin Planning", "Dam Engineering", "Water Rights"],
        "url": "https://www.iwra.org/",
        "lat": 39.9042,
        "lng": 116.4074
    }
]

# 2. TARIM GÜNDEMİ (Agriculture Agenda) Uluslararası Toplantıları
AGRICULTURE_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "gffa-berlin-2026",
        "channel": "agriculture",
        "category": "un_gov",
        "acronym": "GFFA 2026",
        "title_tr": "Küresel Gıda ve Tarım Forumu (GFFA Berlin 2026)",
        "title_en": "Global Forum for Food and Agriculture (GFFA 2026)",
        "organizer_tr": "Almanya Federal Gıda ve Tarım Bakanlığı (BMEL)",
        "organizer_en": "German Federal Ministry of Food and Agriculture (BMEL)",
        "date_display_tr": "21 - 24 Ocak 2026",
        "date_display_en": "January 21 - 24, 2026",
        "cycle_tr": "Her Yıl (Ocak)",
        "cycle_en": "Annual (January)",
        "location_city": "Berlin",
        "location_country_tr": "Almanya",
        "location_country_en": "Germany",
        "flag": "🇩🇪",
        "summary_tr": "Dünyanın en büyük uluslararası tarım politikaları zirvesi. 70'i aşkın ülkenin tarım bakanının bizzat katıldığı 'Berlin Tarım Bakanları Konferansı'nın nihai ortak bildirgesini ilan eder.",
        "summary_en": "The world's foremost conference on vital agricultural policies, culminating in the Berlin Agriculture Ministers' Conference with over 70 ministers issuing a definitive joint communique.",
        "topics_tr": ["Bakanlar Zirvesi", "Küresel Gıda Güvenliği", "Tarımsal Ticaret", "Sürdürülebilir Üretim"],
        "topics_en": ["Ministers Summit", "Global Food Security", "Agricultural Trade", "Sustainable Cropping"],
        "url": "https://www.gffa-berlin.de/en/",
        "lat": 52.5200,
        "lng": 13.4050
    },
    {
        "id": "fao-wff-2026",
        "channel": "agriculture",
        "category": "un_gov",
        "acronym": "FAO WFF",
        "title_tr": "FAO Dünya Gıda Forumu 2026",
        "title_en": "FAO World Food Forum 2026",
        "organizer_tr": "Birleşmiş Milletler Gıda ve Tarım Örgütü (FAO)",
        "organizer_en": "Food and Agriculture Organization of the United Nations (FAO)",
        "date_display_tr": "12 - 16 Ekim 2026",
        "date_display_en": "October 12 - 16, 2026",
        "cycle_tr": "Her Yıl (Ekim)",
        "cycle_en": "Annual (October)",
        "location_city": "Roma",
        "location_country_tr": "İtalya",
        "location_country_en": "Italy",
        "flag": "🇮🇹",
        "summary_tr": "BM FAO'nun amiral gemisi yıllık zirvesi. Küresel Gıda Günü kutlamaları, Tarımsal Bilim ve İnovasyon Forumu ile El Ele (Hand-in-Hand) Tarımsal Yatırım Zirvesi eşzamanlı gerçekleştirilir.",
        "summary_en": "FAO's flagship annual gathering incorporating the Science and Innovation Forum and the Hand-in-Hand Investment Forum to drive systemic transformation across global agrifood value chains.",
        "topics_tr": ["Tarımsal İnovasyon", "Hand-in-Hand Yatırımları", "Tohum & Genetik", "Açlıkla Mücadele"],
        "topics_en": ["Agrifood Innovation", "Hand-in-Hand Investment", "Seed Systems", "Zero Hunger SDG 2"],
        "url": "https://www.world-food-forum.org/",
        "lat": 41.9028,
        "lng": 12.4964
    },
    {
        "id": "agritechnica-2026",
        "channel": "agriculture",
        "category": "industry_expo",
        "acronym": "AGRITECHNICA",
        "title_tr": "AGRITECHNICA - Dünyanın Lider Tarım Makineleri & İnovasyon Zirvesi",
        "title_en": "AGRITECHNICA - The World's Leading Agricultural Machinery Summit",
        "organizer_tr": "DLG (Alman Tarım Derneği)",
        "organizer_en": "DLG (German Agricultural Society)",
        "date_display_tr": "15 - 21 Kasım 2026",
        "date_display_en": "November 15 - 21, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Hannover",
        "location_country_tr": "Almanya",
        "location_country_en": "Germany",
        "flag": "🇩🇪",
        "summary_tr": "2.800 uluslararası üretici ve 450.000 ziyaretçiyle dünyanın en büyük tarım teknolojisi vitrini. Otonom traktörler, yapay zeka destekli hassas ilaçlama ve robotik hasat makinelerinin lansman merkezi.",
        "summary_en": "The global hub for smart farming machinery, gathering 2,800 exhibitors and 450,000 visitors to showcase autonomous tractors, robotics, and variable-rate precision agriculture.",
        "topics_tr": ["Otonom Traktörler", "Hassas Tarım", "Akıllı Sulama", "Robotik Hasat"],
        "topics_en": ["Autonomous Tractors", "Precision Farming", "Smart Irrigation", "Robotic Harvesting"],
        "url": "https://www.agritechnica.com/en/",
        "lat": 52.3759,
        "lng": 9.7320
    },
    {
        "id": "world-agritech-2026",
        "channel": "agriculture",
        "category": "science_academic",
        "acronym": "AGRI-TECH",
        "title_tr": "Dünya Agri-Tech İnovasyon Zirvesi (San Francisco & Londra)",
        "title_en": "World Agri-Tech Innovation Summit 2026",
        "organizer_tr": "Rethink Events",
        "organizer_en": "Rethink Events",
        "date_display_tr": "17 - 18 Mart 2026 (ABD) / 22 - 23 Eylül 2026 (Birleşik Krallık)",
        "date_display_en": "March 17 - 18, 2026 (USA) / September 22 - 23, 2026 (UK)",
        "cycle_tr": "Yılda İki Kez (Bahar/Güz)",
        "cycle_en": "Bi-annual (Spring/Autumn)",
        "location_city": "San Francisco / Londra",
        "location_country_tr": "ABD / Birleşik Krallık",
        "location_country_en": "USA / UK",
        "flag": "🇺🇸",
        "summary_tr": "Tarımsal biyoteknoloji, sentetik biyoloji, mikrobiyal gübreler, kuraklığa dayanıklı genetik tohumlar ve tarım yapay zekasına yön veren küresel risk sermayedarları ve girişimciler zirvesi.",
        "summary_en": "The pre-eminent meeting place for agribusiness corporates, biotech innovators, and venture capital investing in next-generation crop biology, soil carbon, and agricultural AI.",
        "topics_tr": ["Biyogübreler", "Gen Düzenleme (CRISPR)", "Tarım Yapay Zekası", "Girişim Sermayesi"],
        "topics_en": ["Biofertilizers", "Gene Editing CRISPR", "Agricultural AI", "AgTech Venture Capital"],
        "url": "https://worldagritech.com/",
        "lat": 37.7749,
        "lng": -122.4194
    },
    {
        "id": "isf-seed-2026",
        "channel": "agriculture",
        "category": "treaty_policy",
        "acronym": "ISF SEED",
        "title_tr": "ISF Dünya Tohum Kongresi 2026",
        "title_en": "ISF World Seed Congress 2026",
        "organizer_tr": "Uluslararası Tohumculuk Federasyonu (ISF)",
        "organizer_en": "International Seed Federation (ISF)",
        "date_display_tr": "1 - 3 Haziran 2026",
        "date_display_en": "June 1 - 3, 2026",
        "cycle_tr": "Her Yıl (Haziran)",
        "cycle_en": "Annual (June)",
        "location_city": "Vancouver",
        "location_country_tr": "Kanada",
        "location_country_en": "Canada",
        "flag": "🇨🇦",
        "summary_tr": "Dünya tohum ticaretinin kurallarını, fikri mülkiyet haklarını, genetik tohum bankalarını ve fitosaniter kuralları belirleyen en üst düzey küresel tohumculuk zirvesi.",
        "summary_en": "The premier gathering for the global seed industry, setting international seed movement standards, genetic diversity safeguards, and intellectual property protections.",
        "topics_tr": ["Sertifikalı Tohumluk", "Genetik Islah", "Fitosaniter Standartlar", "Tohum Ticareti"],
        "topics_en": ["Certified Seed", "Genetic Breeding", "Phytosanitary Standards", "Seed Trade"],
        "url": "https://worldseed.org/",
        "lat": 49.2827,
        "lng": -123.1207
    },
    {
        "id": "esa-agronomy-2026",
        "channel": "agriculture",
        "category": "science_academic",
        "acronym": "ESA 2026",
        "title_tr": "Avrupa Agronomi Kongresi (ESA Congress 2026)",
        "title_en": "European Society for Agronomy Congress 2026",
        "organizer_tr": "Avrupa Agronomi Birliği (ESA)",
        "organizer_en": "European Society for Agronomy (ESA)",
        "date_display_tr": "31 Ağustos - 4 Eylül 2026",
        "date_display_en": "August 31 - September 4, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Valensiya",
        "location_country_tr": "İspanya",
        "location_country_en": "Spain",
        "flag": "🇪🇸",
        "summary_tr": "Akdeniz ve Avrupa havzasında toprak verimliliği, ekim nöbeti, kuraklığa dirençli tahıl ve baklagil fizyolojisi ile agro-ekolojik tarım uygulamalarının tartışıldığı en büyük bilimsel kongre.",
        "summary_en": "Europe's leading scientific congress exploring resilient cropping systems, Mediterranean drought agronomy, soil nutrient cycles, and agro-ecological transition pathways.",
        "topics_tr": ["Toprak Sağlığı", "Ekim Nöbeti", "Kuraklık Agronomisi", "Agro-Ekoloji"],
        "topics_en": ["Soil Health", "Crop Rotation", "Drought Agronomy", "Agro-Ecology"],
        "url": "https://www.european-agronomy.org/",
        "lat": 39.4699,
        "lng": -0.3763
    }
]

# 3. HAYVANCILIK GÜNDEMİ (Livestock Agenda) Uluslararası Toplantıları
LIVESTOCK_EVENTS: List[Dict[str, Any]] = [
    {
        "id": "eurotier-2026",
        "channel": "livestock",
        "category": "industry_expo",
        "acronym": "EuroTier",
        "title_tr": "EuroTier - Dünyanın Lider Hayvancılık & Sürü Yönetimi Zirvesi",
        "title_en": "EuroTier - The World's Leading Livestock Management Summit",
        "organizer_tr": "DLG (Alman Tarım Derneği)",
        "organizer_en": "DLG (German Agricultural Society)",
        "date_display_tr": "17 - 20 Kasım 2026",
        "date_display_en": "November 17 - 20, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Hannover",
        "location_country_tr": "Almanya",
        "location_country_en": "Germany",
        "flag": "🇩🇪",
        "summary_tr": "Dünyanın en kapsamlı hayvancılık fuarı ve inovasyon kongresi. Büyükbaş süt ve besi sığırcılığı, koyunculuk, kanatlı sektörü, otomatik sağım robotları ve akıllı ahır iklimlendirmesinin küresel lideri.",
        "summary_en": "The world's leading exhibition and technical conference for cattle, pig, poultry, and sheep farming. Showcases robotic milking, feeding automation, and animal welfare solutions.",
        "topics_tr": ["Sürü Yönetimi", "Otomatik Sağım Robotları", "Yem Teknolojileri", "Hayvan Refahı"],
        "topics_en": ["Herd Management", "Robotic Milking", "Feed Technologies", "Animal Welfare"],
        "url": "https://www.eurotier.com/en/",
        "lat": 52.3759,
        "lng": 9.7320
    },
    {
        "id": "idf-wds-2026",
        "channel": "livestock",
        "category": "un_gov",
        "acronym": "IDF WDS",
        "title_tr": "IDF Dünya Süt Zirvesi 2026 (World Dairy Summit)",
        "title_en": "IDF World Dairy Summit 2026",
        "organizer_tr": "Uluslararası Sütçülük Federasyonu (International Dairy Federation - IDF)",
        "organizer_en": "International Dairy Federation (IDF)",
        "date_display_tr": "19 - 22 Ekim 2026",
        "date_display_en": "October 19 - 22, 2026",
        "cycle_tr": "Her Yıl (Ekim)",
        "cycle_en": "Annual (October)",
        "location_city": "Kopenhag",
        "location_country_tr": "Danimarka",
        "location_country_en": "Denmark",
        "flag": "🇩🇰",
        "summary_tr": "Küresel süt sanayiinin en prestijli buluşması. Çiğ süt taban fiyatlama dinamikleri, mandıra hijyen standartları, soğuk zincir güvenliği ve süt sığırcılığında metan emisyonu azaltma hedefleri burada belirlenir.",
        "summary_en": "The global benchmark event for dairy farmers, processors, and regulators, addressing raw milk economics, pasteurization food safety, cold chain analytics, and net-zero dairy pathways.",
        "topics_tr": ["Çiğ Süt Politikaları", "Mandıra İnovasyonu", "Metan Emisyonu", "Soğuk Zincir"],
        "topics_en": ["Raw Milk Economics", "Dairy Processing", "Methane Mitigation", "Cold Chain Logistics"],
        "url": "https://fil-idf.org/",
        "lat": 55.6761,
        "lng": 12.5683
    },
    {
        "id": "world-buiatrics-2026",
        "channel": "livestock",
        "category": "science_academic",
        "acronym": "WBC 2026",
        "title_tr": "Dünya Buiatrics Kongresi 2026 (Sığır Sağlığı & Hekimliği)",
        "title_en": "World Buiatrics Congress 2026 (Cattle Health & Veterinary)",
        "organizer_tr": "Dünya Buiatrics Derneği (World Association for Buiatrics - WAB)",
        "organizer_en": "World Association for Buiatrics (WAB)",
        "date_display_tr": "24 - 28 Ağustos 2026",
        "date_display_en": "August 24 - 28, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Cancún",
        "location_country_tr": "Meksika",
        "location_country_en": "Mexico",
        "flag": "🇲🇽",
        "summary_tr": "Sığır hekimliği ve sürü sağlığında dünyanın 1 numaralı veterinerlik kongresi. Mastitis kontrolü, buzağı mortalitesinin önlenmesi, şap ve tüberküloz aşıları ile reprodüksiyon biyoteknolojisi oturumları yer alır.",
        "summary_en": "The pre-eminent world congress for cattle veterinary medicine, focusing on mastitis prevention, calf health, emerging viral zoonoses, and modern reproductive biotechnology in beef and dairy herds.",
        "topics_tr": ["Sığır Hekimliği", "Mastitis Yönetimi", "Aşı & Biyogüvenlik", "Sürü Reprodüksiyonu"],
        "topics_en": ["Cattle Veterinary Care", "Mastitis Prevention", "Vaccination Biosecurity", "Reproductive Tech"],
        "url": "https://buiatrics.com/",
        "lat": 21.1619,
        "lng": -86.8515
    },
    {
        "id": "eaap-2026",
        "channel": "livestock",
        "category": "science_academic",
        "acronym": "EAAP 2026",
        "title_tr": "EAAP Yıllık Hayvan Bilimleri Konferansı 2026",
        "title_en": "EAAP Annual Animal Science Meeting 2026",
        "organizer_tr": "Avrupa Hayvan Bilimleri Federasyonu (EAAP)",
        "organizer_en": "European Federation of Animal Science (EAAP)",
        "date_display_tr": "30 Ağustos - 3 Eylül 2026",
        "date_display_en": "August 30 - September 3, 2026",
        "cycle_tr": "Her Yıl (Yaz)",
        "cycle_en": "Annual (Summer)",
        "location_city": "Floransa",
        "location_country_tr": "İtalya",
        "location_country_en": "Italy",
        "flag": "🇮🇹",
        "summary_tr": "Avrupa'nın en büyük zootekni ve hayvansal genetik kongresi. Genomik boğa seçimi, kaba yem silaj fermantasyonu, hassas sürü sensörleri ve küçükbaş mera yönetimi üzerine 1.000'den fazla bilimsel bildiri sunulur.",
        "summary_en": "Europe's most influential scientific conference on animal genetics, ruminant nutrition, precision livestock farming sensors, and sustainable pastoral grazing models.",
        "topics_tr": ["Zootekni & Genomik", "Rasyon & Silaj", "Hassas Sensörler", "Mera Yönetimi"],
        "topics_en": ["Animal Genetics", "Ration & Silage", "Precision Sensors", "Pastoral Systems"],
        "url": "https://eaap.org/",
        "lat": 43.7696,
        "lng": 11.2558
    },
    {
        "id": "gasl-fao-2026",
        "channel": "livestock",
        "category": "treaty_policy",
        "acronym": "GASL 2026",
        "title_tr": "GASL - Sürdürülebilir Hayvancılık Küresel Gündemi 2026",
        "title_en": "Global Agenda for Sustainable Livestock 2026",
        "organizer_tr": "BM Gıda ve Tarım Örgütü (FAO) & GASL Ortaklığı",
        "organizer_en": "Food and Agriculture Organization of the United Nations (FAO) & GASL",
        "date_display_tr": "8 - 11 Eylül 2026",
        "date_display_en": "September 8 - 11, 2026",
        "cycle_tr": "Her Yıl (Eylül)",
        "cycle_en": "Annual (September)",
        "location_city": "Cenevre",
        "location_country_tr": "İsviçre",
        "location_country_en": "Switzerland",
        "flag": "🇨🇭",
        "summary_tr": "Hayvancılıkta 'Tek Sağlık' (One Health) yaklaşımı, antibiyotik direncinin sınırlandırılması, meraların çölleşmeye karşı korunması ve düşük karbonlu kırmızı et üretim ilkelerinin hükümetler düzeyinde ele alındığı BM platformu.",
        "summary_en": "Multi-stakeholder partnership addressing global livestock sustainability under the One Health framework, antimicrobial resistance containment, and pastoral grassland regeneration.",
        "topics_tr": ["Tek Sağlık (One Health)", "Antibiyotik Direnci", "Düşük Karbonlu Üretim", "FAO Küresel Gündemi"],
        "topics_en": ["One Health", "Antimicrobial Resistance", "Low-Carbon Livestock", "FAO Global Agenda"],
        "url": "https://www.livestockdialogue.org/",
        "lat": 46.2044,
        "lng": 6.1432
    },
    {
        "id": "viv-europe-2026",
        "channel": "livestock",
        "category": "industry_expo",
        "acronym": "VIV Europe",
        "title_tr": "VIV Europe 2026 - Hayvansal Protein ve Yem Sanayii Zirvesi",
        "title_en": "VIV Europe 2026 - Feed to Food Animal Protein Summit",
        "organizer_tr": "VNU Exhibitions Europe",
        "organizer_en": "VNU Exhibitions Europe",
        "date_display_tr": "12 - 14 Mayıs 2026",
        "date_display_en": "May 12 - 14, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Utrecht",
        "location_country_tr": "Hollanda",
        "location_country_en": "Netherlands",
        "flag": "🇳🇱",
        "summary_tr": "Yemden gıdaya (Feed to Food) hayvansal protein tedarik zincirinin dünya merkezi. Karma yem fabrikaları, kanatlı kümes ekipmanları, yumurta işleme ve kuluçkahane biyogüvenliği teknolojileri sergilenir.",
        "summary_en": "Global business network covering the entire animal protein value chain from compound feed mills and premixes to industrial poultry housing and hatchery biosecurity.",
        "topics_tr": ["Karma Yem Sanayii", "Kanatlı & Yumurta", "Kuluçkahane Teknolojisi", "Biyogüvenlik"],
        "topics_en": ["Compound Feed Mills", "Poultry & Eggs", "Hatchery Systems", "Biosecurity"],
        "url": "https://www.viv.net/",
        "lat": 52.0907,
        "lng": 5.1214
    },
    {
        "id": "wmc-meat-2026",
        "channel": "livestock",
        "category": "treaty_policy",
        "acronym": "WMC 2026",
        "title_tr": "Dünya Et Kongresi 2026 (World Meat Congress)",
        "title_en": "World Meat Congress 2026",
        "organizer_tr": "Uluslararası Et Sekreteryası (International Meat Secretariat - IMS)",
        "organizer_en": "International Meat Secretariat (IMS)",
        "date_display_tr": "4 - 6 Kasım 2026",
        "date_display_en": "November 4 - 6, 2026",
        "cycle_tr": "2 Yılda Bir",
        "cycle_en": "Biennial",
        "location_city": "Montevideo",
        "location_country_tr": "Uruguay",
        "location_country_en": "Uruguay",
        "flag": "🇺🇾",
        "summary_tr": "Kırmızı et tedarik zinciri, karkas derecelendirme standartları, uluslararası canlı hayvan ve et ihracatı regülasyonları ile meraya dayalı sürdürülebilir besicilik politikalarının küresel zirvesi.",
        "summary_en": "The global forum for meat industry leaders, ranchers, and trade negotiators reviewing carcass quality standards, border biosecurity, and grass-fed sustainable beef markets.",
        "topics_tr": ["Kırmızı Et Ticareti", "Karkas Standartları", "Mera Besiciliği", "Uluslararası Regülasyon"],
        "topics_en": ["Red Meat Trade", "Carcass Grading", "Grass-Fed Beef", "Trade Regulations"],
        "url": "https://meat-ims.org/",
        "lat": -34.9011,
        "lng": -56.1645
    }
]

def get_channel_events(channel: str) -> List[Dict[str, Any]]:
    """Kanal adına göre uluslararası etkinlik listesini döndürür."""
    if channel == "agriculture":
        return AGRICULTURE_EVENTS
    elif channel == "livestock":
        return LIVESTOCK_EVENTS
    else:
        return WATER_EVENTS

def build_google_cal_url(event: Dict[str, Any]) -> str:
    """Google Takvim linki üretir."""
    title = f"{event.get('acronym', '')}: {event.get('title_tr', '')}"
    details = f"{event.get('summary_tr', '')}\n\nOrganizatör: {event.get('organizer_tr', '')}\nResmi Web: {event.get('url', '')}"
    location = f"{event.get('location_city', '')}, {event.get('location_country_tr', '')}"
    params = {
        "action": "TEMPLATE",
        "text": title,
        "details": details,
        "location": location
    }
    return "https://calendar.google.com/calendar/render?" + urllib.parse.urlencode(params)

def render_events_hub_html(channel_key: str, events: List[Dict[str, Any]]) -> str:
    """Uluslararası Zirveler ve Toplantılar ana bileşen HTML'ini üretir."""
    meta = CHANNEL_EVENTS_METADATA.get(channel_key, CHANNEL_EVENTS_METADATA["water"])
    
    # 1. Sub-tabs bar
    subtabs_html = f"""
    <div class="events-subtabs-bar" id="eventsSubTabsBar">
        <button type="button" class="event-subtab-btn active" data-event-cat="all" onclick="filterEventCategory('all')">
            <span>🌟 Tüm Zirveler</span>
            <span class="subtab-count">{len(events)}</span>
        </button>
        <button type="button" class="event-subtab-btn" data-event-cat="un_gov" onclick="filterEventCategory('un_gov')">
            <span>🏛️ BM &amp; Hükümetlerarası</span>
        </button>
        <button type="button" class="event-subtab-btn" data-event-cat="science_academic" onclick="filterEventCategory('science_academic')">
            <span>🔬 Bilimsel Kongreler</span>
        </button>
        <button type="button" class="event-subtab-btn" data-event-cat="industry_expo" onclick="filterEventCategory('industry_expo')">
            <span>🚜 Sektörel &amp; Fuarlar</span>
        </button>
        <button type="button" class="event-subtab-btn" data-event-cat="treaty_policy" onclick="filterEventCategory('treaty_policy')">
            <span>📜 Sözleşmeler &amp; Politikalar</span>
        </button>
    </div>
    """

    # 2. Event Cards
    cards_html = []
    for ev in events:
        cal_url = build_google_cal_url(ev)
        cat_meta = EVENT_CATEGORIES.get(ev["category"], {"tr": "Küresel Zirve", "en": "Global Summit"})
        
        topics_html = " ".join([f'<span class="event-topic-pill">#{html.escape(t)}</span>' for t in ev.get("topics_tr", [])])
        
        card = f"""
        <article class="event-card" data-event-card-id="{ev['id']}" data-event-cat="{ev['category']}">
            <div class="event-card-header">
                <div class="event-header-left">
                    <span class="event-acronym-badge">{ev['flag']} {html.escape(ev['acronym'])}</span>
                    <span class="event-cat-badge">{cat_meta['tr']}</span>
                </div>
                <span class="event-cycle-badge">{html.escape(ev['cycle_tr'])}</span>
            </div>

            <h3 class="event-card-title">{html.escape(ev['title_tr'])}</h3>
            <div class="event-card-org">🏛️ <span class="event-org-text">{html.escape(ev['organizer_tr'])}</span></div>

            <div class="event-meta-grid">
                <div class="event-meta-item">
                    <span class="meta-icon">🗓️</span>
                    <div class="meta-content">
                        <span class="meta-label">Tarih</span>
                        <span class="meta-val event-date-text">{html.escape(ev['date_display_tr'])}</span>
                    </div>
                </div>
                <div class="event-meta-item">
                    <span class="meta-icon">📍</span>
                    <div class="meta-content">
                        <span class="meta-label">Konum</span>
                        <span class="meta-val event-loc-text">{html.escape(ev['location_city'])}, {html.escape(ev['location_country_tr'])}</span>
                    </div>
                </div>
            </div>

            <p class="event-card-desc">{html.escape(ev['summary_tr'])}</p>

            <div class="event-topics-tags">
                {topics_html}
            </div>

            <div class="event-card-actions">
                <a href="{html.escape(ev['url'])}" target="_blank" rel="noopener noreferrer" class="btn-event-link" title="Resmi İnternet Sitesini Ziyaret Et">
                    <span>Resmi Web Sitesi</span>
                    <span class="ext-arrow">&nearr;</span>
                </a>
                <button type="button" class="btn-event-map" onclick="focusEventOnMap({ev['lat']}, {ev['lng']}, '{html.escape(ev['acronym'])}')">
                    <span>📍 Haritada Gör</span>
                </button>
                <a href="{html.escape(cal_url)}" target="_blank" rel="noopener noreferrer" class="btn-event-cal" title="Google Takvim'e Ekle">
                    <span>📅 Takvim</span>
                </a>
            </div>
        </article>
        """
        cards_html.append(card)

    cards_joined = "\n".join(cards_html)

    return f"""
    <div class="events-hub-col" id="eventsHubCol" style="display: none;">
        
        <!-- Events Section Headline -->
        <div class="events-hub-header">
            <div class="events-hub-badge" id="eventsSectionBadge">{meta['badge_tr']}</div>
            <h2 class="events-hub-title" id="eventsSectionTitle">{meta['title_tr']}</h2>
            <p class="events-hub-desc" id="eventsSectionDesc">{meta['desc_tr']}</p>
        </div>

        <!-- Sub-tabs bar (Sekmeler) -->
        {subtabs_html}

        <!-- Cards Grid -->
        <div class="events-cards-grid" id="eventsCardsGrid">
            {cards_joined}
        </div>

        <!-- Empty State for sub-tab filtering -->
        <div id="eventsEmptyState" class="empty-results-box" style="display: none; margin-top: 25px;">
            <div class="empty-icon">🌐</div>
            <h3>Bu alt kategoride henüz toplantı kaydı bulunmuyor</h3>
            <p>Farklı bir kategori seçebilir veya tüm zirveleri görüntüleyebilirsiniz.</p>
            <button type="button" class="btn-reset-filter" onclick="filterEventCategory('all')">Tüm Zirveleri Göster</button>
        </div>

    </div>
    """

def render_sidebar_events_widget(channel_key: str, events: List[Dict[str, Any]]) -> str:
    """Sağ kenar çubuğu (Sidebar) için öne çıkan zirveler widget'ı."""
    top_events = events[:4]
    
    items_html = []
    for ev in top_events:
        items_html.append(f"""
        <div class="sidebar-event-item" onclick="switchPortalMainView('events'); filterEventCategory('all');">
            <div class="sidebar-event-date">{ev['flag']} {html.escape(ev['date_display_tr'].split('(')[0].strip())}</div>
            <div class="sidebar-event-title">{html.escape(ev['acronym'])} &bull; {html.escape(ev['title_tr'])}</div>
            <div class="sidebar-event-loc">📍 {html.escape(ev['location_city'])}, {html.escape(ev['location_country_tr'])}</div>
        </div>
        """)
        
    joined_items = "\n".join(items_html)
    
    return f"""
    <div class="sidebar-card sidebar-events-card">
        <div class="sidebar-events-header">
            <h4 class="sidebar-title" style="margin-bottom:0;">🌐 Uluslararası Zirveler</h4>
            <span class="sidebar-events-count">{len(events)} Zirve</span>
        </div>
        <p style="font-size: 11px; color: var(--ink-muted); margin: 6px 0 12px 0;">
            Politikaları, uluslararası anlaşmaları ve küresel fonları belirleyen kritik toplantılar.
        </p>
        <div class="sidebar-events-list">
            {joined_items}
        </div>
        <button type="button" class="btn-all-events-hub" onclick="switchPortalMainView('events')">
            Tüm Zirveleri &amp; Detayları İncele &rarr;
        </button>
    </div>
    """
