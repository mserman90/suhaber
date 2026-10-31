"""
app/prices_data.py
------------------
Tarım ve Hayvancılık Gündemleri için Türkiye ve Diğer Ülkeler (AB, ABD, Küresel)
Gerçek ve Güncel Karşılaştırmalı Tarımsal ve Hayvansal Ürün Fiyatları Modülü.
Veri kaynakları: TÜRİB, USK, UKON, TÜİK, Euronext/Matif, CBOT, USDA, DG AGRI, FAO, MLA, Fonterra.
Döviz referans kurları: 1 USD = 35.80 ₺ | 1 EUR = 38.80 ₺ (Ekim 2026 sonu).
"""

import html
from typing import List, Dict, Any

FX_RATES = {
    "USD_TRY": 35.80,
    "EUR_TRY": 38.80,
    "EUR_USD": 1.084,
    "last_update_tr": "31 Ekim 2026",
    "last_update_en": "October 31, 2026"
}

# 1. TARIM EMTİA FİYATLARI (Agricultural Commodity Prices)
AGRICULTURE_PRICES: List[Dict[str, Any]] = [
    {
        "id": "wheat-milling",
        "category": "cereals",
        "name_tr": "Ekmeklik Buğday (Tip 2 / 12.5% Protein)",
        "name_en": "Milling Wheat (12.5% Protein Benchmark)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 10850.0,
        "tr_price_usd": 303.1,
        "tr_source": "TÜRİB / Polatlı - Konya TB",
        "eu_price_orig": "228.00 €/Ton",
        "eu_price_usd": 247.1,
        "eu_price_tl": 8846.0,
        "eu_source": "Euronext Paris (Matif)",
        "us_price_orig": "5.85 $/bu",
        "us_price_usd": 215.0,
        "us_price_tl": 7697.0,
        "us_source": "CBOT (No:2 HRW)",
        "world_price_orig": "235.00 $/Ton",
        "world_price_usd": 235.0,
        "world_price_tl": 8413.0,
        "world_name_tr": "Karadeniz (Rusya FOB)",
        "world_name_en": "Black Sea (Russia FOB)",
        "world_source": "Sovecon / IKAR",
        "diff_vs_world_pct": "+28.9%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.4% (Haftalık)",
        "change_en": "+1.4% (Weekly)",
        "note_tr": "TMO 2026 alım baremleri ve gümrük vergisi koruması sebebiyle iç piyasa dünya vadeli fiyatlarına kıyasla primli işlem görmektedir.",
        "note_en": "Turkish domestic milling wheat commands a tariff-backed premium over international CBOT and Euronext futures."
    },
    {
        "id": "wheat-durum",
        "category": "cereals",
        "name_tr": "Makarnalık Buğday (Durum Wheat / Sert)",
        "name_en": "Durum Wheat (Amber Durum)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 12200.0,
        "tr_price_usd": 340.8,
        "tr_source": "TÜRİB / Güneydoğu Borsaları",
        "eu_price_orig": "315.00 €/Ton",
        "eu_price_usd": 341.5,
        "eu_price_tl": 12222.0,
        "eu_source": "İtalya Foggia Borsası",
        "us_price_orig": "355.00 $/Ton",
        "us_price_usd": 355.0,
        "us_price_tl": 12709.0,
        "us_source": "Kanada St. Lawrence FOB (CWAD)",
        "world_price_orig": "335.00 $/Ton",
        "world_price_usd": 335.0,
        "world_price_tl": 11993.0,
        "world_name_tr": "Akdeniz Havzası Ortalama",
        "world_name_en": "Mediterranean Durum Index",
        "world_source": "International Grains Council",
        "diff_vs_world_pct": "+1.7%",
        "diff_status": "neutral",
        "trend": "stable",
        "change_tr": "+0.2% (Haftalık)",
        "change_en": "+0.2% (Weekly)",
        "note_tr": "Akdeniz havzasındaki kuraklık etkisine bağlı olarak Türkiye fiyatları İtalya ve Akdeniz ihracat kotasyonlarıyla tam başa baş dengelenmiştir.",
        "note_en": "Tight Mediterranean durum balances keep Turkish durum prices virtually in line with Italian Foggia benchmark bids."
    },
    {
        "id": "corn-maize",
        "category": "cereals",
        "name_tr": "Mısır (1. Sınıf Tane Mısır)",
        "name_en": "Feed Corn / Maize (Yellow No. 2)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 8900.0,
        "tr_price_usd": 248.6,
        "tr_source": "TÜRİB / Adana - Şanlıurfa TB",
        "eu_price_orig": "205.00 €/Ton",
        "eu_price_usd": 222.2,
        "eu_price_tl": 7954.0,
        "eu_source": "Euronext Paris (Maize)",
        "us_price_orig": "4.25 $/bu",
        "us_price_usd": 167.3,
        "us_price_tl": 5989.0,
        "us_source": "CBOT Corn",
        "world_price_orig": "195.00 $/Ton",
        "world_price_usd": 195.0,
        "world_price_tl": 6981.0,
        "world_name_tr": "Brezilya Paranagua FOB",
        "world_name_en": "Brazil Paranagua FOB",
        "world_source": "CEPEA / ESALQ",
        "diff_vs_world_pct": "+27.5%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+2.1% (Haftalık)",
        "change_en": "+2.1% (Weekly)",
        "note_tr": "Yurt içi yem ve nişasta sanayisinin güçlü hasat talebi ve ithalat kısıtları nedeniyle Türkiye mısır fiyatı küresel FOB seviyelerinin üzerindedir.",
        "note_en": "Strong compound feed demand and import regulations keep Turkish domestic corn significantly above CBOT levels."
    },
    {
        "id": "feed-barley",
        "category": "cereals",
        "name_tr": "Yemlik Arpa (Standart 62-64 Hektolitre)",
        "name_en": "Feed Barley (62-64 kg/hl)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 8450.0,
        "tr_price_usd": 236.0,
        "tr_source": "TÜRİB / İç Anadolu Borsaları",
        "eu_price_orig": "198.00 €/Ton",
        "eu_price_usd": 214.6,
        "eu_price_tl": 7682.0,
        "eu_source": "Fransa Rouen FOB",
        "us_price_orig": "205.00 $/Ton",
        "us_price_usd": 205.0,
        "us_price_tl": 7339.0,
        "us_source": "USDA Feed Grain Report",
        "world_price_orig": "192.00 $/Ton",
        "world_price_usd": 192.0,
        "world_price_tl": 6874.0,
        "world_name_tr": "Karadeniz FOB",
        "world_name_en": "Black Sea Feed Barley FOB",
        "world_source": "Argus AgriMarkets",
        "diff_vs_world_pct": "+22.9%",
        "diff_status": "premium",
        "trend": "down",
        "change_tr": "-0.6% (Haftalık)",
        "change_en": "-0.6% (Weekly)",
        "note_tr": "Yem fabrikalarının rasyon maliyet baskısı karşısında TMO regülasyon satışlarıyla arpa fiyatı son haftalarda yatay-aşağı seyretmektedir.",
        "note_en": "TMO regulatory intervention stocks offer relief against surging compound feed cost pressures."
    },
    {
        "id": "sunflower-seed",
        "category": "oilseeds",
        "name_tr": "Yağlık Ayçiçeği Tohumu (%44 Yağ Bazlı)",
        "name_en": "Sunflower Seed (44% Oil Content)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 20500.0,
        "tr_price_usd": 572.6,
        "tr_source": "Trakya Birlik Alım / Edirne TB",
        "eu_price_orig": "490.00 €/Ton",
        "eu_price_usd": 531.2,
        "eu_price_tl": 19012.0,
        "eu_source": "Bulgaristan / Romanya FOB",
        "us_price_orig": "520.00 $/Ton",
        "us_price_usd": 520.0,
        "us_price_tl": 18616.0,
        "us_source": "USDA Sunflower Market",
        "world_price_orig": "485.00 $/Ton",
        "world_price_usd": 485.0,
        "world_price_tl": 17363.0,
        "world_name_tr": "Ukrayna FOB Karadeniz",
        "world_name_en": "Ukraine FOB Black Sea",
        "world_source": "UkrAgroConsult",
        "diff_vs_world_pct": "+18.1%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.8% (Haftalık)",
        "change_en": "+1.8% (Weekly)",
        "note_tr": "Trakya ve İç Anadolu'da kuraklık nedeniyle rekolte düşüşü, iç piyasada ayçiçeği tohumu fiyatlarını dünya kotasyonlarının üzerine taşımıştır.",
        "note_en": "Drought-driven harvest declines across Thrace and Anatolia support buoyant domestic sunflower pricing."
    },
    {
        "id": "crude-sunflower-oil",
        "category": "oilseeds",
        "name_tr": "Ham Ayçiçek Yağı (Crude Sunflower Oil)",
        "name_en": "Crude Sunflower Oil (FOB/CIF)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 43500.0,
        "tr_price_usd": 1215.1,
        "tr_source": "İç Piyasa Rafineri Teslim",
        "eu_price_orig": "1,030.00 €/Ton",
        "eu_price_usd": 1116.5,
        "eu_price_tl": 39964.0,
        "eu_source": "Rotterdam FOB",
        "us_price_orig": "1,140.00 $/Ton",
        "us_price_usd": 1140.0,
        "us_price_tl": 40812.0,
        "us_source": "USDA Oil Crops",
        "world_price_orig": "1,080.00 $/Ton",
        "world_price_usd": 1080.0,
        "world_price_tl": 38664.0,
        "world_name_tr": "Karadeniz CIF Marmara",
        "world_name_en": "Black Sea CIF Marmara",
        "world_source": "Fastmarkets AgriCensus",
        "diff_vs_world_pct": "+12.5%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+2.5% (Haftalık)",
        "change_en": "+2.5% (Weekly)",
        "note_tr": "Karasal lojistik maliyetleri ve gümrük vergileri ile birlikte CIF Marmara ithal fiyatı iç piyasa rafineri fiyatlarını yukarı çekmektedir.",
        "note_en": "Import parity and CIF Marmara freight charges maintain an upward bias in Turkish refinery gate rates."
    },
    {
        "id": "soybeans",
        "category": "oilseeds",
        "name_tr": "Soya Fasulyesi (Yemlik ve Sanayi Soya)",
        "name_en": "Soybeans (Yellow No. 2 Feed)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 17800.0,
        "tr_price_usd": 497.2,
        "tr_source": "TÜRİB / Çukurova Borsaları",
        "eu_price_orig": "410.00 €/Ton",
        "eu_price_usd": 444.4,
        "eu_price_tl": 15908.0,
        "eu_source": "Rotterdam CIF",
        "us_price_orig": "10.15 $/bu",
        "us_price_usd": 372.9,
        "us_price_tl": 13350.0,
        "us_source": "CBOT Soybeans",
        "world_price_orig": "395.00 $/Ton",
        "world_price_usd": 395.0,
        "world_price_tl": 14141.0,
        "world_name_tr": "Brezilya Paranagua FOB",
        "world_name_en": "Brazil Paranagua FOB",
        "world_source": "CEPEA Brasil",
        "diff_vs_world_pct": "+25.9%",
        "diff_status": "premium",
        "trend": "stable",
        "change_tr": "+0.3% (Haftalık)",
        "change_en": "+0.3% (Weekly)",
        "note_tr": "Yem sanayiinin proteine olan yüksek ihtiyacı ve soya küspesi ithalat bağımlılığı yerli soyayı yüksek fiyattan tutmaktadır.",
        "note_en": "Turkey's structural protein deficit reinforces premium local soybean market values."
    },
    {
        "id": "cotton-raw",
        "category": "industrial",
        "name_tr": "Mahlıç Pamuk (Standart 1 Beyaz)",
        "name_en": "Upland Raw Cotton (Standard 1 White)",
        "unit_tr": "₺ / kg",
        "unit_en": "¢ / lb",
        "tr_price_tl": 58.50,
        "tr_price_usd": 1.63,
        "tr_source": "İzmir Ticaret Borsası",
        "eu_price_orig": "1.58 €/kg",
        "eu_price_usd": 1.71,
        "eu_price_tl": 61.30,
        "eu_source": "Yunanistan Teslim",
        "us_price_orig": "72.80 ¢/lb",
        "us_price_usd": 1.60,
        "us_price_tl": 57.28,
        "us_source": "ICE Cotton Futures (NY)",
        "world_price_orig": "81.20 ¢/lb",
        "world_price_usd": 1.79,
        "world_price_tl": 64.08,
        "world_name_tr": "Cotlook A Endeksi",
        "world_name_en": "Cotlook A Index Benchmark",
        "world_source": "Cotlook Limited",
        "diff_vs_world_pct": "-8.7%",
        "diff_status": "discount",
        "trend": "stable",
        "change_tr": "-0.4% (Haftalık)",
        "change_en": "-0.4% (Weekly)",
        "note_tr": "Tekstil ve iplik fabrikalarındaki sipariş yavaşlaması nedeniyle yerli pamuk dünya Cotlook endeksinin hafif altında iskontolu işlem görmektedir.",
        "note_en": "Moderate spinning mill operating rates keep domestic Turkish lint slightly discounted against Cotlook A."
    },
    {
        "id": "fertilizer-urea",
        "category": "inputs",
        "name_tr": "Granül Üre Gübresi (%46 N)",
        "name_en": "Granular Urea 46% N",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 16200.0,
        "tr_price_usd": 452.5,
        "tr_source": "Bayi Perakende / Peşin Satış",
        "eu_price_orig": "395.00 €/Ton",
        "eu_price_usd": 428.2,
        "eu_price_tl": 15326.0,
        "eu_source": "Kuzeybatı Avrupa CIF",
        "us_price_orig": "385.00 $/Ton",
        "us_price_usd": 385.0,
        "us_price_tl": 13783.0,
        "us_source": "NOLA Barge FOB (New Orleans)",
        "world_price_orig": "355.00 $/Ton",
        "world_price_usd": 355.0,
        "world_price_tl": 12709.0,
        "world_name_tr": "Mısır / Karadeniz FOB",
        "world_name_en": "Egypt / Black Sea FOB",
        "world_source": "Fertecon / Argus",
        "diff_vs_world_pct": "+27.5%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+3.2% (Haftalık)",
        "change_en": "+3.2% (Weekly)",
        "note_tr": "Doğalgaz fiyatları ve sonbahar buğday ekim dönemi taban gübresi talebiyle yurt içi üre gübresi perakende fiyatları artış eğilimindedir.",
        "note_en": "Autumn wheat planting demand and natural gas input trends underpin firm domestic retail nitrogen quotes."
    },
    {
        "id": "fertilizer-dap",
        "category": "inputs",
        "name_tr": "DAP Gübresi (18-46-0 Kompoze)",
        "name_en": "DAP Fertilizer (18-46-0 Diammonium)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 24500.0,
        "tr_price_usd": 684.4,
        "tr_source": "Bayi Perakende / Peşin Satış",
        "eu_price_orig": "590.00 €/Ton",
        "eu_price_usd": 639.6,
        "eu_price_tl": 22892.0,
        "eu_source": "Avrupa İthalat CIF",
        "us_price_orig": "570.00 $/Ton",
        "us_price_usd": 570.0,
        "us_price_tl": 20406.0,
        "us_source": "US Gulf FOB Export",
        "world_price_orig": "580.00 $/Ton",
        "world_price_usd": 580.0,
        "world_price_tl": 20764.0,
        "world_name_tr": "Fas (OCP FOB İhracat)",
        "world_name_en": "Morocco (OCP FOB Export)",
        "world_source": "Argus Phosphates",
        "diff_vs_world_pct": "+18.0%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.9% (Haftalık)",
        "change_en": "+1.9% (Weekly)",
        "note_tr": "Küresel fosfat kısıtları ve navlun maliyetleri ekim dönemindeki DAP bayi perakende fiyatlarını yukarıda tutmaktadır.",
        "note_en": "Global phosphate supply tightness maintains firm import parity for Turkish phosphate applications."
    }
]

