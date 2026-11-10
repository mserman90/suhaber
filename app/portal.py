import html
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.quotes import get_daily_water_quote
from app.legal_data import render_footer_legal_bar_html, render_legal_modal_html
import json
from app.prices_data import (
    get_channel_prices,
    render_prices_hub_html,
    render_sidebar_prices_widget,
    PRICE_CATEGORIES,
    CHANNEL_PRICES_METADATA,
    FX_RATES
)
from app.events_data import (
    get_channel_events,
    render_events_hub_html,
    render_sidebar_events_widget,
    CHANNEL_EVENTS_METADATA,
    EVENT_CATEGORIES
)

def clean_html_tags(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    return " ".join(clean.split())



# ── Su Diplomasisi Bilgi Kartları Widget ─────────────────────────────────────
# Source: github.com/mserman90/SuDiplomasisiBilgiKartlari
_WATER_DIPLOMACY_CARDS = [
    {"soru": "Su Diplomasisi Çerçevesi (WDF) su sorunlarının teşhisinde hangi aracı 'kaldıraç' olarak kullanır?", "cevap": "Çeşitli bakış açılarını, belirsizliği ve değişen talepleri uzlaştırmak için 'müzakere'yi (negotiation) teşhis ve müdahalenin merkez kaldıracı olarak kullanır.", "kategori": "Su Diplomasisi"},
    {"soru": "Büyük Etiyopya Rönesans Barajı (GERD) inşası karşısında Mısır'ın temel argümanı nedir?", "cevap": "Mısır, mansap su payının azalacağını ve 1929/1959 anlaşmalarına dayanan tarihsel su haklarının ihlal edileceğini savunmaktadır.", "kategori": "Havza Yönetimi"},
    {"soru": "Su diplomasisinde 'Karşılıklı Kazanım' (Mutual Gains) yaklaşımı ne anlama gelir?", "cevap": "Sabit pozisyonlar üzerinden yürütülen sıfır toplamlı politikaların aksine, ortak çıkarları merkeze alan ve değişen koşullara uyarlanabilen esnek çözümler üretme stratejisidir.", "kategori": "Su Diplomasisi"},
    {"soru": "1997 BM Su Yolları Sözleşmesi su paylaşımında hangi temel prensibi benimser?", "cevap": "'Hakkaniyete Uygun ve Makul Kullanım' (Equitable and Reasonable Utilization) ve 'Önemli Zarar Vermeme' (No Significant Harm) prensiplerini eşgüdümlü olarak benimser.", "kategori": "Uluslararası Hukuk"},
    {"soru": "Tacikistan-Özbekistan arasındaki Rogun Barajı projesinde su diplomasisi nasıl bir dönüşüm sağladı?", "cevap": "Başlangıçta ciddi jeopolitik çatışma kaynağıyken, proaktif su diplomasisi ve pragmatik fayda paylaşımı (kış-kömür, yaz-sulama suyu takası) ile işbirliği platformuna dönüştü.", "kategori": "Su Diplomasisi"},
    {"soru": "Entegre Su Kaynakları Yönetimi (IWRM) nedir?", "cevap": "Su, arazi ve ilgili kaynakların koordineli gelişimini, ekosistemlerin sürdürülebilirliğinden ödün vermeden ekonomik ve sosyal refahı maksimize edecek şekilde teşvik eden süreçtir.", "kategori": "Havza Yönetimi"},
    {"soru": "Su diplomasisi geleneksel 'yangın söndürme' modelinden nasıl farklılaşır?", "cevap": "Kriz anında devreye giren tepkisel bir araç değil; uzun vadeli güven inşası ve istikrar yaratmak amacıyla sürekli uygulanan proaktif bir politika alanıdır.", "kategori": "Su Diplomasisi"},
    {"soru": "Küresel iklim değişikliği transsınır su anlaşmalarını nasıl tehdit etmektedir?", "cevap": "Bir 'tehdit çarpanı' (threat multiplier) olarak akış rejimlerini öngörülemez şekilde değiştirerek statik ve eski kotalı anlaşmaları işlevsiz hale getirmektedir.", "kategori": "Çevresel Etkiler"},
    {"soru": "Türkiye ile Irak arasındaki ilk kapsamlı su anlaşması hangisidir?", "cevap": "1946 Dostluk ve İyi Komşuluk Antlaşması'na ekli 1 No'lu Protokol; Dicle, Fırat ve kollarının sularının düzenlenmesine ilişkin hükümleri içermektedir.", "kategori": "Uluslararası Hukuk"},
    {"soru": "Su diplomasisinde 'Sıfır Toplamlı' (Zero-Sum) yaklaşım ne anlama gelir?", "cevap": "Havzadaki su miktarının sabit olduğu varsayımıyla, bir kıyıdaş ülkenin kazandığı her bir damla suyun, otomatik olarak diğer kıyıdaşın kaybı olarak algılandığı statik çatışma modelidir.", "kategori": "Su Diplomasisi"},
    {"soru": "Orta Asya'da Aral Gölü krizine yol açan 'Beyaz Altın' politikası nedir?", "cevap": "Sovyetler döneminde Ceyhun ve Seyhun nehirlerini çöl ortasında devasa pamuk tarlalarını sulamak için yönlendiren; Aral Gölü'nü kurumasına neden olan politikadır.", "kategori": "Çevresel Etkiler"},
    {"soru": "Transsınır sularda 'Hidrosolidarite' (Hydrosolidarity) kavramı neyi ifade eder?", "cevap": "Suyun ulusal sınırlar ve milliyetçi çıkarlar ötesinde, tüm havza paydaşlarının ortak çıkarı ve dayanışması çerçevesinde yönetilmesini ifade eder.", "kategori": "Havza Yönetimi"},
]

_AGRICULTURE_FLASHCARDS = [
    {"soru": "Münavebe (Ekim Nöbeti) uygulamasında baklagillerin buğdaygil rotasyonundaki temel faydası nedir?", "cevap": "Baklagiller köklerindeki Rhizobium bakterileriyle havanın serbest azotunu toprağa bağlar; buğday ekiminde kimyasal azotlu gübre ihtiyacını %30-40 azaltır ve toprak yorgunluğunu önler.", "kategori": "Ekim Nöbeti"},
    {"soru": "Damla sulama sistemlerinin geleneksel salma (vahşi) sulamaya kıyasla su ve gübre verimliliği avantajı nedir?", "cevap": "Su tüketiminde %40 ila %60 tasarruf sağlar. Fertigasyon (gübreli sulama) ile bitki kök bölgesine doğrudan besin ileterek gübre israfını ve yabancı ot gelişimini minimize eder.", "kategori": "Sulama & Tasarruf"},
    {"soru": "Toprak pH değerinin 7.5 üzerine çıkması (alkali toprak) bitkilerde hangi besin elementlerinin alımını kilitler?", "cevap": "Başta Demir (Fe), Çinko (Zn), Fosfor (P) ve Mangan (Mn) olmak üzere mikro elementlerin bitki kökleri tarafından alınamaz bileşiklere dönüşmesine (bağlanmasına) yol açar.", "kategori": "Toprak & Besleme"},
    {"soru": "Fosforlu taban gübreleri (örn. DAP veya 20-20-0) neden mutlaka tohum derinliğine yakın uygulanmalıdır?", "cevap": "Fosfor toprakta hareketsiz (mobilitesi son derece düşük) bir elementtir; yüzeye atılırsa köklere ulaşamaz. Tohumun 4-5 cm altına veya yanına gömülmelidir.", "kategori": "Gübreleme"},
    {"soru": "İlkbahar geç donlarında meyve bahçelerinde don pervaneleri ve yağmurlama sistemi nasıl koruma sağlar?", "cevap": "Don pervaneleri üstteki sıcak hava tabakası ile zemindeki soğuk havayı karıştırır; yağmurlama sulama ise su donarken çevreye gizli ısı vererek tomurcuk sıcaklığını 0°C'de tutar.", "kategori": "Don Koruması"},
    {"soru": "Entegre Zararlı Yönetimi (IPM) felsefesi kimyasal ilaçlamadan nasıl ayrılır?", "cevap": "Zararlıyı tamamen yok etmek yerine 'ekonomik zarar eşiği' altında tutmayı amaçlar. Önceliği kültürel önlemler, dayanıklı tohumlar, faydalı böcekler ve biyolojik tuzaklara verir.", "kategori": "Bitki Koruma"},
    {"soru": "Doğrudan anıza ekim (No-Till Farming) tekniğinin kuraklıkla mücadeledeki kritik rolü nedir?", "cevap": "Toprağı devirmeden ekim yaparak toprak nemini buharlaşmaya karşı korur, organik maddeyi yükseltir, erozyonu engeller ve traktör yakıt tüketimini %50'ye varan oranda düşürür.", "kategori": "Akıllı Tarım"},
    {"soru": "Sertifikalı tohum kullanımının verim ve kalite üzerine ölçümlenmiş etkisi nedir?", "cevap": "Çimlenme kabiliyeti (%95+), genetik saflık ve tohum kaynaklı hastalıklardan arındırılmış olması sayesinde verimde ortalama %15 ila %25 arasında artış sağlar.", "kategori": "Tohumculuk"},
    {"soru": "Yaprak analizi (foliar diagnosis) toprak analizine kıyasla hangi ek faydayı sunar?", "cevap": "Toprakta var olan ancak kökler tarafından emilemeyen 'gizli açlık' durumlarını gösterir; gelişme döneminde hızlı yaprak gübresi müdahalesi yapma imkânı tanır.", "kategori": "Toprak & Besleme"},
    {"soru": "Tarımsal kireçleme hangi tip topraklarda uygulanır ve etkisi nedir?", "cevap": "pH değeri 6.0'nın altına inmiş asidik topraklarda uygulanır. Toprak asitliğini nötralize ederek kalsiyum sağlar ve yararlı toprak mikroorganizmalarının aktivitesini artırır.", "kategori": "Toprak & Besleme"},
    {"soru": "Mikoriza mantarlarının bitki kök gelişimine ve su stresine etkisi nasıldır?", "cevap": "Kök yüzey alanını hifleriyle 100 katına kadar genişleterek bitkinin kuraklık stresine dayanıklılığını artırır ve toprakta zor çözünen fosfatları bitkiye taşır.", "kategori": "Biyoteknoloji"},
    {"soru": "Mısır ve pamukta 'tav suyu' ve tepe püskülü çıkarma dönemindeki su açığının riski nedir?", "cevap": "Koçan ve polen oluşumunun gerçekleştiği bu kritik evrede yaşanacak 3-4 günlük su stresi dahi dane bağlamayı aksatarak nihai rekoltede %30'a varan kayba yol açabilir.", "kategori": "Sulama & Tasarruf"}
]

_LIVESTOCK_FLASHCARDS = [
    {"soru": "Yeni doğan buzağılara ilk kolostrum (ağız sütü) verilmesinde kritik zaman penceresi nedir?", "cevap": "Doğumdan sonraki ilk 2 ila 4 saat içinde verilmelidir. 24 saat sonra buzağının bağırsak bariyeri antikor geçişine tamamen kapanır ve pasif bağışıklık fırsatı kaybedilir.", "kategori": "Buzağı Sağlığı"},
    {"soru": "Süt sığırlarında kuru dönem (dry period) süresi neden en az 45-60 gün olmalıdır?", "cevap": "Meme dokusunun rejenere olması, ineğin vücut kondisyon puanını (BCS 3.25-3.5) toparlaması ve bir sonraki laktasyonda pik süt verimine ulaşabilmesi için zorunludur.", "kategori": "Süt Verimi"},
    {"soru": "Besi tosunlarında subakut rumen asidozunu (SARA) önlemek için rasyonda aranması gereken temel kural nedir?", "cevap": "Rasyondaki efektif lif (eNDF) oranının yeterli olması, kaba-kesif yem oranının dengelenmesi ve kaba yemin çok ince kıyılmaması gerekir (geviş getirmeyi teşvik için).", "kategori": "Besi & Rasyon"},
    {"soru": "Mısır silajı yapımında ideal kuru madde (KM) oranı ve fermantasyon kriteri nedir?", "cevap": "Hasat anında ideal kuru madde %32-35 olmalıdır. İyi sıkıştırma ve hava sızdırmaz örtü ile pH 3.8-4.2 aralığına inerek laktik asit fermantasyonu tamamlanmalıdır.", "kategori": "Yem & Silaj"},
    {"soru": "Süt ineklerinde mastitis riskini azaltmada sağım hijyeninin altın kuralı nedir?", "cevap": "Sağım öncesi daldırma ve kurulama, sağım sonrası ise meme ucu kanalının 30 dakika açık kalması nedeniyle antiseptik son daldırma yapılması ve hayvanın ayakta tutulmasıdır.", "kategori": "Sürü Sağlığı"},
    {"soru": "Sığır besiciliğinde 'Kuru Madde Tüketimi' canlı ağırlığın yüzde kaçı olmalıdır?", "cevap": "Sağlıklı bir besi tosunu canlı ağırlığının ortalama %2.2 ila %2.6'sı kadar günlük kuru madde tüketmelidir.", "kategori": "Besi & Rasyon"},
    {"soru": "Ahır içi havalandırmada amonyak birikimini ve solunum yolu hastalıklarını önlemenin göstergesi nedir?", "cevap": "Hava giriş-çıkış hızı dakikada 2-3 metre olmalı, amonyak kokusu insan burnunu rahatsız etmeyecek seviyede (10 ppm altı) tutulmalı ve hava akımı doğrudan hayvanın üzerine esmemelidir.", "kategori": "Barınak & Refah"},
    {"soru": "Küçükbaş hayvancılıkta koç katımı öncesi 'Flushing' (ek yemleme) uygulaması ne sağlar?", "cevap": "Koç katımından 2-3 hafta önce koyunlara yüksek enerjili rasyon verilerek yumurtlama oranı ve ikizlik şansı belirgin şekilde artırılır.", "kategori": "Küçükbaş"},
    {"soru": "Ayak banyoları (bakır sülfat / çinko sülfat) süt sürülerinde hangi hastalığa karşı birincil kalkan vazifesi görür?", "cevap": "Ökçe siğili (dijital dermatit) ve parmak arası apselerin yayılmasını engeller; topallığı ve dolayısıyla süt kaybını önler.", "kategori": "Sürü Sağlığı"},
    {"soru": "Kanatlı kümeslerinde aydınlatma programının yumurta verimi üzerindeki etkisi nedir?", "cevap": "Yumurtlama döneminde günde 16 saat sabit aydınlatma uygulanarak hipofiz bezi uyarılır; aydınlatma süresinin aniden düşürülmesi tüy dökümüne ve yumurta kesilmesine yol açar.", "kategori": "Kanatlı"},
    {"soru": "Yonca kuru otunun ruminant beslemesindeki yeri ve protein değeri nedir?", "cevap": "Kaba yemlerin kraliçesi kabul edilen yonca, %17-20 ham protein içeriği ve yüksek kalsiyum oranıyla hem kemik gelişimini hem de süt verimini destekler.", "kategori": "Yem & Silaj"},
    {"soru": "Sıcaklık Stresi (THI indeksi 68+) ineklerde hangi verim kayıplarına yol açar?", "cevap": "Yem tüketimini %15-20 azaltır, süt veriminde 3-5 litreye varan düşüşe sebep olur, gebelik oranlarını zayıflatır ve asidoz riskini tetikler.", "kategori": "Sürü Yönetimi"}
]

def render_sidebar_calendar_widget(channel: str = "water") -> str:
    """Renders a seasonal calendar widget for the right sidebar."""
    if channel == "agriculture":
        return """
                <div class="sidebar-card sidebar-calendar-card">
                    <div class="sidebar-cal-header">
                        <span class="cal-icon">📅</span>
                        <div>
                            <h4 class="sidebar-title" style="margin-bottom:2px;">Kasım Ayı Saha &amp; Ekim Takvimi</h4>
                            <span style="font-size:11px; color:var(--ink-muted);">Anadolu Tarımsal İş Takvimi</span>
                        </div>
                    </div>
                    <div class="cal-task-list">
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🌾</span>
                            <div><strong>Tahıllar:</strong> Kışlık buğday ve arpa ekimlerinin tamamlanması, çimlenme ve kök boğazı kontrolü.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🫒</span>
                            <div><strong>Zeytincilik:</strong> Yağlık ve sofralık zeytin hasadı, zeytin sineği sonrası bakım ve bordo bulamacı.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🚜</span>
                            <div><strong>Toprak Hazırlığı:</strong> Derin kış sürümü, hayvan gübresi ve kompoze taban gübrelemesi.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">💧</span>
                            <div><strong>Sulama Tesisleri:</strong> Don öncesi damla sulama hatlarının boşaltılması ve pompa kış bakımı.</div>
                        </div>
                    </div>
                </div>
        """.strip()
    elif channel == "livestock":
        return """
                <div class="sidebar-card sidebar-calendar-card">
                    <div class="sidebar-cal-header">
                        <span class="cal-icon">📅</span>
                        <div>
                            <h4 class="sidebar-title" style="margin-bottom:2px;">Kasım Ayı Barınak &amp; Besi Takvimi</h4>
                            <span style="font-size:11px; color:var(--ink-muted);">Kışa Geçiş Dönemi Önlemleri</span>
                        </div>
                    </div>
                    <div class="cal-task-list">
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🌬️</span>
                            <div><strong>Barınak Yalıtımı:</strong> Ahır içi hava akımını kesip tepe havalandırmasını açık tutarak kış yalıtımı sağlama.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🐮</span>
                            <div><strong>Buzağı Bakımı:</strong> Isı lambaları ve buzağı battaniyelerinin hazırlanması, altlıkların kuru tutulması.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🌾</span>
                            <div><strong>Rasyon Enerji Artışı:</strong> Soğuk stresine karşı rasyondaki enerji oranının %10-15 artırılması.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🩺</span>
                            <div><strong>Koruyucu Aşılar:</strong> Pasteurella ve enterotoksemi aşı takviminin gözden geçirilmesi.</div>
                        </div>
                    </div>
                </div>
        """.strip()
    else:
        return """
                <div class="sidebar-card sidebar-calendar-card">
                    <div class="sidebar-cal-header">
                        <span class="cal-icon">📅</span>
                        <div>
                            <h4 class="sidebar-title" style="margin-bottom:2px;">2026-2027 Su Yılı &amp; Baraj Takvimi</h4>
                            <span style="font-size:11px; color:var(--ink-muted);">Hidrolojik Dönem Takibi</span>
                        </div>
                    </div>
                    <div class="cal-task-list">
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">💧</span>
                            <div><strong>Yeni Su Yılı:</strong> 1 Ekim itibariyle başlayan 2026-2027 hidrolojik su yılı havza izlemesi.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🏔️</span>
                            <div><strong>Kar Örtüsü:</strong> Fırat-Dicle ve Doğu Anadolu yükseklerindeki kar birikiminin izlenmesi.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">🛡️</span>
                            <div><strong>Taşkın Kontrolü:</strong> Kış yağışları öncesi baraj savak kapakları ve mansap tahliye testleri.</div>
                        </div>
                        <div class="cal-task-item">
                            <span class="cal-task-bullet">📊</span>
                            <div><strong>Yeraltı Suları:</strong> DSİ kış dönemi akifer seviye ve statik su tablası ölçümleri.</div>
                        </div>
                    </div>
                </div>
        """.strip()

def _build_flashcards_widget(channel: str = "water") -> str:
    """Builds an inline interactive 3D flashcard widget for the right sidebar."""
    import json as _json
    if channel == "agriculture":
        cards = _AGRICULTURE_FLASHCARDS
        title = "🌾 Akıllı Tarım &amp; Çiftçi Rehberi"
        desc = "Toprak verimliliği, damla sulama, gübreleme ve bitki koruma ipuçları"
        default_icon = "🌾"
        ext_link = "index.html#prices"
        ext_text = "Emtia Fiyatları ↗"
        icons_json = _json.dumps({
            "Ekim Nöbeti": "🌱", "Sulama & Tasarruf": "💧", "Toprak & Besleme": "🧪",
            "Gübreleme": "🌾", "Don Koruması": "❄️", "Bitki Koruma": "🛡️",
            "Akıllı Tarım": "🚜", "Tohumculuk": "🌾", "Biyoteknoloji": "🔬"
        }, ensure_ascii=False)
        colors_json = _json.dumps({
            "Ekim Nöbeti": "#16a34a", "Sulama & Tasarruf": "#0284c7", "Toprak & Besleme": "#ca8a04",
            "Gübreleme": "#d97706", "Don Koruması": "#2563eb", "Bitki Koruma": "#dc2626",
            "Akıllı Tarım": "#059669", "Tohumculuk": "#65a30d", "Biyoteknoloji": "#7c3aed"
        }, ensure_ascii=False)
    elif channel == "livestock":
        cards = _LIVESTOCK_FLASHCARDS
        title = "🐄 Modern Besi &amp; Sürü Yönetimi"
        desc = "Sürü sağlığı, buzağı bakımı, rasyon dengesi ve modern hayvancılık pratikleri"
        default_icon = "🐄"
        ext_link = "hayvancilik.html#prices"
        ext_text = "Yem Fiyatları ↗"
        icons_json = _json.dumps({
            "Buzağı Sağlığı": "🍼", "Süt Verimi": "🥛", "Besi & Rasyon": "🥩",
            "Yem & Silaj": "🌾", "Sürü Sağlığı": "🩺", "Barınak & Refah": "🏠",
            "Küçükbaş": "🐑", "Kanatlı": "🐔", "Sürü Yönetimi": "📊"
        }, ensure_ascii=False)
        colors_json = _json.dumps({
            "Buzağı Sağlığı": "#0284c7", "Süt Verimi": "#0891b2", "Besi & Rasyon": "#b91c1c",
            "Yem & Silaj": "#ca8a04", "Sürü Sağlığı": "#dc2626", "Barınak & Refah": "#475569",
            "Küçükbaş": "#16a34a", "Kanatlı": "#d97706", "Sürü Yönetimi": "#7c3aed"
        }, ensure_ascii=False)
    else:
        cards = _WATER_DIPLOMACY_CARDS
        title = "💧 Su Diplomasisi Bilgi Kartları"
        desc = "Sınıraşan su yönetimi ve uluslararası su hukukuna dair temel kavramlar"
        default_icon = "💧"
        ext_link = "https://mserman90.github.io/SuDiplomasisiBilgiKartlari/"
        ext_text = "Tüm Kartlar ↗"
        icons_json = _json.dumps({"Su Diplomasisi":"🌐","Havza Yönetimi":"💧","Uluslararası Hukuk":"⚖️","Çevresel Etkiler":"🌿"}, ensure_ascii=False)
        colors_json = _json.dumps({"Su Diplomasisi":"#0ea5e9","Havza Yönetimi":"#0284c7","Uluslararası Hukuk":"#7c3aed","Çevresel Etkiler":"#059669"}, ensure_ascii=False)

    total = len(cards)
    cards_json = _json.dumps(cards, ensure_ascii=False)

    template = f"""
                <div class="sidebar-card sdiplomasi-widget-card">
                    <div class="sdiplomasi-header">
                        <h4 class="sidebar-title" style="margin-bottom:4px;">{title}</h4>
                        <span class="sdiplomasi-badge">{total} Kart</span>
                    </div>
                    <p class="sdiplomasi-desc">{desc}</p>
                    <div class="sdiplomasi-card-wrap" id="sdcardWrap">
                        <div class="sdiplomasi-card" id="sdCard" onclick="sdFlipCard()">
                            <div class="sdiplomasi-card-inner" id="sdCardInner">
                                <div class="sdiplomasi-front">
                                    <span class="sd-category-tag" id="sdCategoryTag">Kategori</span>
                                    <div class="sd-card-icon" id="sdIcon">{default_icon}</div>
                                    <p class="sd-question" id="sdQuestion">Yükleniyor...</p>
                                    <span class="sd-flip-hint">Cevap için tıklayın ↩</span>
                                </div>
                                <div class="sdiplomasi-back">
                                    <span class="sd-category-tag sd-cat-back" id="sdCategoryTagBack">Kategori</span>
                                    <p class="sd-answer" id="sdAnswer">Cevap burada görünecek.</p>
                                    <span class="sd-flip-hint sd-flip-hint-back">Soruya dönmek için tıklayın ↩</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="sdiplomasi-nav">
                        <button class="sd-nav-btn" onclick="sdPrevCard()" title="Önceki Kart">◀</button>
                        <span class="sd-progress" id="sdProgress">1 / {total}</span>
                        <button class="sd-nav-btn" onclick="sdNextCard()" title="Sonraki Kart">▶</button>
                    </div>
                    <div class="sdiplomasi-footer-row">
                        <button class="sd-shuffle-btn" onclick="sdShuffle()" title="Kartları karıştır">🔀 Karıştır</button>
                        <a href="{ext_link}" target="_blank" rel="noopener noreferrer" class="sd-full-link">{ext_text}</a>
                    </div>
                    <script>
                    (function(){{
                        var SD = {cards_json};
                        var idx=0, flipped=false, deck=SD.slice();
                        var ICONS = {icons_json};
                        var COLORS = {colors_json};
                        var defaultIco = "{default_icon}";
                        function render(){{
                            var c=deck[idx]; if(!c) return;
                            var cat=c.kategori||"";
                            var qEl=document.getElementById("sdQuestion"); if(qEl) qEl.textContent=c.soru;
                            var aEl=document.getElementById("sdAnswer"); if(aEl) aEl.textContent=c.cevap;
                            ["sdCategoryTag","sdCategoryTagBack"].forEach(function(id){{
                                var el=document.getElementById(id);
                                if(el){{ el.textContent=cat; el.style.background=COLORS[cat]||"#0284c7"; }}
                            }});
                            var ico=document.getElementById("sdIcon"); if(ico) ico.textContent=ICONS[cat]||defaultIco;
                            var pr=document.getElementById("sdProgress"); if(pr) pr.textContent=(idx+1)+" / "+deck.length;
                            flipped=false;
                            var inn=document.getElementById("sdCardInner"); if(inn) inn.style.transform="rotateY(0deg)";
                        }}
                        window.sdFlipCard=function(){{
                            var inn=document.getElementById("sdCardInner"); if(!inn) return;
                            flipped=!flipped; inn.style.transform=flipped?"rotateY(180deg)":"rotateY(0deg)";
                        }};
                        window.sdNextCard=function(){{
                            if(flipped){{ window.sdFlipCard(); setTimeout(function(){{ idx=(idx+1)%deck.length; render(); }},300); }}
                            else{{ idx=(idx+1)%deck.length; render(); }}
                        }};
                        window.sdPrevCard=function(){{
                            if(flipped){{ window.sdFlipCard(); setTimeout(function(){{ idx=(idx-1+deck.length)%deck.length; render(); }},300); }}
                            else{{ idx=(idx-1+deck.length)%deck.length; render(); }}
                        }};
                        window.sdShuffle=function(){{
                            for(var i=deck.length-1;i>0;i--){{ var j=Math.floor(Math.random()*(i+1)); var t=deck[i]; deck[i]=deck[j]; deck[j]=t; }}
                            idx=0; render();
                        }};
                        if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",render);
                        else render();
                    }})();
                    </script>
                </div>
    """
    return template.strip()

def _build_diplomacy_flashcards_widget() -> str:
    """Backward compatibility wrapper."""
    return _build_flashcards_widget("water")

def generate_newspaper_portal_html(
    items: List[Dict[str, Any]],
    last_updated: str,
    rss_url: str,
    atom_url: str,
    json_url: str,
    channel: str = "agriculture",
    water_count: int = 0,
    agri_count: int = 0,
    livestock_count: int = 0,
    water_items: Optional[List[Dict[str, Any]]] = None,
    agri_items: Optional[List[Dict[str, Any]]] = None,
    livestock_items: Optional[List[Dict[str, Any]]] = None
) -> str:
    today_str = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    is_agri = (channel == "agriculture")
    is_livestock = (channel == "livestock")
    curr_channel_key = "livestock" if is_livestock else ("agriculture" if is_agri else "water")
    channel_events = get_channel_events(curr_channel_key)
    events_hub_html = render_events_hub_html(curr_channel_key, channel_events)
    sidebar_events_widget_html = render_sidebar_events_widget(curr_channel_key, channel_events)
    channel_prices = get_channel_prices(curr_channel_key)
    has_prices = (curr_channel_key in ("agriculture", "livestock"))
    prices_hub_html = render_prices_hub_html(curr_channel_key, channel_prices) if has_prices else ""
    sidebar_prices_widget_html = render_sidebar_prices_widget(curr_channel_key) if has_prices else ""
    tab_prices_label = "TARIMSAL EMTİA FİYATLARI (TR / DÜNYA)" if is_agri else ("HAYVANSAL ÜRÜN & YEM FİYATLARI (TR / DÜNYA)" if is_livestock else "PİYASA FİYATLARI")
    prices_badge_text = "Ürün"
    prices_tab_btn_html = f"""
                <button type="button" class="view-tab-btn" id="tabModePrices" onclick="switchPortalMainView('prices')">
                    <span class="view-tab-icon">📊</span>
                    <span class="view-tab-label" data-i18n="tab_mode_prices">{tab_prices_label}</span>
                    <span class="view-tab-badge prices-count-badge" id="pricesBadgeCount">{len(channel_prices)} {prices_badge_text}</span>
                </button>
    """ if has_prices else ""
    tab_news_label = "GÜNCEL HABER AKIŞI"
    tab_events_label = "ULUSLARARASI ZİRVELER & TOPLANTILAR"
    events_badge_text = "Zirve" 

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
            and not any(term in ((it.get("title_tr") or "") + " " + (it.get("title") or "")).lower() for term in livestock_terms)
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
            m_entry = {
                "id": it["id"],
                "title": it["title_tr"],
                "category": it["category"],
                "date": it["date"][:16] if it.get("date") else today_str,
                "source": it.get("source", ""),
                "summary": it.get("summary_tr", "")[:260],
                "lat": lat,
                "lng": lng,
                "loc": loc_name,
                "channel": channel
            }
            if channel == "agriculture":
                agri_map_data.append(m_entry)
            elif channel == "livestock":
                livestock_map_data.append(m_entry)
            else:
                water_map_data.append(m_entry)

    if channel != "water" and water_items:
        for idx, w_it in enumerate(water_items):
            wid = 30000 + idx
            title_tr = w_it.get("title_tr") or w_it.get("title") or ""
            summary_tr = w_it.get("summary_tr") or ""
            source = w_it.get("source_feed") or w_it.get("author") or "Su Basını"
            cat = w_it.get("category_tr") or "Su Kaynakları"
            img = w_it.get("image_url") or "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=900&q=80"
            lat, lng, loc_name = geocode_article(w_it, wid)
            all_articles_data.append({
                "id": wid,
                "title_tr": title_tr,
                "title_en": w_it.get("title_en") or w_it.get("title") or title_tr,
                "summary_tr": summary_tr,
                "summary_en": w_it.get("summary_en") or "",
                "category": cat,
                "channel_key": "water",
                "channel_name": "Su Gündemi",
                "channel_name_en": "Water Agenda",
                "slug": "su",
                "source": source,
                "author": w_it.get("author", "Hidroloji Muhabiri"),
                "date": w_it.get("pub_date", today_str),
                "link": w_it.get("link", "#"),
                "image": img,
                "is_turkey": w_it.get("is_turkey", False),
                "is_academic": w_it.get("is_academic", False)
            })
            if lat is not None and lng is not None:
                water_map_data.append({
                    "id": wid,
                    "title": title_tr,
                    "category": cat,
                    "date": (w_it.get("pub_date") or today_str)[:16],
                    "source": source,
                    "summary": summary_tr[:260],
                    "lat": lat,
                    "lng": lng,
                    "loc": loc_name,
                    "channel": "water"
                })

    if channel != "agriculture" and agri_items:
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

    if channel != "livestock" and livestock_items:
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

                            <label class="panel-layer-card active" data-layer="events" id="layerBtn_events" title="Uluslararası Zirveler &amp; Toplantılar Katmanı">
                                <div class="layer-card-left">
                                    <input type="checkbox" id="layerEventsCheck" checked onchange="toggleMapLayer('events')">
                                    <span class="layer-dot" style="background:#d97706; box-shadow:0 0 6px #d97706;"></span>
                                    <div class="layer-card-info">
                                        <span class="layer-name">🌐 Uluslararası Zirveler</span>
                                        <span class="layer-desc">Küresel kongreler, BM &amp; zirveler</span>
                                    </div>
                                </div>
                                <span class="layer-count" style="background:rgba(217,119,6,0.18); color:#d97706;">{len(channel_events)}</span>
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
            <a href="index.html" class="channel-tab-btn {agri_active_cls}" id="tabAgri" title="Tarım Gündemi">
                <span class="channel-tab-icon">🌾</span>
                <span class="channel-tab-name" id="tabNameAgri" data-i18n="tab_agri">TARIM GÜNDEMİ</span>
                {agri_badge_count}
            </a>
            <a href="su.html" class="channel-tab-btn {water_active_cls}" id="tabWater" title="Su Gündemi">
                <span class="channel-tab-icon">💧</span>
                <span class="channel-tab-name" id="tabNameWater" data-i18n="tab_water">SU GÜNDEMİ</span>
                {water_badge_count}
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
                <button type="button" class="cat-btn cat-btn-events" data-slug="events" onclick="filterCategory('events')" title="Uluslararası Zirveler &amp; Toplantılar">🌐 <span data-i18n="nav_events_pill">Uluslararası Zirveler</span></button>
                <button type="button" class="cat-btn cat-btn-prices" data-slug="prices" onclick="filterCategory('prices')" title="Hayvansal Ürün &amp; Yem Fiyatları (TR vs Dünya)">📊 <span data-i18n="nav_prices_pill">Ürün Fiyatları</span></button>
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
        sidebar_diplomacy_cards_html = _build_flashcards_widget("livestock")
        sidebar_calendar_widget_html = render_sidebar_calendar_widget("livestock")
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
                <button type="button" class="cat-btn cat-btn-events" data-slug="events" onclick="filterCategory('events')" title="Uluslararası Zirveler &amp; Kongreler">🌐 <span data-i18n="nav_events_pill">Uluslararası Zirveler</span></button>
                <button type="button" class="cat-btn cat-btn-prices" data-slug="prices" onclick="filterCategory('prices')" title="Tarımsal Ürün &amp; Emtia Fiyatları (TR vs Dünya)">📊 <span data-i18n="nav_prices_pill">Emtia Fiyatları</span></button>
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
        sidebar_diplomacy_cards_html = _build_flashcards_widget("agriculture")
        sidebar_calendar_widget_html = render_sidebar_calendar_widget("agriculture")
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
                <button type="button" class="cat-btn cat-btn-events" data-slug="events" onclick="filterCategory('events')" title="Uluslararası Zirveler &amp; Toplantılar">🌐 <span data-i18n="nav_events_pill">Uluslararası Zirveler</span></button>
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
        sidebar_diplomacy_cards_html = _build_flashcards_widget("water")
        sidebar_calendar_widget_html = render_sidebar_calendar_widget("water")
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

    
    base_public_url = "https://mserman90.github.io/suhaber"
    if is_livestock:
        canonical_url = f"{base_public_url}/hayvancilik.html"
        page_seo_title = "Hayvancılık Gündemi | Türkiye ve Dünya Hayvancılık, Süt, Besi & Yem Gazetesi"
        page_seo_desc = "Türkiye ve dünya hayvancılık sektörü, çiğ süt tavsiye fiyatları, büyükbaş ve küçükbaş karkas et piyasası, yem maliyetleri, hayvan sağlığı ve uluslararası hayvancılık zirveleri dijital gazetesi."
        page_seo_keywords = "hayvancılık gündemi, karkas et fiyatları, çiğ süt fiyatı, büyükbaş besicilik, küçükbaş hayvancılık, yem fiyatları, et ve süt kurumu, damızlık sığır, hayvancılık destekleri, hayvan sağlığı"
        og_image = "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=1200&h=630&fit=crop&q=85"
    elif is_agri:
        canonical_url = f"{base_public_url}/index.html"
        page_seo_title = "Tarım Gündemi | Türkiye ve Dünya Tarım, Bitkisel Üretim & Çiftçi Gazetesi"
        page_seo_desc = "Türkiye ve dünya tarım, bitkisel üretim, tohumculuk, gübre, sulama ve akıllı tarım sektörü güncel haberleri; uluslararası tarım kongreleri, buğday, mısır, pamuk ve ayçiçeği piyasa fiyatları."
        page_seo_keywords = "tarım gündemi, buğday fiyatları, gübre fiyatları, mazot gübre desteği, bitkisel üretim, akıllı tarım, çukurova tarım, konya ovası, tohumculuk, tarımsal emtia borsası, tmo alım fiyatları, tarım haberleri"
        og_image = "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1200&h=630&fit=crop&q=85"
    else:
        canonical_url = f"{base_public_url}/su.html"
        page_seo_title = "Su Gündemi | Türkiye ve Dünya Su Kaynakları, Sulama, Barajlar & GIS Atlası"
        page_seo_desc = "Türkiye ve dünya su kaynakları, baraj doluluk oranları, kuraklık haritası, tarımsal sulama ve hidro-jeolojik araştırmalar dijital gazetesi. İnteraktif GIS atlası, uluslararası su zirveleri ve canlı haber akışı."
        page_seo_keywords = "su gündemi, türkiye baraj doluluk oranları, dsi barajları, su kaynakları, kuraklık haritası, tarımsal sulama, su anlaşmaları, su stresi, su krizi, yeraltı suları, fırat dicle havzası, gis su haritası"
        og_image = "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1200&h=630&fit=crop&q=85"

    json_ld_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{base_public_url}/#website",
                "url": f"{base_public_url}/",
                "name": "Tarım, Su ve Hayvancılık Dijital Gazete Portalı",
                "alternateName": "Agriculture, Water & Livestock Digital Newspaper",
                "description": "Türkiye ve Dünya Tarım, Su ve Hayvancılık haberleri, tarımsal emtia & girdi fiyatları, interaktif GIS atlası ve uluslararası zirveler.",
                "inLanguage": ["tr-TR", "en-US"],
                "publisher": {
                    "@id": f"{base_public_url}/#organization"
                }
            },
            {
                "@type": "NewsMediaOrganization",
                "@id": f"{base_public_url}/#organization",
                "name": "Su & Tarım & Hayvancılık Dijital Gazetesi",
                "url": f"{base_public_url}/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=600&h=600&fit=crop&q=85"
                },
                "sameAs": [
                    "https://github.com/mserman90/suhaber",
                    "https://mserman90.github.io/water-agreements-portal/"
                ]
            },
            {
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": page_seo_title,
                "description": page_seo_desc,
                "isPartOf": {
                    "@id": f"{base_public_url}/#website"
                },
                "inLanguage": "tr-TR"
            }
        ]
    }
    json_ld_script_tag = f'<script type="application/ld+json">\n{json.dumps(json_ld_schema, ensure_ascii=False, indent=2)}\n    </script>'

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_seo_title}</title>
    
    <!-- Google SEO & Discoverability Meta Tags -->
    <meta name="description" content="{page_seo_desc}">
    <meta name="keywords" content="{page_seo_keywords}">
    <meta name="author" content="Su & Tarım & Hayvancılık Dijital Gazetesi">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <link rel="canonical" href="{canonical_url}">
    <meta name="theme-color" content="#0a192f">

    <!-- Open Graph Protocol (Facebook, WhatsApp, LinkedIn, Slack) -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="Su, Tarım ve Hayvancılık Dijital Gazete Portalı">
    <meta property="og:title" content="{page_seo_title}">
    <meta property="og:description" content="{page_seo_desc}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{portal_name}">
    <meta property="og:locale" content="tr_TR">
    <meta property="og:locale:alternate" content="en_US">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{page_seo_title}">
    <meta name="twitter:description" content="{page_seo_desc}">
    <meta name="twitter:image" content="{og_image}">

    <!-- Feed Readers & Syndication (RSS / Atom / JSON Feed) -->
    <link rel="alternate" type="application/rss+xml" title="{portal_name} (RSS 2.0)" href="{rss_url}">
    <link rel="alternate" type="application/atom+xml" title="{portal_name} (Atom)" href="{atom_url}">
    <link rel="alternate" type="application/feed+json" title="{portal_name} (JSON)" href="{json_url}">

    <!-- Schema.org JSON-LD Structured Data for Google Rich Results -->
    {json_ld_script_tag}

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

    <!-- Newspaper Portal Core Stylesheet -->
    <link rel="stylesheet" href="assets/css/portal.css">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#0b2545">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <link rel="icon" type="image/svg+xml" href="assets/icons/icon.svg">
    <link rel="apple-touch-icon" href="assets/icons/icon.svg">
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

        <!-- View Mode Switcher Tabs (Haber Akışı vs Uluslararası Zirveler) -->
        <div class="view-mode-tabs-bar" id="portalViewTabs">
            <div class="view-mode-tabs-inner">
                <button type="button" class="view-tab-btn active" id="tabModeNews" onclick="switchPortalMainView('news')">
                    <span class="view-tab-icon">📰</span>
                    <span class="view-tab-label" data-i18n="tab_mode_news">{tab_news_label}</span>
                    <span class="view-tab-badge" id="newsBadgeCount">{len(items)}</span>
                </button>
                <button type="button" class="view-tab-btn" id="tabModeEvents" onclick="switchPortalMainView('events')">
                    <span class="view-tab-icon">🌐</span>
                    <span class="view-tab-label" data-i18n="tab_mode_events">{tab_events_label}</span>
                    <span class="view-tab-badge events-count-badge" id="eventsBadgeCount">{len(channel_events)} {events_badge_text}</span>
                </button>
                {prices_tab_btn_html}
            </div>
        </div>

        <!-- Columns Section -->
        <div class="newspaper-columns">
            
            <!-- Left Main Column: News Grid -->
            <div class="main-articles-col" id="newsGridCol">
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

            <!-- Left Main Column: Events Hub (Switched with News Grid) -->
            {events_hub_html}

            <!-- Left Main Column: Prices Hub (Switched with News Grid) -->
            {prices_hub_html}

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

                <!-- Commodity & Livestock Prices Widget -->
                {sidebar_prices_widget_html}

                <!-- Seasonal Calendar Widget -->
                {sidebar_calendar_widget_html}

                <!-- Interactive Flashcards Widget -->
                {sidebar_diplomacy_cards_html}

                <!-- Upcoming Events Widget -->
                {sidebar_events_widget_html}

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

    {render_legal_modal_html()}

    <!-- Newspaper Footer -->
    <footer class="newspaper-footer" role="contentinfo">
        <div class="footer-inner">
            <h4 id="footerPortalName">{portal_name}</h4>
            <p id="footerSubText">{footer_sub_text}</p>
            {render_footer_legal_bar_html()}
            <p class="footer-meta-info" style="font-size:11.5px; opacity:0.8; margin-top:16px;">
                <span data-i18n="footer_automation">Otomasyon: GitHub Actions ile periyodik olarak derlenir</span> &bull; 
                <span data-i18n="footer_last_update">Son Güncelleme:</span> {last_updated} &bull; 
                <span>Depo: <a href="https://github.com/mserman90/suhaber" target="_blank" rel="noopener noreferrer" style="color:inherit; text-decoration:underline;">mserman90/suhaber</a></span>
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
            // 4. International Summits Layer
            const eventsGroup = L.layerGroup();
            const eventIcon = L.divIcon({{
                className: 'custom-event-map-pin',
                html: '<div style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; border: 2px solid #fff; box-shadow: 0 4px 10px rgba(0,0,0,0.35); cursor: pointer;">🌐</div>',
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            }});
            channelEventsData.forEach(ev => {{
                if (!ev.lat || !ev.lng) return;
                const marker = L.marker([ev.lat, ev.lng], {{ icon: eventIcon, title: ev.title_tr }});
                const popupContent = `
                    <div style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; min-width:240px; max-width:300px; padding:2px;">
                        <div style="background:linear-gradient(135deg,#d97706,#b45309); color:#fff; padding:6px 10px; border-radius:6px; font-weight:800; font-size:11.5px; margin-bottom:8px;">
                            ${{ev.flag}} ${{ev.acronym}} &bull; ULUSLARARASI ZİRVE
                        </div>
                        <h4 style="margin:0 0 6px 0; font-size:14px; font-weight:700; color:#0f172a; line-height:1.3;">${{ev.title_tr}}</h4>
                        <div style="font-size:12px; color:#d97706; font-weight:700; margin-bottom:4px;">🗓️ ${{ev.date_display_tr}}</div>
                        <div style="font-size:11.5px; color:#64748b; margin-bottom:8px;">📍 ${{ev.location_city}}, ${{ev.location_country_tr}} &bull; 🏛️ ${{ev.organizer_tr}}</div>
                        <p style="font-size:12px; line-height:1.45; color:#334155; margin:0 0 10px 0;">${{ev.summary_tr.slice(0, 150)}}...</p>
                        <a href="${{ev.url}}" target="_blank" rel="noopener noreferrer" style="display:inline-block; font-size:12px; font-weight:700; color:#d97706; text-decoration:none;">Resmi Web Sitesini İncele &rarr;</a>
                    </div>
                `;
                marker.bindPopup(popupContent);
                eventsGroup.addLayer(marker);
            }});
            portalMap.addLayer(eventsGroup);
            mapLayers['events'] = eventsGroup;

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
            const layerIds = ['water', 'agri', 'livestock', 'events', 'agreements', 'conflicts', 'basins'];
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
            const otherIds = ['agri', 'livestock', 'events', 'agreements', 'conflicts', 'basins'];
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

            if (layerId === 'water' || layerId === 'agri' || layerId === 'livestock' || layerId === 'events') {{
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
            document.getElementById('modalContent').innerHTML = (summary || '').split(String.fromCharCode(10)).filter(p => p.trim()).map(p => '<p>' + p + '</p>').join('') || '<p></p>'
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
            if (e.key === 'Escape') {{
                closeArticleModal();
                closeLegalModal();
            }}
        }});

        function openLegalModal(tabName) {{
            const m = document.getElementById('legalModal');
            if (m) {{
                m.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                switchLegalTab(tabName || 'disclaimer');
            }}
        }}

        function closeLegalModal(e) {{
            if (e && e.target && e.target.closest && e.target.closest('.legal-modal-window') && !e.target.classList.contains('btn-close-modal') && !e.target.classList.contains('btn-legal-close')) {{
                return;
            }}
            const m = document.getElementById('legalModal');
            if (m) {{
                m.style.display = 'none';
                document.body.style.overflow = '';
            }}
        }}

        function switchLegalTab(tabName) {{
            ['disclaimer', 'kvkk', 'imprint'].forEach(t => {{
                const btn = document.getElementById('btnLegalTab_' + t);
                const pane = document.getElementById('legalPane_' + t);
                if (btn) btn.classList.toggle('active', t === tabName);
                if (pane) pane.style.display = (t === tabName) ? 'block' : 'none';
            }});
        }}

                // Bilingual (Turkish / English) Engine
        window.currentPortalLang = localStorage.getItem('portal_language') || 'tr';

        const CHANNEL_CONFIG = {{
            channel_key: '{channel_key}',
            is_agri: {'true' if is_agri else 'false'},
            is_livestock: {'true' if is_livestock else 'false'},
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

            
            // 12. Update View Tabs & International Events Hub Elements
            const tabNewsLabel = document.querySelector('[data-i18n="tab_mode_news"]');
            const tabEventsLabel = document.querySelector('[data-i18n="tab_mode_events"]');
            const navEventsPill = document.querySelector('[data-i18n="nav_events_pill"]');
            if (tabNewsLabel) tabNewsLabel.innerText = isEn ? 'LATEST NEWS FEED' : 'GÜNCEL HABER AKIŞI';
            if (tabEventsLabel) tabEventsLabel.innerText = isEn ? 'INTERNATIONAL SUMMITS & CONFERENCES' : 'ULUSLARARASI ZİRVELER & TOPLANTILAR';
            if (navEventsPill) navEventsPill.innerText = isEn ? 'International Summits' : 'Uluslararası Zirveler';

            const evBadge = document.getElementById('eventsSectionBadge');
            const evSectionTitle = document.getElementById('eventsSectionTitle');
            const evSectionDesc = document.getElementById('eventsSectionDesc');
            if (evBadge && typeof CHANNEL_EVENTS_CONFIG !== 'undefined') evBadge.innerText = isEn ? CHANNEL_EVENTS_CONFIG.badge_en : CHANNEL_EVENTS_CONFIG.badge_tr;
            if (evSectionTitle && typeof CHANNEL_EVENTS_CONFIG !== 'undefined') evSectionTitle.innerText = isEn ? CHANNEL_EVENTS_CONFIG.title_en : CHANNEL_EVENTS_CONFIG.title_tr;
            if (evSectionDesc && typeof CHANNEL_EVENTS_CONFIG !== 'undefined') evSectionDesc.innerText = isEn ? CHANNEL_EVENTS_CONFIG.desc_en : CHANNEL_EVENTS_CONFIG.desc_tr;

            document.querySelectorAll('.event-subtab-btn[data-event-cat]').forEach(btn => {{
                const cat = btn.getAttribute('data-event-cat');
                if (typeof EVENT_CAT_TRANSLATIONS !== 'undefined' && EVENT_CAT_TRANSLATIONS[cat]) {{
                    const labelSpan = btn.querySelector('span');
                    if (labelSpan) {{
                        labelSpan.innerText = isEn ? EVENT_CAT_TRANSLATIONS[cat].en : EVENT_CAT_TRANSLATIONS[cat].tr;
                    }}
                }}
            }});

            document.querySelectorAll('[data-event-card-id]').forEach(card => {{
                const eid = card.getAttribute('data-event-card-id');
                const evData = (typeof channelEventsData !== 'undefined') ? channelEventsData.find(e => e.id === eid) : null;
                if (evData) {{
                    const titleEl = card.querySelector('.event-card-title');
                    const orgEl = card.querySelector('.event-org-text');
                    const dateEl = card.querySelector('.event-date-text');
                    const locEl = card.querySelector('.event-loc-text');
                    const descEl = card.querySelector('.event-card-desc');
                    const cycleEl = card.querySelector('.event-cycle-badge');
                    const catBadge = card.querySelector('.event-cat-badge');

                    if (titleEl) titleEl.innerText = isEn ? evData.title_en : evData.title_tr;
                    if (orgEl) orgEl.innerText = isEn ? evData.organizer_en : evData.organizer_tr;
                    if (dateEl) dateEl.innerText = isEn ? evData.date_display_en : evData.date_display_tr;
                    if (locEl) locEl.innerText = `${{evData.location_city}}, ${{isEn ? evData.location_country_en : evData.location_country_tr}}`;
                    if (descEl) descEl.innerText = isEn ? evData.summary_en : evData.summary_tr;
                    if (cycleEl) cycleEl.innerText = isEn ? evData.cycle_en : evData.cycle_tr;
                    if (catBadge && typeof EVENT_CAT_TRANSLATIONS !== 'undefined' && EVENT_CAT_TRANSLATIONS[evData.category]) {{
                        catBadge.innerText = isEn ? EVENT_CAT_TRANSLATIONS[evData.category].en : EVENT_CAT_TRANSLATIONS[evData.category].tr;
                    }}
                }}
            }});

            // 13. Update Prices Hub Elements
            const tabPricesLabel = document.querySelector('[data-i18n="tab_mode_prices"]');
            const navPricesPill = document.querySelector('[data-i18n="nav_prices_pill"]');
            if (tabPricesLabel) tabPricesLabel.innerText = isEn ? (CHANNEL_CONFIG.is_agri ? 'AGRI COMMODITY PRICES (TR / WORLD)' : 'LIVESTOCK & FEED PRICES (TR / WORLD)') : (CHANNEL_CONFIG.is_agri ? 'TARIMSAL EMTİA FİYATLARI (TR / DÜNYA)' : 'HAYVANSAL ÜRÜN & YEM FİYATLARI (TR / DÜNYA)');
            if (navPricesPill) navPricesPill.innerText = isEn ? (CHANNEL_CONFIG.is_agri ? 'Commodity Prices' : 'Product Prices') : (CHANNEL_CONFIG.is_agri ? 'Emtia Fiyatları' : 'Ürün Fiyatları');

            const prBadge = document.getElementById('pricesSectionBadge');
            const prSectionTitle = document.getElementById('pricesSectionTitle');
            const prSectionDesc = document.getElementById('pricesSectionDesc');
            if (prBadge && typeof CHANNEL_PRICES_CONFIG !== 'undefined') prBadge.innerText = isEn ? CHANNEL_PRICES_CONFIG.badge_en : CHANNEL_PRICES_CONFIG.badge_tr;
            if (prSectionTitle && typeof CHANNEL_PRICES_CONFIG !== 'undefined') prSectionTitle.innerText = isEn ? CHANNEL_PRICES_CONFIG.title_en : CHANNEL_PRICES_CONFIG.title_tr;
            if (prSectionDesc && typeof CHANNEL_PRICES_CONFIG !== 'undefined') prSectionDesc.innerText = isEn ? CHANNEL_PRICES_CONFIG.desc_en : CHANNEL_PRICES_CONFIG.desc_tr;

            document.querySelectorAll('.price-subtab-btn[data-price-cat]').forEach(btn => {{
                const cat = btn.getAttribute('data-price-cat');
                if (typeof PRICE_CAT_TRANSLATIONS !== 'undefined' && PRICE_CAT_TRANSLATIONS[cat]) {{
                    const labelSpan = btn.querySelector('span');
                    if (labelSpan) {{
                        labelSpan.innerText = isEn ? PRICE_CAT_TRANSLATIONS[cat].en : PRICE_CAT_TRANSLATIONS[cat].tr;
                    }}
                }}
            }});

            document.querySelectorAll('[data-price-card-id]').forEach(card => {{
                const pid = card.getAttribute('data-price-card-id');
                const pData = (typeof channelPricesData !== 'undefined') ? channelPricesData.find(p => p.id === pid) : null;
                if (pData) {{
                    const titleEl = card.querySelector('.price-card-title');
                    const unitEl = card.querySelector('.price-card-unit');
                    const noteEl = card.querySelector('.analysis-text');
                    const trendEl = card.querySelector('.price-trend-tag');
                    const diffBadge = card.querySelector('.price-diff-badge');

                    if (titleEl) titleEl.innerText = isEn ? pData.name_en : pData.name_tr;
                    if (unitEl) unitEl.innerHTML = isEn ? `Unit: <strong>${{pData.unit_en}}</strong>` : `Birim: <strong>${{pData.unit_tr}}</strong>`;
                    if (noteEl) noteEl.innerText = isEn ? pData.note_en : pData.note_tr;
                    if (trendEl) {{
                        const icon = pData.trend === 'up' ? '▲' : (pData.trend === 'down' ? '▼' : '▬');
                        trendEl.innerText = `${{icon}} ${{isEn ? pData.change_en : pData.change_tr}}`;
                    }}
                    if (diffBadge) {{
                        if (pData.diff_status === 'premium') {{
                            diffBadge.innerText = isEn ? `🇹🇷 ${{pData.diff_vs_world_pct}} Premium vs World` : `🇹🇷 ${{pData.diff_vs_world_pct}} Primli (TR Yüksek)`;
                        }} else if (pData.diff_status === 'discount') {{
                            diffBadge.innerText = isEn ? `🇹🇷 ${{pData.diff_vs_world_pct}} Discount vs World` : `🇹🇷 ${{pData.diff_vs_world_pct}} İskontolu (TR Uygun)`;
                        }} else {{
                            diffBadge.innerText = isEn ? `🇹🇷 ${{pData.diff_vs_world_pct}} Parity` : `🇹🇷 ${{pData.diff_vs_world_pct}} Başa Baş / Dengeli`;
                        }}
                    }}

                    // Country names in cells
                    const cellTR = card.querySelector('.price-cell-tr .cell-country-name');
                    const cellEU = card.querySelector('.price-cell-eu .cell-country-name');
                    const cellUS = card.querySelector('.price-cell-us .cell-country-name');
                    const cellWorld = card.querySelector('.price-cell-world .cell-country-name');
                    if (cellTR) cellTR.innerText = isEn ? 'Turkey' : 'Türkiye';
                    if (cellEU) cellEU.innerText = isEn ? 'European Union' : 'Avrupa Birliği';
                    if (cellUS) cellUS.innerText = isEn ? 'United States' : 'ABD';
                    if (cellWorld) cellWorld.innerText = isEn ? pData.world_name_en : pData.world_name_tr;
                }}
            }});

            const sidePrTitle = document.getElementById('sidePricesTitle');
            const sidePrBtn = document.getElementById('sidePricesBtn');
            if (sidePrTitle) sidePrTitle.innerText = isEn ? (CHANNEL_CONFIG.is_agri ? 'Commodity Markets (TR / World)' : 'Livestock & Feed Markets') : (CHANNEL_CONFIG.is_agri ? '🌾 Emtia Piyasaları (TR / Dünya)' : '🐄 Hayvancılık & Yem Piyasası');
            if (sidePrBtn) sidePrBtn.innerText = isEn ? 'View Full Comparison Table →' : 'Tam Karşılaştırma Tablosunu Gör →';

            // 11. If an article modal is currently open, refresh it in the active language
            if (window.currentModalArticleId !== null && window.currentModalArticleId !== undefined) {{
                openArticleModal(window.currentModalArticleId);
            }}

            // 11. Legal & KVKK Footer & Modal i18n
            const disclaimerBtn = document.querySelector('[data-i18n="legal_disclaimer_btn"]');
            if (disclaimerBtn) disclaimerBtn.innerText = isEn ? 'Legal Disclaimer' : 'Yasal Sorumluluk Reddi';

            const kvkkBtn = document.querySelector('[data-i18n="legal_kvkk_btn"]');
            if (kvkkBtn) kvkkBtn.innerText = isEn ? 'Privacy & Data Protection' : 'KVKK & Gizlilik Beyanı';

            const imprintBtn = document.querySelector('[data-i18n="legal_imprint_btn"]');
            if (imprintBtn) imprintBtn.innerText = isEn ? 'Imprint & Copyright' : 'Künye & Atıf Politikası';

            const standaloneLink = document.querySelector('[data-i18n="legal_standalone_link"]');
            if (standaloneLink) standaloneLink.innerText = isEn ? 'Full Text (Separate Page)' : 'Tam Metin (Ayrı Sayfa)';

            const footerAuto = document.querySelector('[data-i18n="footer_automation"]');
            if (footerAuto) footerAuto.innerText = isEn ? 'Automated: Built regularly via GitHub Actions' : 'Otomasyon: GitHub Actions ile düzenli derlenir';

            const footerLastUp = document.querySelector('[data-i18n="footer_last_update"]');
            if (footerLastUp) footerLastUp.innerText = isEn ? 'Last Updated:' : 'Son Güncelleme:';

            const microDisclaimer = document.getElementById('footerMicroDisclaimer');
            if (microDisclaimer) {{
                microDisclaimer.innerHTML = isEn
                    ? '<strong>⚖️ Legal Notice:</strong> All market, commodity and news data are curated from open public sources and do not constitute financial or investment advice. In compliance with KVKK, no personal data is collected on this portal.'
                    : '<strong>⚖️ Yasal Uyarı:</strong> Bu portalda yer alan haber, emtia ve borsa verileri açık kaynaklardan derlenmiş olup, yatırım veya ticari danışmanlık niteliği taşımaz. 6698 sayılı KVKK kapsamında ziyaretçilerden kişisel veri toplanmamaktadır.';
            }}

            const modalBadge = document.getElementById('legalModalBadge');
            if (modalBadge) modalBadge.innerText = isEn ? 'LEGAL DISCLOSURE & TRANSPARENCY NOTICE' : 'HUKUKİ BİLGİLENDİRME & ŞEFFAFLIK BEYANI';

            const modalTitle = document.getElementById('legalModalTitle');
            if (modalTitle) modalTitle.innerText = isEn ? 'Legal Disclaimer and Privacy Notice' : 'Yasal Sorumluluk Reddi ve KVKK Bildirimi';

            const tabDisc = document.querySelector('[data-i18n="legal_tab_disclaimer"]');
            if (tabDisc) tabDisc.innerText = isEn ? 'Legal Disclaimer' : 'Yasal Sorumluluk Reddi';

            const tabKVKK = document.querySelector('[data-i18n="legal_tab_kvkk"]');
            if (tabKVKK) tabKVKK.innerText = isEn ? 'Privacy & KVKK' : 'KVKK & Gizlilik Beyanı';

            const tabImp = document.querySelector('[data-i18n="legal_tab_imprint"]');
            if (tabImp) tabImp.innerText = isEn ? 'Imprint & Attribution' : 'Künye & Atıf Politikası';

            const btnCloseLegal = document.querySelector('[data-i18n="legal_close_btn"]');
            if (btnCloseLegal) btnCloseLegal.innerText = isEn ? 'Understood & Close' : 'Anladım ve Kapat';

            // Toggle language inside modal
            document.querySelectorAll('.legal-lang-tr').forEach(el => el.style.display = isEn ? 'none' : 'block');
            document.querySelectorAll('.legal-lang-en').forEach(el => el.style.display = isEn ? 'block' : 'none');
        }}

        // Initialize language immediately
        document.addEventListener('DOMContentLoaded', function() {{
            setPortalLanguage(window.currentPortalLang);
        }});


        const channelEventsData = {json.dumps(channel_events, ensure_ascii=False)};
        const CHANNEL_EVENTS_CONFIG = {json.dumps(CHANNEL_EVENTS_METADATA.get(curr_channel_key, {}), ensure_ascii=False)};
        const EVENT_CAT_TRANSLATIONS = {json.dumps(EVENT_CATEGORIES, ensure_ascii=False)};

        const channelPricesData = {json.dumps(channel_prices, ensure_ascii=False)};
        const CHANNEL_PRICES_CONFIG = {json.dumps(CHANNEL_PRICES_METADATA.get(curr_channel_key, {}), ensure_ascii=False)};
        const PRICE_CAT_TRANSLATIONS = {json.dumps(PRICE_CATEGORIES.get(curr_channel_key, {}), ensure_ascii=False)};

        function switchPortalMainView(viewMode) {{
            const tabNews = document.getElementById('tabModeNews');
            const tabEvents = document.getElementById('tabModeEvents');
            const tabPrices = document.getElementById('tabModePrices');
            const newsCol = document.getElementById('newsGridCol');
            const eventsCol = document.getElementById('eventsHubCol');
            const pricesCol = document.getElementById('pricesHubCol');
            const heroEl = document.getElementById('heroSection');
            const subEl = document.getElementById('subHeadlinesSection');

            // Update category button active states
            document.querySelectorAll('.cat-btn').forEach(btn => {{
                if (btn.dataset.slug === 'events') {{
                    btn.classList.toggle('active', viewMode === 'events');
                }} else if (btn.dataset.slug === 'prices') {{
                    btn.classList.toggle('active', viewMode === 'prices');
                }} else if (viewMode === 'events' || viewMode === 'prices') {{
                    btn.classList.remove('active');
                }}
            }});

            if (viewMode === 'events') {{
                if (tabNews) tabNews.classList.remove('active');
                if (tabEvents) tabEvents.classList.add('active');
                if (tabPrices) tabPrices.classList.remove('active');
                if (newsCol) newsCol.style.display = 'none';
                if (eventsCol) eventsCol.style.display = 'block';
                if (pricesCol) pricesCol.style.display = 'none';
                if (heroEl) heroEl.style.display = 'none';
                if (subEl) subEl.style.display = 'none';
                eventsCol.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }} else if (viewMode === 'prices') {{
                if (tabNews) tabNews.classList.remove('active');
                if (tabEvents) tabEvents.classList.remove('active');
                if (tabPrices) tabPrices.classList.add('active');
                if (newsCol) newsCol.style.display = 'none';
                if (eventsCol) eventsCol.style.display = 'none';
                if (pricesCol) pricesCol.style.display = 'block';
                if (heroEl) heroEl.style.display = 'none';
                if (subEl) subEl.style.display = 'none';
                pricesCol.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }} else {{
                if (tabNews) tabNews.classList.add('active');
                if (tabEvents) tabEvents.classList.remove('active');
                if (tabPrices) tabPrices.classList.remove('active');
                if (newsCol) newsCol.style.display = '';
                if (eventsCol) eventsCol.style.display = 'none';
                if (pricesCol) pricesCol.style.display = 'none';
                if (currentSlug === 'all') {{
                    if (heroEl) heroEl.style.display = '';
                    if (subEl) subEl.style.display = '';
                }}
            }}
        }}

        function filterPriceCategory(catSlug) {{
            document.querySelectorAll('.price-subtab-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-price-cat') === catSlug);
            }});
            const cards = document.querySelectorAll('.price-compare-card');
            let visibleCount = 0;
            cards.forEach(card => {{
                const cCat = card.getAttribute('data-price-cat');
                if (catSlug === 'all' || cCat === catSlug) {{
                    card.style.display = '';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            const emptyEl = document.getElementById('pricesEmptyState');
            if (emptyEl) {{
                emptyEl.style.display = (visibleCount === 0) ? 'block' : 'none';
            }}
        }}

        function filterEventCategory(catSlug) {{
            document.querySelectorAll('.event-subtab-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-event-cat') === catSlug);
            }});
            const cards = document.querySelectorAll('.event-card');
            let visibleCount = 0;
            cards.forEach(card => {{
                const cCat = card.getAttribute('data-event-cat');
                if (catSlug === 'all' || cCat === catSlug) {{
                    card.style.display = '';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            const emptyEl = document.getElementById('eventsEmptyState');
            if (emptyEl) {{
                emptyEl.style.display = (visibleCount === 0) ? 'block' : 'none';
            }}
        }}

        function focusEventOnMap(lat, lng, acronym) {{
            const mapEl = document.getElementById('portalLeafletMap');
            if (mapEl && window.portalMapInstance) {{
                mapEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                setTimeout(() => {{
                    window.portalMapInstance.setView([lat, lng], 8, {{ animate: true }});
                }}, 350);
            }}
        }}

        let currentSlug = 'all';

        const CATEGORY_TITLES = {{
            {category_titles_js}
        }};

        function filterCategory(slug) {{
            if (slug === 'events') {{
                switchPortalMainView('events');
                return;
            }} else if (slug === 'prices') {{
                switchPortalMainView('prices');
                return;
            }} else {{
                switchPortalMainView('news');
            }}
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
            // PWA Service Worker Registration
            if ('serviceWorker' in navigator) {{
                window.addEventListener('load', function() {{
                    navigator.serviceWorker.register('./sw.js').catch(function() {{}});
                }});
            }}
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