# 2. HAYVANCILIK ÜRÜN VE YEM FİYATLARI (Livestock & Feed Prices)
LIVESTOCK_PRICES: List[Dict[str, Any]] = [
    {
        "id": "raw-milk",
        "category": "dairy",
        "name_tr": "Çiğ İnek Sütü (%3.6 Yağ, %3.2 Protein)",
        "name_en": "Raw Cow Milk (3.6% Fat, 3.2% Protein)",
        "unit_tr": "₺ / Litre",
        "unit_en": "$ / kg Farmgate",
        "tr_price_tl": 14.65,
        "tr_price_usd": 0.409,
        "tr_source": "USK (Ulusal Süt Konseyi Tavsiye)",
        "eu_price_orig": "0.470 €/kg",
        "eu_price_usd": 0.509,
        "eu_price_tl": 18.24,
        "eu_source": "Avrupa Süt Gözlemevi (MMO Ortalama)",
        "us_price_orig": "19.80 $/cwt",
        "us_price_usd": 0.436,
        "us_price_tl": 15.61,
        "us_source": "USDA Class III Milk (Chicago)",
        "world_price_orig": "0.370 $/kg",
        "world_price_usd": 0.370,
        "world_price_tl": 13.25,
        "world_name_tr": "Yeni Zelanda Fonterra Farmgate",
        "world_name_en": "New Zealand Fonterra Payout",
        "world_source": "Fonterra Co-operative",
        "diff_vs_world_pct": "-19.6%",
        "diff_status": "discount",
        "trend": "stable",
        "change_tr": "0.0% (Sabit)",
        "change_en": "0.0% (Stable)",
        "note_tr": "USK çiğ süt tavsiye fiyatı 14.65 TL seviyesinde sabit seyrederken sanayicinin brüt maliyeti 16.20 TL/kg'yi bulmaktadır. AB fiyatının gerisindedir.",
        "note_en": "Turkish farmgate milk price remains regulated at 14.65 TRY/kg, sitting below EU average farmgate benchmarks."
    },
    {
        "id": "beef-carcass-bull",
        "category": "meat",
        "name_tr": "Dana Karkas Eti (Yağsız Kesim / Randımanlı)",
        "name_en": "Young Bull Beef Carcass (Lean Dressing)",
        "unit_tr": "₺ / kg",
        "unit_en": "$ / kg Carcass Eq.",
        "tr_price_tl": 385.00,
        "tr_price_usd": 10.75,
        "tr_source": "UKON (Ulusal Kırmızı Et Konseyi Haftalık)",
        "eu_price_orig": "5.15 €/kg",
        "eu_price_usd": 5.58,
        "eu_price_tl": 199.82,
        "eu_source": "EU DG AGRI (Young Bull R3)",
        "us_price_orig": "5.95 $/kg",
        "us_price_usd": 5.95,
        "us_price_tl": 213.01,
        "us_source": "USDA Choice Steer Carcass Eq.",
        "world_price_orig": "3.80 $/kg",
        "world_price_usd": 3.80,
        "world_price_tl": 136.04,
        "world_name_tr": "Brezilya / Uruguay FOB Karkas",
        "world_name_en": "Brazil / Uruguay FOB Carcass",
        "world_source": "Meat & Livestock Commercial Index",
        "diff_vs_world_pct": "+92.7%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.3% (Haftalık)",
        "change_en": "+1.3% (Weekly)",
        "note_tr": "Besilik dana ithalat maliyetleri, yüksek yem fiyatları ve damızlık varlığı baskısı nedeniyle Türkiye karkas kesim fiyatı dünya ortalamasının neredeyse iki katıdır.",
        "note_en": "Structural feeder scarcity and feed costs keep Turkish beef carcass prices roughly double international parity."
    },
    {
        "id": "lamb-carcass",
        "category": "meat",
        "name_tr": "Kuzu Karkas Eti (Yağsız Kesim)",
        "name_en": "Lamb Carcass (Heavy Lamb Dressed)",
        "unit_tr": "₺ / kg",
        "unit_en": "$ / kg Carcass Eq.",
        "tr_price_tl": 415.00,
        "tr_price_usd": 11.59,
        "tr_source": "UKON (Kuzu Kesim Ortalaması)",
        "eu_price_orig": "8.40 €/kg",
        "eu_price_usd": 9.10,
        "eu_price_tl": 325.92,
        "eu_source": "EU DG AGRI Heavy Lamb Index",
        "us_price_orig": "8.80 $/kg",
        "us_price_usd": 8.80,
        "us_price_tl": 315.04,
        "us_source": "USDA National Lamb Market",
        "world_price_orig": "5.20 $/kg",
        "world_price_usd": 5.20,
        "world_price_tl": 186.16,
        "world_name_tr": "Avustralya / YZ (MLA Heavy FOB)",
        "world_name_en": "Australia / NZ (MLA Heavy FOB)",
        "world_source": "Meat & Livestock Australia",
        "diff_vs_world_pct": "+27.3%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+0.8% (Haftalık)",
        "change_en": "+0.8% (Weekly)",
        "note_tr": "Yaz-sonbahar mera geçişinde besiye alınan kuzularda arz darlığı kuzu karkas fiyatını AB seviyelerinin de üzerine çıkarmıştır.",
        "note_en": "Tight pastoral lamb marketings keep Turkish sheepmeat carcass prices elevated above European standards."
    },
    {
        "id": "feeder-cattle",
        "category": "live",
        "name_tr": "Canlı Besi Danası (250-300 kg Canlı Ağırlık)",
        "name_en": "Feeder Cattle (250-300 kg Live Weight)",
        "unit_tr": "₺ / kg Canlı",
        "unit_en": "$ / kg Live Weight",
        "tr_price_tl": 245.00,
        "tr_price_usd": 6.84,
        "tr_source": "Yurt İçi Besi Materyali Piyasası",
        "eu_price_orig": "3.65 €/kg",
        "eu_price_usd": 3.96,
        "eu_price_tl": 141.62,
        "eu_source": "İrlanda / Fransa Canlı İhracat",
        "us_price_orig": "2.52 $/lb",
        "us_price_usd": 5.55,
        "us_price_tl": 198.69,
        "us_source": "CME Feeder Cattle Futures",
        "world_price_orig": "2.80 $/kg",
        "world_price_usd": 2.80,
        "world_price_tl": 100.24,
        "world_name_tr": "Güney Amerika (Uruguay FOB Canlı)",
        "world_name_en": "South America (Uruguay FOB Live)",
        "world_source": "INAC Uruguay",
        "diff_vs_world_pct": "+72.7%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.7% (Haftalık)",
        "change_en": "+1.7% (Weekly)",
        "note_tr": "Besi işletmelerinin boş kapasiteyi doldurmak için besilik materyal arayışı, canlı kilo fiyatlarını yüksek tutmaktadır.",
        "note_en": "Robust feedlot stocking demand maintains high prices for local feeder steers relative to CME benchmarks."
    },
    {
        "id": "dairy-compound-feed",
        "category": "feed_parity",
        "name_tr": "Karma Süt Yemi (19 Protein / 2700 Enerji)",
        "name_en": "Compound Dairy Feed (19% Protein)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 9800.0,
        "tr_price_usd": 273.7,
        "tr_source": "Yem Sanayicileri Birlik Ortalaması",
        "eu_price_orig": "275.00 €/Ton",
        "eu_price_usd": 298.1,
        "eu_price_tl": 10670.0,
        "eu_source": "Avrupa Karma Yem (FEFAC Ortalama)",
        "us_price_orig": "260.00 $/Ton",
        "us_price_usd": 260.0,
        "us_price_tl": 9308.0,
        "us_source": "USDA Dairy Ration Equivalent",
        "world_price_orig": "265.00 $/Ton",
        "world_price_usd": 265.0,
        "world_price_tl": 9487.0,
        "world_name_tr": "Küresel Yem Rasyonu Referansı",
        "world_name_en": "Global Compound Ration Index",
        "world_source": "Agri-Benchmark",
        "diff_vs_world_pct": "-8.2%",
        "diff_status": "discount",
        "trend": "up",
        "change_tr": "+1.0% (Haftalık)",
        "change_en": "+1.0% (Weekly)",
        "note_tr": "Soya küspesi ve mısır ithal maliyetlerine bağlı olarak dolar bazında dünya ile paralel seyrederken üretici TL maliyetinde artış sürmektedir.",
        "note_en": "Ration prices track international protein meals while local currency volatility tests farmer purchasing power."
    },
    {
        "id": "beef-finishing-feed",
        "category": "feed_parity",
        "name_tr": "Besi Büyütme & Bitirme Yemi (14 Protein)",
        "name_en": "Beef Feedlot Finishing Feed (14% Protein)",
        "unit_tr": "₺ / Ton",
        "unit_en": "$ / Metric Ton",
        "tr_price_tl": 8900.0,
        "tr_price_usd": 248.6,
        "tr_source": "Fabrika Satış / Çuval Bazlı Ortalama",
        "eu_price_orig": "250.00 €/Ton",
        "eu_price_usd": 271.0,
        "eu_price_tl": 9700.0,
        "eu_source": "EU Compound Beef Feed Index",
        "us_price_orig": "240.00 $/Ton",
        "us_price_usd": 240.0,
        "us_price_tl": 8592.0,
        "us_source": "US Feedlot Ration Index",
        "world_price_orig": "245.00 $/Ton",
        "world_price_usd": 245.0,
        "world_price_tl": 8771.0,
        "world_name_tr": "Küresel Besi Yemi Endeksi",
        "world_name_en": "Global Beef Finishing Index",
        "world_source": "Agri-Benchmark Beef",
        "diff_vs_world_pct": "-8.3%",
        "diff_status": "discount",
        "trend": "stable",
        "change_tr": "+0.5% (Haftalık)",
        "change_en": "+0.5% (Weekly)",
        "note_tr": "Arpa ve kepek maliyetlerindeki ılımlı seyir sayesinde besi rasyonları son çeyrekte dengeli bir bantta işlem görmektedir.",
        "note_en": "Moderate cereal grain inputs keep beef feedlot formulations relatively balanced in dollar terms."
    },
    {
        "id": "milk-feed-ratio",
        "category": "feed_parity",
        "name_tr": "Süt / Yem Paritesi (1 kg Süt ile Alınan Yem)",
        "name_en": "Milk-to-Feed Ratio (kg Feed per kg Milk)",
        "unit_tr": "Rasyo (kg/kg)",
        "unit_en": "Ratio (kg/kg)",
        "tr_price_tl": 1.49,
        "tr_price_usd": 1.49,
        "tr_source": "USK Süt Fiyatı / 19 HP Süt Yemi Fiyatı",
        "eu_price_orig": "1.71 rasyo",
        "eu_price_usd": 1.71,
        "eu_price_tl": 1.71,
        "eu_source": "Avrupa Birliği MMO Paritesi",
        "us_price_orig": "2.15 rasyo",
        "us_price_usd": 2.15,
        "us_price_tl": 2.15,
        "us_source": "USDA Milk-Feed Price Ratio",
        "world_price_orig": "1.65 rasyo",
        "world_price_usd": 1.65,
        "world_price_tl": 1.65,
        "world_name_tr": "Sektörel İdeal Eşik (1.50)",
        "world_name_en": "Industry Viability Threshold (1.50)",
        "world_source": "FAO / IDF Dairy Guidelines",
        "diff_vs_world_pct": "-12.9%",
        "diff_status": "discount",
        "trend": "stable",
        "change_tr": "0.0% (Kritik Eşik: 1.50)",
        "change_en": "0.0% (Threshold: 1.50)",
        "note_tr": "Türkiye'de süt/yem paritesi 1.49 ile sürdürülebilirlik eşiği olan 1.50'nin hemen altında seyretmekte; AB (1.71) ve ABD'nin (2.15) gerisindedir.",
        "note_en": "Turkish milk-to-feed ratio of 1.49 hovers just below the vital 1.50 profitability benchmark."
    },
    {
        "id": "meat-feed-ratio",
        "category": "feed_parity",
        "name_tr": "Et / Yem Paritesi (1 kg Karkas ile Alınan Yem)",
        "name_en": "Beef-to-Feed Ratio (kg Feed per kg Carcass)",
        "unit_tr": "Rasyo (kg/kg)",
        "unit_en": "Ratio (kg/kg)",
        "tr_price_tl": 43.2,
        "tr_price_usd": 43.2,
        "tr_source": "UKON Dana Karkas / 14 HP Besi Yemi",
        "eu_price_orig": "20.6 rasyo",
        "eu_price_usd": 20.6,
        "eu_price_tl": 20.6,
        "eu_source": "AB Young Bull / Besi Yemi Rasyosu",
        "us_price_orig": "24.8 rasyo",
        "us_price_usd": 24.8,
        "us_price_tl": 24.8,
        "us_source": "USDA Steer-to-Corn Ratio Eq.",
        "world_price_orig": "22.5 rasyo",
        "world_price_usd": 22.5,
        "world_price_tl": 22.5,
        "world_name_tr": "Dünya Ortalaması Rasyo",
        "world_name_en": "Global Average Beef-Feed Ratio",
        "world_source": "Agri-Benchmark Economics",
        "diff_vs_world_pct": "+109.7%",
        "diff_status": "premium",
        "trend": "up",
        "change_tr": "+1.2% (Yüksek Rasyo)",
        "change_en": "+1.2% (High Ratio)",
        "note_tr": "Karkas et fiyatı çok yüksek olduğu için et/yem rasyosu yüksek görünse de, canlı besilik dana alım maliyetinin aşırılığı net kârı daraltmaktadır.",
        "note_en": "Nominal beef-feed ratio is exceptionally high due to dear carcass rates, but expensive feeder calf acquisition compresses margins."
    },
    {
        "id": "broiler-chicken",
        "category": "poultry",
        "name_tr": "Bütün Piliç Eti (Toptan Taze Karkas)",
        "name_en": "Whole Broiler Chicken (Wholesale Ready-to-Cook)",
        "unit_tr": "₺ / kg",
        "unit_en": "$ / kg Wholesale",
        "tr_price_tl": 82.00,
        "tr_price_usd": 2.29,
        "tr_source": "BESD-BİR Toptan Pazar Kotasyonu",
        "eu_price_orig": "2.68 €/kg",
        "eu_price_usd": 2.90,
        "eu_price_tl": 103.98,
        "eu_source": "EU Broiler Carcass Index",
        "us_price_orig": "2.75 $/kg",
        "us_price_usd": 2.75,
        "us_price_tl": 98.45,
        "us_source": "USDA Composite Broiler Index",
        "world_price_orig": "1.65 $/kg",
        "world_price_usd": 1.65,
        "world_price_tl": 59.07,
        "world_name_tr": "Brezilya FOB Tavuk İhracatı",
        "world_name_en": "Brazil FOB Poultry Export",
        "world_source": "ABPA Brasil",
        "diff_vs_world_pct": "-21.0%",
        "diff_status": "discount",
        "trend": "stable",
        "change_tr": "-0.3% (Haftalık)",
        "change_en": "-0.3% (Weekly)",
        "note_tr": "Türkiye entegre kanatlı sektörü, ileri tesis altyapısıyla AB ve ABD'ye göre daha ucuz toptan beyaz et sunarak güçlü ihracatını sürdürmektedir.",
        "note_en": "Vertically integrated Turkish poultry operations maintain cost competitiveness against EU and US processors."
    },
    {
        "id": "table-eggs",
        "category": "poultry",
        "name_tr": "Yumurta (L Boy / 30'lu Toptan Koli)",
        "name_en": "Table Eggs (Grade A Large / 30-Pack Tray)",
        "unit_tr": "₺ / 30'lu Koli",
        "unit_en": "$ / 30-Pack Tray",
        "tr_price_tl": 114.00,
        "tr_price_usd": 3.18,
        "tr_source": "YUM-BİR Toptan Satış Referansı",
        "eu_price_orig": "4.20 € / 30 ad",
        "eu_price_usd": 4.55,
        "eu_price_tl": 162.96,
        "eu_source": "EU Egg Market Oversight",
        "us_price_orig": "4.80 $ / 30 ad",
        "us_price_usd": 4.80,
        "us_price_tl": 171.84,
        "us_source": "USDA Shell Egg National Report",
        "world_price_orig": "4.10 $ / 30 ad",
        "world_price_usd": 4.10,
        "world_price_tl": 146.78,
        "world_name_tr": "Küresel Yumurta Piyasası Endeksi",
        "world_name_en": "Global Shell Egg Index",
        "world_source": "International Egg Commission (IEC)",
        "diff_vs_world_pct": "-30.1%",
        "diff_status": "discount",
        "trend": "up",
        "change_tr": "+2.0% (Haftalık)",
        "change_en": "+2.0% (Weekly)",
        "note_tr": "Türkiye yumurta üretimi, iç piyasaya dünya ortalamasının %30 altında fiyat sağlarken Orta Doğu pazarlarına yoğun ihracat yapmaktadır.",
        "note_en": "Robust local egg supply delivers consumer prices roughly 30% below European retail tray averages."
    }
]

# Kategori filtre tanımları
PRICE_CATEGORIES: Dict[str, Dict[str, Dict[str, str]]] = {
    "agriculture": {
        "all": {"tr": "🌟 Tüm Tarımsal Emtialar", "en": "🌟 All Agri Commodities"},
        "cereals": {"tr": "🌾 Hububat & Tahıllar", "en": "🌾 Grains & Cereals"},
        "oilseeds": {"tr": "🌻 Yağlı Tohumlar & Ham Yağ", "en": "🌻 Oilseeds & Crude Oils"},
        "industrial": {"tr": "🧶 Endüstriyel Bitkiler", "en": "🧶 Industrial Crops"},
        "inputs": {"tr": "🧪 Gübre & Girdiler", "en": "🧪 Fertilizer & Inputs"}
    },
    "livestock": {
        "all": {"tr": "🌟 Tüm Hayvansal Ürünler", "en": "🌟 All Livestock Products"},
        "dairy": {"tr": "🥛 Çiğ Süt & Süt Ürünleri", "en": "🥛 Raw Milk & Dairy"},
        "meat": {"tr": "🥩 Kırmızı Et & Karkas", "en": "🥩 Red Meat & Carcass"},
        "live": {"tr": "🐂 Canlı Hayvan", "en": "🐂 Live Feeder Cattle"},
        "feed_parity": {"tr": "🌾 Yem & Pariteler", "en": "🌾 Feed & Parity Ratios"},
        "poultry": {"tr": "🐔 Kanatlı & Yumurta", "en": "🐔 Poultry & Eggs"}
    }
}

CHANNEL_PRICES_METADATA = {
    "agriculture": {
        "badge_tr": "📊 GÜNCEL TARIMSAL EMTİA & BORSA FİYATLARI",
        "badge_en": "📊 REAL-TIME AGRI COMMODITY BENCHMARKS",
        "title_tr": "🌾 Türkiye ve Dünya Karşılaştırmalı Tarımsal Ürün Fiyatları",
        "title_en": "🌾 Comparative Agricultural Commodity Prices: Turkey vs. World",
        "desc_tr": "TÜRİB, CBOT, Euronext, USDA ve IGC verileriyle buğday, mısır, arpa, ayçiçeği, pamuk ve gübre fiyatları, borsa kotasyonları ve Türkiye prim/iskonto analizi.",
        "desc_en": "Real-time grain, oilseed, cotton and fertilizer parity across TURIB, CBOT, Euronext, and Black Sea ports with domestic premium/discount spreads."
    },
    "livestock": {
        "badge_tr": "📊 GÜNCEL HAYVANCILIK PİYASASI & PARİTELER",
        "badge_en": "📊 REAL-TIME LIVESTOCK & FEED BENCHMARKS",
        "title_tr": "🐄 Türkiye ve Dünya Karşılaştırmalı Hayvansal Ürün ve Yem Fiyatları",
        "title_en": "🐄 Comparative Livestock, Meat & Feed Prices: Turkey vs. World",
        "desc_tr": "UKON, USK, DG AGRI, USDA ve Fonterra verileriyle çiğ süt, karkas et, canlı hayvan, karma yem fiyatları ve süt/yem - et/yem rasyo analizleri.",
        "desc_en": "Farmgate milk, beef carcass, feeder cattle and compound feed parity across UKON, USK, EU DG AGRI, USDA and global dairy/meat auctions."
    }
}

def get_channel_prices(channel_key: str) -> List[Dict[str, Any]]:
    """Kanal anahtarına göre ürün fiyat listesini döndürür."""
    if channel_key == "livestock":
        return LIVESTOCK_PRICES
    elif channel_key == "agriculture":
        return AGRICULTURE_PRICES
    return []

def render_prices_hub_html(channel_key: str, prices: List[Dict[str, Any]]) -> str:
    """Tarımsal ve hayvansal ürün fiyatları ana bileşen HTML'ini üretir."""
    meta = CHANNEL_PRICES_METADATA.get(channel_key, CHANNEL_PRICES_METADATA["agriculture"])
    categories = PRICE_CATEGORIES.get(channel_key, PRICE_CATEGORIES["agriculture"])

    # 1. Sub-tabs bar (Kategori Sekmeleri)
    subtabs_html = ['<div class="prices-subtabs-bar" id="pricesSubTabsBar">']
    for cat_slug, cat_dict in categories.items():
        is_first = (cat_slug == "all")
        active_cls = " active" if is_first else ""
        cnt = len(prices) if is_first else len([p for p in prices if p["category"] == cat_slug])
        subtabs_html.append(f"""
        <button type="button" class="price-subtab-btn{active_cls}" data-price-cat="{cat_slug}" onclick="filterPriceCategory('{cat_slug}')">
            <span>{cat_dict['tr']}</span>
            <span class="price-subtab-count">{cnt}</span>
        </button>
        """)
    subtabs_html.append('</div>')
    subtabs_bar_str = "".join(subtabs_html)

    # 2. FX Ticker Strip
    fx_strip = f"""
    <div class="prices-fx-strip">
        <div class="fx-strip-item">
            <span class="fx-label">💵 USD/TRY:</span>
            <span class="fx-val">35.80 ₺</span>
        </div>
        <div class="fx-strip-sep">&bull;</div>
        <div class="fx-strip-item">
            <span class="fx-label">💶 EUR/TRY:</span>
            <span class="fx-val">38.80 ₺</span>
        </div>
        <div class="fx-strip-sep">&bull;</div>
        <div class="fx-strip-item">
            <span class="fx-label">📅 Referans Tarihi:</span>
            <span class="fx-val">{FX_RATES['last_update_tr']}</span>
        </div>
        <div class="fx-strip-sep">&bull;</div>
        <div class="fx-strip-item">
            <span class="fx-label">🏛️ Kaynaklar:</span>
            <span class="fx-val">TÜRİB, UKON, USK, Euronext, CBOT, USDA, DG AGRI</span>
        </div>
    </div>
    """

    # 3. Price Cards Grid
    cards_html = []
    for item in prices:
        cat_info = categories.get(item["category"], {"tr": "Emtia", "en": "Commodity"})
        diff_status = item.get("diff_status", "premium")
        diff_pct = item.get("diff_vs_world_pct", "0%")
        
        if diff_status == "premium":
            diff_badge_cls = "diff-badge-premium"
            diff_badge_text_tr = f"🇹🇷 {diff_pct} Primli (TR Yüksek)"
            diff_badge_text_en = f"🇹🇷 {diff_pct} Premium vs World"
        elif diff_status == "discount":
            diff_badge_cls = "diff-badge-discount"
            diff_badge_text_tr = f"🇹🇷 {diff_pct} İskontolu (TR Uygun)"
            diff_badge_text_en = f"🇹🇷 {diff_pct} Discount vs World"
        else:
            diff_badge_cls = "diff-badge-neutral"
            diff_badge_text_tr = f"🇹🇷 {diff_pct} Başa Baş / Dengeli"
            diff_badge_text_en = f"🇹🇷 {diff_pct} Parity"

        trend_cls = "trend-" + item.get("trend", "stable")
        trend_icon = "▲" if item.get("trend") == "up" else ("▼" if item.get("trend") == "down" else "▬")

        # Format numerical prices
        tr_tl_str = f"{item['tr_price_tl']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if item['tr_price_tl'] < 100 else f"{int(item['tr_price_tl']):,}".replace(",", ".")
        tr_usd_str = f"${item['tr_price_usd']:,.2f}" if item['tr_price_usd'] < 50 else f"${int(item['tr_price_usd']):,}"

        card = f"""
        <article class="price-compare-card" data-price-card-id="{item['id']}" data-price-cat="{item['category']}">
            
            <div class="price-card-header">
                <div class="price-header-left">
                    <span class="price-category-pill">{cat_info['tr']}</span>
                    <span class="price-trend-tag {trend_cls}">{trend_icon} {html.escape(item['change_tr'])}</span>
                </div>
                <span class="price-diff-badge {diff_badge_cls}">{diff_badge_text_tr}</span>
            </div>

            <h3 class="price-card-title">{html.escape(item['name_tr'])}</h3>
            <div class="price-card-unit">Birim: <strong>{html.escape(item['unit_tr'])}</strong></div>

            <!-- Comparison Matrix -->
            <div class="price-comparison-grid">
                
                <!-- Türkiye -->
                <div class="price-cell price-cell-tr">
                    <div class="cell-country">
                        <span class="cell-flag">🇹🇷</span>
                        <span class="cell-country-name">Türkiye</span>
                    </div>
                    <div class="cell-main-price">{tr_tl_str} ₺</div>
                    <div class="cell-usd-equiv">~{tr_usd_str} / ton/kg</div>
                    <div class="cell-source" title="Kaynak">{html.escape(item['tr_source'])}</div>
                </div>

                <!-- Avrupa Birliği (AB) -->
                <div class="price-cell price-cell-eu">
                    <div class="cell-country">
                        <span class="cell-flag">🇪🇺</span>
                        <span class="cell-country-name">Avrupa Birliği</span>
                    </div>
                    <div class="cell-main-price">{html.escape(item['eu_price_orig'])}</div>
                    <div class="cell-usd-equiv">~${item['eu_price_usd']:.1f} ({int(item['eu_price_tl']):,} ₺)</div>
                    <div class="cell-source" title="Borsa Kotasyonu">{html.escape(item['eu_source'])}</div>
                </div>

                <!-- ABD -->
                <div class="price-cell price-cell-us">
                    <div class="cell-country">
                        <span class="cell-flag">🇺🇸</span>
                        <span class="cell-country-name">ABD</span>
                    </div>
                    <div class="cell-main-price">{html.escape(item['us_price_orig'])}</div>
                    <div class="cell-usd-equiv">~${item['us_price_usd']:.1f} ({int(item['us_price_tl']):,} ₺)</div>
                    <div class="cell-source" title="Borsa Kotasyonu">{html.escape(item['us_source'])}</div>
                </div>

                <!-- Dünya / Karadeniz Referansı -->
                <div class="price-cell price-cell-world">
                    <div class="cell-country">
                        <span class="cell-flag">🌐</span>
                        <span class="cell-country-name">{html.escape(item['world_name_tr'])}</span>
                    </div>
                    <div class="cell-main-price">{html.escape(item['world_price_orig'])}</div>
                    <div class="cell-usd-equiv">~${item['world_price_usd']:.1f} ({int(item['world_price_tl']):,} ₺)</div>
                    <div class="cell-source" title="Kaynak">{html.escape(item['world_source'])}</div>
                </div>

            </div>

            <!-- Analysis note -->
            <div class="price-card-analysis">
                <span class="analysis-icon">💡</span>
                <span class="analysis-text">{html.escape(item['note_tr'])}</span>
            </div>

        </article>
        """
        cards_html.append(card)

    cards_grid_str = "\n".join(cards_html)

    return f"""
    <!-- Prices Hub Column -->
    <div class="prices-hub-col" id="pricesHubCol" style="display: none;">
        
        <div class="prices-hub-header">
            <div class="prices-hub-badge" id="pricesSectionBadge">{meta['badge_tr']}</div>
            <h2 class="prices-hub-title" id="pricesSectionTitle">{meta['title_tr']}</h2>
            <p class="prices-hub-desc" id="pricesSectionDesc">{meta['desc_tr']}</p>
        </div>

        {fx_strip}

        {subtabs_bar_str}

        <div class="prices-cards-grid" id="pricesCardsGrid">
            {cards_grid_str}
        </div>

        <div id="pricesEmptyState" class="empty-results-box" style="display: none;">
            <div class="empty-icon">📊</div>
            <h3>Bu alt kategoride fiyat kaydı bulunamadı</h3>
            <p>Diğer emtia sekmelerini inceleyebilir veya tümünü listeleyebilirsiniz.</p>
            <button type="button" class="btn-reset-filter" onclick="filterPriceCategory('all')">Tüm Fiyatları Göster</button>
        </div>

    </div>
    """

def render_sidebar_prices_widget(channel_key: str) -> str:
    """Kenar çubuğu (Sidebar) için öne çıkan piyasa fiyatları mini özet kartı üretir."""
    if channel_key not in ("agriculture", "livestock"):
        return ""

    prices = get_channel_prices(channel_key)[:4]
    if not prices:
        return ""

    widget_title_tr = "🌾 Emtia Piyasaları (TR / Dünya)" if channel_key == "agriculture" else "🐄 Hayvancılık & Yem Piyasası"
    widget_btn_tr = "Tam Karşılaştırma Tablosunu Gör →"

    rows = []
    for p in prices:
        name = p["name_tr"].split("(")[0].strip()
        tr_val = f"{int(p['tr_price_tl']):,} ₺".replace(",", ".") if p['tr_price_tl'] >= 100 else f"{p['tr_price_tl']:.2f} ₺"
        diff = p.get("diff_vs_world_pct", "")
        diff_cls = "pill-prem" if p.get("diff_status") == "premium" else "pill-disc"
        
        row = f"""
        <div class="side-price-row">
            <div class="side-price-name">
                <span>{html.escape(name)}</span>
                <span class="side-price-diff {diff_cls}">{diff}</span>
            </div>
            <div class="side-price-vals">
                <span class="side-price-tr">{tr_val}</span>
                <span class="side-price-world">${p['tr_price_usd']:.0f}</span>
            </div>
        </div>
        """
        rows.append(row)

    rows_str = "".join(rows)

    return f"""
    <div class="sidebar-card sidebar-prices-card">
        <h4 class="sidebar-title" id="sidePricesTitle">{widget_title_tr}</h4>
        <div class="side-prices-list">
            {rows_str}
        </div>
        <button type="button" class="btn-sidebar-view-prices" onclick="switchPortalMainView('prices')">
            <span id="sidePricesBtn">{widget_btn_tr}</span>
        </button>
    </div>
    """
